"""02: the plugin publishes an enumerated payload, not the rest of the repository.

Level 1 (the Claude Code plugin) had no payload declaration at all.  The marketplace
entry said ``"source": "./"``, which means "whatever else happens to be in the
repository", so the plugin published exactly what the Level 2 bundle manifest
deliberately excludes.  This module gives Level 1 its own enumeration -- declared in
``.claude-plugin/plugin.json`` under ``payload`` -- and proves three things about it:

* the enumeration is a list, not a remainder, so a new development directory
  defaults to *not* shipping;
* the enumeration is closed over every file reference the shipped skills, commands
  and their transitively reachable documents make;
* the marketplace entry pins a named, existing, non-floating commit.

The reference scan covers the payload's text documents (``.md``/``.yaml``/``.yml``),
which is where path references live.  Python imports inside ``library/`` are covered
separately by :meth:`PayloadPythonImportTests`.

This declaration is intentionally *independent data* from
``library/local_orchestration/windows_package_manifest.py``.  Level 1 and Level 2
publish different sets over different transports; sharing one literal would let a
change to either silently change the other.

Reading the declaration, matching a path against it and reading the pin are *not*
independent data: they are the same rules the publication step applies, so they
live once in ``plugin_publication`` and are imported here.  A copy kept in this
file would let these tests keep agreeing with themselves while the step that
builds the shipped tree drifted away from both.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final

from library.local_orchestration.plugin_publication import (
    PayloadDeclarationError,
    _is_forbidden,
    commit_exists,
    declared_payload_files,
    declared_payload_paths,
    is_payload_path,
    load_payload_declaration,
    materialise_publication_tree,
    pinned_plugin_source,
)

_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
_PLUGIN_MANIFEST: Final[Path] = _REPO_ROOT / ".claude-plugin" / "plugin.json"
_MARKETPLACE_MANIFEST: Final[Path] = _REPO_ROOT / ".claude-plugin" / "marketplace.json"
_LEVEL_TWO_MANIFEST: Final[Path] = (
    _REPO_ROOT / "library" / "local_orchestration" / "windows_package_manifest.py"
)

_FULL_SHA: Final[re.Pattern[str]] = re.compile(r"[0-9a-f]{40}\Z")
_SEMVER: Final[re.Pattern[str]] = re.compile(r"[0-9]+(?:\.[0-9]+){2}\Z")

# The three trees a plugin user can never reach a use for are held as *segment
# tuples* in :mod:`plugin_publication`, so that "modules/tickets" is expressible
# without also excluding "modules/spec": prefix comparison on raw strings would
# not tell those apart, and would additionally let "skills-old/" match a "skills"
# root.  :func:`_is_forbidden` is imported from there rather than restated here.

_MD_LINK: Final[re.Pattern[str]] = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_INLINE_CODE: Final[re.Pattern[str]] = re.compile(r"`([^`\n]+)`")
_PATH_SUFFIXES: Final[tuple[str, ...]] = (
    ".md", ".py", ".json", ".ps1", ".lock", ".txt", ".cmd", ".yaml", ".yml", ".kt",
)
_SCANNED_SUFFIXES: Final[frozenset[str]] = frozenset({".md", ".yaml", ".yml"})

# Every reference that resolves to a repository path *outside* the payload, with the
# reason it is allowed to stay outside.  Exact equality is asserted, so a new escape
# turns this file red and a repaired one forces a deliberate edit here.
#
#   TARGET_OWNED     the path names an artifact in the *user's* project, not ours;
#                    the workflow tells the agent where to write, it does not ship it.
#                    (ticket 68: the SPEC archive rule of the requirement-lineage reference
#                    names the user's `doc/archive/specs/` and `modules/spec/README.md`.)
#   DEVELOPMENT_ONLY a link into Johnny's own development material.  These are dead
#                    links in published prose and belong on the reviewer's list for
#                    the README/Workflow pass that lands with this mechanism.
_REFERENCES_OUTSIDE_PAYLOAD: Final[dict[str, str]] = {
    "CLAUDE.md": "TARGET_OWNED",
    "CONTEXT.md": "TARGET_OWNED",
    "PRD.md": "TARGET_OWNED",
    "ProjectSchedule.md": "TARGET_OWNED",
    "doc/RequirementChangeLog.md": "TARGET_OWNED",
    "doc/archive/specs/README.md": "TARGET_OWNED",
    "doc/runbooks/dispatch-model-profile.md": "DEVELOPMENT_ONLY",
    "modules/element/": "TARGET_OWNED",
    "modules/spec/README.md": "TARGET_OWNED",
}

# Path-shaped tokens that name no repository path at all.  Kept explicit so that a
# mistyped real reference cannot hide among them.
_UNRESOLVED_REFERENCE_TOKENS: Final[dict[str, str]] = {
    ".claude/worktrees/": "TARGET_OWNED",
    "SKILL.md": "PROSE",
    "WorkProgressReport.md": "PROSE",
    "__init__.py": "PROSE",
    "archive/requirements/README.md": "TARGET_OWNED",
    "camouflage_state/": "PROSE",
    "card_rules_engine/": "PROSE",
    "discovery-change.md": "PROSE",
    "doc/specs/": "TARGET_OWNED",
    "doc/tickets/": "TARGET_OWNED",
    "identity_resolution/": "PROSE",
    "reconciliation/": "PROSE",
    "router-control.md": "PROSE",
    "subscription_ledger/": "PROSE",
}


def _payload_entries(payload: dict[str, object], key: str) -> tuple[str, ...]:
    entries = payload.get(key)
    if not isinstance(entries, list) or not all(isinstance(entry, str) for entry in entries):
        raise AssertionError(f"payload {key} is not a string list")
    return tuple(entries)


class PayloadClosureError(ValueError):
    """Raised when payload content references a path the payload does not carry."""


class ReferenceScanError(ValueError):
    """Raised when a payload file cannot be read, so its references are unknown.

    Never returned as an empty reference set: "unreadable" is not "has no
    references", and a scan that conflates them proves nothing.
    """


def scan_file_references(path: Path) -> frozenset[str]:
    """Every path-shaped token one document names.

    Raises :class:`ReferenceScanError` when the document cannot be read.  A readable
    document with no references returns an empty set; the two outcomes stay
    distinguishable.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ReferenceScanError(f"payload file cannot be scanned: {path}") from error

    tokens: set[str] = {match.split("#")[0] for match in _MD_LINK.findall(text)}
    # Link *text* is prose, not a target: strip whole links before reading inline code.
    for match in _INLINE_CODE.findall(_MD_LINK.sub(" ", text)):
        token = match.strip()
        if " " in token:
            continue
        if token.endswith(_PATH_SUFFIXES) or token.endswith("/"):
            tokens.add(token.split("#")[0])
    return frozenset(
        token
        for token in tokens
        if token
        and not token.startswith(("http://", "https://", "mailto:"))
        and not any(character in token for character in "<>*")
    )


def _resolve(referrer: Path, root: Path, token: str) -> str | None:
    for base in (referrer.parent, root):
        candidate = base / token
        try:
            if candidate.is_file():
                return candidate.resolve().relative_to(root).as_posix()
            if candidate.is_dir():
                return candidate.resolve().relative_to(root).as_posix() + "/"
        except (OSError, ValueError):
            continue
    return None


def closure_report(root: Path, payload: dict[str, object]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return (references escaping the payload, path-shaped tokens resolving nowhere)."""

    escaping: dict[str, set[str]] = {}
    unresolved: dict[str, set[str]] = {}
    for path in declared_payload_files(root, payload):
        if path.suffix.lower() not in _SCANNED_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        for token in scan_file_references(path):
            resolved = _resolve(path, root, token)
            if resolved is None:
                unresolved.setdefault(token, set()).add(relative)
            elif not is_payload_path(resolved, payload):
                escaping.setdefault(resolved, set()).add(relative)
    return escaping, unresolved


def assert_payload_closed(root: Path, payload: dict[str, object]) -> None:
    """Raise unless every reference resolves inside the payload or is declared.

    The publication step calls this before it materialises a release tree, so an
    unclosed payload fails loudly there rather than silently on a user's disk.
    """

    escaping, unresolved = closure_report(root, payload)
    undeclared = sorted(set(escaping) - set(_REFERENCES_OUTSIDE_PAYLOAD))
    stray = sorted(set(unresolved) - set(_UNRESOLVED_REFERENCE_TOKENS))
    if undeclared:
        raise PayloadClosureError(
            "payload content references paths it does not carry: " + ", ".join(undeclared)
        )
    if stray:
        raise PayloadClosureError(
            "payload content names paths that do not exist: " + ", ".join(stray)
        )


class PayloadDeclarationTests(unittest.TestCase):
    """The declaration is an enumeration, and it enumerates the plugin surface."""

    def setUp(self) -> None:
        self.payload = load_payload_declaration(_PLUGIN_MANIFEST)

    def test_the_plugin_surface_is_declared(self) -> None:
        trees = _payload_entries(self.payload, "trees")
        for required in (".claude-plugin", "skills", "commands"):
            with self.subTest(tree=required):
                self.assertIn(required, trees)

    def test_the_declared_payload_is_a_list_not_a_remainder(self) -> None:
        """Every repository top-level entry is either enumerated or not shipped."""

        shipped = {
            entry.name
            for entry in _REPO_ROOT.iterdir()
            if is_payload_path(entry.name if entry.is_file() else entry.name + "/", self.payload)
        }
        declared = set(_payload_entries(self.payload, "trees")) | set(
            _payload_entries(self.payload, "files")
        )
        self.assertTrue(shipped <= declared, f"undeclared entries would ship: {shipped - declared}")

    def test_nested_trees_are_segment_exact_and_clean_at_the_manifest_boundary(self) -> None:
        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "plugin.json"
            manifest.write_text(
                json.dumps(
                    {
                        "payload": {
                            "trees": ["library/NLP", "library/功能集群"],
                            "files": ["AGENTS.md"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            payload = load_payload_declaration(manifest)
            self.assertTrue(is_payload_path("library/NLP/python/model.py", payload))
            self.assertTrue(is_payload_path("library/功能集群/README.md", payload))
            for sibling in (
                "library/NLP-old/model.py",
                "library/NLPx/model.py",
                "library/新功能集群/README.md",
            ):
                with self.subTest(path=sibling):
                    self.assertFalse(is_payload_path(sibling, payload))

            malformed_trees = (
                ["library/../NLP"],
                ["/library/NLP"],
                ["library//NLP"],
                [" library/NLP"],
                ["library/NLP "],
                ["."],
                [".."],
                ["C:/library/NLP"],
                ["library/NLP", "library/NLP/models"],
            )
            for trees in malformed_trees:
                with self.subTest(trees=trees):
                    manifest.write_text(
                        json.dumps({"payload": {"trees": trees, "files": ["AGENTS.md"]}}),
                        encoding="utf-8",
                    )
                    with self.assertRaises(PayloadDeclarationError):
                        load_payload_declaration(manifest)

    def test_excluded_payload_admission_is_a_reversible_red_mutation(self) -> None:
        original = _PLUGIN_MANIFEST.read_bytes()
        committed = load_payload_declaration(_PLUGIN_MANIFEST)
        self.assertFalse(is_payload_path("library/local_orchestration/README.md", committed))
        self.assertFalse(is_payload_path("install.ps1", committed))
        committed_paths = {
            path.relative_to(_REPO_ROOT).as_posix()
            for path in declared_payload_files(_REPO_ROOT, committed)
        }
        self.assertFalse(
            any(path.startswith("library/local_orchestration/") for path in committed_paths)
        )
        self.assertNotIn("install.ps1", committed_paths)

        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "plugin.json"
            candidate = json.loads(original.decode("utf-8"))
            candidate["payload"]["trees"].append("library/local_orchestration")
            manifest.write_text(json.dumps(candidate), encoding="utf-8")
            widened = load_payload_declaration(manifest)
            with self.assertRaises(AssertionError):
                self.assertFalse(
                    is_payload_path("library/local_orchestration/README.md", widened)
                )

            manifest.write_bytes(original)
            restored = load_payload_declaration(manifest)
            self.assertEqual(manifest.read_bytes(), original)
            self.assertFalse(is_payload_path("library/local_orchestration/README.md", restored))

    def test_every_declared_entry_exists(self) -> None:
        self.assertGreater(len(declared_payload_files(_REPO_ROOT, self.payload)), 0)

    def test_the_excluded_trees_are_not_shipped(self) -> None:
        """tests/, doc/ and modules/tickets/ never appear in the payload."""

        for probe in (
            "tests/test_plugin_payload_boundary.py",
            "doc/runbooks/dispatch-model-profile.md",
            "modules/tickets/TEMPLATE.md",
        ):
            with self.subTest(path=probe):
                self.assertFalse(is_payload_path(probe, self.payload))
        for path in declared_payload_files(_REPO_ROOT, self.payload):
            relative = path.relative_to(_REPO_ROOT).as_posix()
            with self.subTest(path=relative):
                self.assertFalse(_is_forbidden(tuple(relative.split("/"))))

    def test_a_declaration_naming_an_excluded_tree_is_rejected(self) -> None:
        for illegal in ("tests", "doc"):
            with self.subTest(tree=illegal), TemporaryDirectory() as raw:
                manifest = Path(raw) / "plugin.json"
                manifest.write_text(
                    json.dumps({"payload": {"trees": ["skills", illegal], "files": ["AGENTS.md"]}}),
                    encoding="utf-8",
                )
                with self.assertRaises(PayloadDeclarationError):
                    load_payload_declaration(manifest)

    def test_a_declaration_naming_modules_tickets_is_rejected(self) -> None:
        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "plugin.json"
            manifest.write_text(
                json.dumps({"payload": {"trees": ["skills"], "files": ["modules/tickets/TEMPLATE.md"]}}),
                encoding="utf-8",
            )
            with self.assertRaises(PayloadDeclarationError):
                load_payload_declaration(manifest)

    def test_an_absent_declaration_is_rejected(self) -> None:
        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "plugin.json"
            manifest.write_text(json.dumps({"name": "x"}), encoding="utf-8")
            with self.assertRaises(PayloadDeclarationError):
                load_payload_declaration(manifest)


class PayloadPathMatchingTests(unittest.TestCase):
    """Membership is segment-exact, so neighbouring names cannot leak in."""

    def setUp(self) -> None:
        self.payload = load_payload_declaration(_PLUGIN_MANIFEST)

    def test_a_similar_prefix_does_not_join_the_payload(self) -> None:
        self.assertTrue(is_payload_path("skills/johnny-project-takeover/SKILL.md", self.payload))
        for impostor in ("skills-old/SKILL.md", "skillsx/SKILL.md", "library-backup/x.md"):
            with self.subTest(path=impostor):
                self.assertFalse(is_payload_path(impostor, self.payload))

    def test_modules_and_modules_tickets_stay_distinguishable(self) -> None:
        """The exclusion mechanism can name modules/tickets without naming modules/spec."""

        self.assertTrue(_is_forbidden(("modules", "tickets", "TEMPLATE.md")))
        self.assertFalse(_is_forbidden(("modules", "spec", "workflow-governance.md")))
        self.assertFalse(_is_forbidden(("modules-archive", "tickets", "x.md")))

    def test_the_spec_archive_is_not_a_payload_path(self) -> None:
        """Ticket 68: archived SPECs are development material; no similar name joins the payload either."""

        for archived in (
            "doc/archive/specs/README.md",
            "doc/archive/specs/2026/README.md",
            "doc/archive/specs/2026/router-framework.md",
            "doc/archive/specs-old/x.md",
        ):
            with self.subTest(path=archived):
                self.assertFalse(is_payload_path(archived, self.payload))

    def test_excluded_segments_and_suffixes_are_honoured(self) -> None:
        self.assertFalse(is_payload_path("library/__pycache__/x.pyc", self.payload))
        self.assertFalse(is_payload_path("library/workflow_router/router.pyc", self.payload))
        self.assertTrue(is_payload_path("library/workflow_router/router.py", self.payload))

    def test_empty_and_traversing_paths_are_refused(self) -> None:
        for bad in ("", "/", "..", "skills/../tests/x.py", "./skills/x.md"):
            with self.subTest(path=bad):
                self.assertFalse(is_payload_path(bad, self.payload))


class ReferenceScanTests(unittest.TestCase):
    """An unreadable document is a named failure, never a silent empty result."""

    def test_a_readable_document_without_references_returns_empty(self) -> None:
        with TemporaryDirectory() as raw:
            document = Path(raw) / "plain.md"
            document.write_text("# Title\n\nNo paths here at all.\n", encoding="utf-8")
            self.assertEqual(scan_file_references(document), frozenset())

    def test_an_absent_document_raises_instead_of_returning_empty(self) -> None:
        with TemporaryDirectory() as raw:
            with self.assertRaises(ReferenceScanError):
                scan_file_references(Path(raw) / "missing.md")

    def test_an_undecodable_document_raises(self) -> None:
        with TemporaryDirectory() as raw:
            document = Path(raw) / "binary.md"
            document.write_bytes(b"\xff\xfe\x00\x00 not utf-8 \xc3\x28")
            with self.assertRaises(ReferenceScanError):
                scan_file_references(document)

    def test_markdown_link_targets_are_found_and_link_text_is_not(self) -> None:
        with TemporaryDirectory() as raw:
            document = Path(raw) / "doc.md"
            document.write_text(
                "See [`pretty_name/README.md`](../../real/target.md) and `bare/path.md`.\n",
                encoding="utf-8",
            )
            found = scan_file_references(document)
            self.assertIn("../../real/target.md", found)
            self.assertIn("bare/path.md", found)
            self.assertNotIn("pretty_name/README.md", found)

    def test_placeholders_and_urls_are_not_paths(self) -> None:
        with TemporaryDirectory() as raw:
            document = Path(raw) / "doc.md"
            document.write_text(
                "`modules/spec/<feature>.md` `*_reducer.py` [x](https://example.com/a.md)\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_file_references(document), frozenset())

    def test_every_payload_document_is_actually_readable(self) -> None:
        """Fail closed: the closure proof is worthless if a document was skipped."""

        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        scanned = 0
        for path in declared_payload_files(_REPO_ROOT, payload):
            if path.suffix.lower() in _SCANNED_SUFFIXES:
                scan_file_references(path)
                scanned += 1
        self.assertGreater(scanned, 0, "the reference scan read nothing at all")


class PayloadClosureTests(unittest.TestCase):
    """Nothing the payload names falls outside the payload without a stated reason."""

    def setUp(self) -> None:
        self.payload = load_payload_declaration(_PLUGIN_MANIFEST)
        self.escaping, self.unresolved = closure_report(_REPO_ROOT, self.payload)

    def test_the_skills_and_commands_are_carried(self) -> None:
        shipped = {
            path.relative_to(_REPO_ROOT).as_posix()
            for path in declared_payload_files(_REPO_ROOT, self.payload)
        }
        for required in (
            "skills/apply-reusable-modules/SKILL.md",
            "skills/johnny-project-takeover/SKILL.md",
            "commands/apply-reusable-modules.md",
            "commands/johnny-project-takeover.md",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
        ):
            with self.subTest(path=required):
                self.assertIn(required, shipped)

    def test_the_documents_the_skills_read_are_carried(self) -> None:
        """The closure the skills actually walk: Workflow, CodeReview, wayfinder, catalog."""

        shipped = {
            path.relative_to(_REPO_ROOT).as_posix()
            for path in declared_payload_files(_REPO_ROOT, self.payload)
        }
        for required in (
            "Workflow.md",
            "CodeReview.md",
            "Defined_wayfinder.md",
            "AGENTS.md",
            "library/MODULE_CATALOG.md",
            "library/workflow_router/contracts.py",
            "template/README.md",
        ):
            with self.subTest(path=required):
                self.assertIn(required, shipped)

    def test_every_reference_that_escapes_is_a_declared_exception(self) -> None:
        self.assertEqual(
            set(self.escaping),
            set(_REFERENCES_OUTSIDE_PAYLOAD),
            "the set of references leaving the payload changed",
        )

    def test_every_path_shaped_token_resolving_nowhere_is_declared(self) -> None:
        self.assertEqual(
            set(self.unresolved),
            set(_UNRESOLVED_REFERENCE_TOKENS),
            "a path-shaped token that names nothing appeared or disappeared",
        )

    def test_no_skill_or_command_points_at_our_own_development_material(self) -> None:
        """A skill may name a path in the *user's* project; it may not name ours.

        The two are not distinguishable by shape -- ``doc/RequirementChangeLog.md``
        is a target-owned index whose name also exists in this repository -- so the
        category recorded in the declaration is what decides.
        """

        for escape, referrers in self.escaping.items():
            if _REFERENCES_OUTSIDE_PAYLOAD[escape] != "DEVELOPMENT_ONLY":
                continue
            offenders = {r for r in referrers if r.startswith(("skills/", "commands/"))}
            with self.subTest(reference=escape):
                self.assertEqual(offenders, set(), f"{escape} is reached from {offenders}")

    def test_target_owned_references_are_never_shipped(self) -> None:
        """Naming a target-owned path is correct; carrying our copy of it is not."""

        for escape, category in _REFERENCES_OUTSIDE_PAYLOAD.items():
            if category != "TARGET_OWNED":
                continue
            with self.subTest(reference=escape):
                self.assertFalse(is_payload_path(escape, self.payload))

    def test_the_committed_payload_is_closed(self) -> None:
        assert_payload_closed(_REPO_ROOT, self.payload)

    def test_a_shrunken_payload_raises_a_closure_error(self) -> None:
        """Dropping a tree the skills read must be caught, not tolerated."""

        narrowed = dict(self.payload)
        narrowed["trees"] = [
            t
            for t in _payload_entries(self.payload, "trees")
            if t != "library/workflow_router"
        ]
        with self.assertRaises(PayloadClosureError) as caught:
            assert_payload_closed(_REPO_ROOT, narrowed)
        self.assertIn("library/workflow_router/contracts.py", str(caught.exception))

    def test_a_closure_error_is_not_a_declaration_error(self) -> None:
        """Two failures, two names: the gate must say which one it hit."""

        self.assertFalse(issubclass(PayloadClosureError, PayloadDeclarationError))
        self.assertFalse(issubclass(PayloadDeclarationError, PayloadClosureError))


class PinnedSourceValidatorTests(unittest.TestCase):
    """The validator itself, exercised on inputs it must refuse.

    Deliberately independent of the committed manifest: when the real declaration
    regresses, these stay green and name the validator as still correct, so the
    failure is attributable to the declaration rather than to the check.
    """

    def test_an_abbreviated_sha_is_rejected(self) -> None:
        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "marketplace.json"
            manifest.write_text(
                json.dumps(
                    {"plugins": [{"source": {"source": "url", "url": "u", "sha": "9073ac54"}}]}
                ),
                encoding="utf-8",
            )
            with self.assertRaises(PayloadDeclarationError):
                pinned_plugin_source(manifest)

    def test_a_floating_ref_is_rejected(self) -> None:
        for floating in ("main", "master", "HEAD"):
            with self.subTest(ref=floating), TemporaryDirectory() as raw:
                manifest = Path(raw) / "marketplace.json"
                manifest.write_text(
                    json.dumps(
                        {
                            "plugins": [
                                {
                                    "source": {
                                        "source": "url",
                                        "url": "u",
                                        "ref": floating,
                                        "sha": "9073ac54511d54157f4d5b54f32df2c8d9206547",
                                    }
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                with self.assertRaises(PayloadDeclarationError):
                    pinned_plugin_source(manifest)

    def test_a_bare_relative_source_is_rejected(self) -> None:
        with TemporaryDirectory() as raw:
            manifest = Path(raw) / "marketplace.json"
            manifest.write_text(
                json.dumps({"plugins": [{"source": "./"}]}), encoding="utf-8"
            )
            with self.assertRaises(PayloadDeclarationError):
                pinned_plugin_source(manifest)

    def test_a_nonexistent_sha_is_observable(self) -> None:
        self.assertFalse(commit_exists(_REPO_ROOT, "0" * 40))


class CommittedPinTests(unittest.TestCase):
    """What the repository actually declares today."""

    def test_the_source_is_no_longer_the_rest_of_the_repository(self) -> None:
        document = json.loads(_MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
        self.assertNotEqual(document["plugins"][0]["source"], "./")

    def test_the_committed_source_survives_the_validator(self) -> None:
        self.assertIn("sha", pinned_plugin_source(_MARKETPLACE_MANIFEST))

    def test_the_pinned_sha_is_a_full_lowercase_sha(self) -> None:
        source = pinned_plugin_source(_MARKETPLACE_MANIFEST)
        self.assertIsNotNone(_FULL_SHA.fullmatch(str(source["sha"])))

    def test_the_pinned_sha_exists(self) -> None:
        source = pinned_plugin_source(_MARKETPLACE_MANIFEST)
        self.assertTrue(
            commit_exists(_REPO_ROOT, str(source["sha"])),
            "the pinned sha names no commit in this repository",
        )

    def test_the_plugin_and_marketplace_versions_agree(self) -> None:
        plugin = json.loads(_PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        market = json.loads(_MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
        self.assertIsNotNone(_SEMVER.fullmatch(str(plugin["version"])))
        self.assertEqual(plugin["version"], market["plugins"][0]["version"])


_RELEASE_VERSION: Final[str] = "0.5.0"
_PLUGIN_ID: Final[str] = "software-factory"
_AUTHOR_NAME: Final[str] = "Johnny Liu"
_PUBLICATION_REPOSITORY: Final[str] = (
    "https://github.com/johnnyliu365-sys/software-factory-plugin"
)
_CLAUDE_COMMANDS: Final[tuple[str, ...]] = (
    "claude plugin marketplace add https://raw.githubusercontent.com/johnnyliu365-sys/"
    "software-factory-plugin/marketplace/.claude-plugin/marketplace.json",
    "claude plugin install software-factory@software-factory --scope user",
    "claude plugin update software-factory@software-factory --scope user",
    "claude plugin uninstall software-factory@software-factory --scope user",
    "claude plugin marketplace remove software-factory",
)
_LEVEL_TWO_FILES: Final[tuple[str, ...]] = (
    "install.ps1",
    "johnny-install.cmd",
    "johnny-router.ps1",
    "requirements-runtime.lock",
)
_EMAIL: Final[re.Pattern[str]] = re.compile(r"[^\s@\"]+@[^\s@\"]+\.[^\s@\"]+")
_FENCE: Final[re.Pattern[str]] = re.compile(r"^```[a-z]*\n(.*?)^```$", re.M | re.S)
_SECTION_HEADING: Final[re.Pattern[str]] = re.compile(r"^## ([0-9]+)\. ", re.M)


def _field(document: object, *steps: str | int) -> object:
    """Walk a parsed JSON document, failing loudly when a step is absent."""

    current = document
    for step in steps:
        if isinstance(step, int):
            if not isinstance(current, list) or step >= len(current):
                raise AssertionError(f"manifest has no element {step} at {steps}")
            current = current[step]
        else:
            if not isinstance(current, dict) or step not in current:
                raise AssertionError(f"manifest has no field {step} at {steps}")
            current = current[step]
    return current


def _with_field(document: object, value: object, *steps: str | int) -> object:
    """A deep copy of ``document`` with the field at ``steps`` set to ``value``."""

    copy = json.loads(json.dumps(document))
    parent = _field(copy, *steps[:-1])
    last = steps[-1]
    if isinstance(last, int) and isinstance(parent, list):
        parent[last] = value
    elif isinstance(last, str) and isinstance(parent, dict):
        parent[last] = value
    else:
        raise AssertionError(f"cannot set {steps}")
    return copy


def _strings_under(document: object) -> list[str]:
    if isinstance(document, str):
        return [document]
    if isinstance(document, dict):
        return [text for value in document.values() for text in _strings_under(value)]
    if isinstance(document, list):
        return [text for value in document for text in _strings_under(value)]
    return []


def _assert_shipped_manifests(plugin: object, market: object) -> None:
    """The identity, version, licence and author both shipped manifests must carry."""

    entry = _field(market, "plugins", 0)
    expected: tuple[tuple[object, tuple[str | int, ...], str], ...] = (
        (plugin, ("name",), _PLUGIN_ID),
        (plugin, ("version",), _RELEASE_VERSION),
        (plugin, ("license",), "Apache-2.0"),
        (plugin, ("author", "name"), _AUTHOR_NAME),
        (plugin, ("homepage",), _PUBLICATION_REPOSITORY),
        (plugin, ("repository",), _PUBLICATION_REPOSITORY),
        (market, ("name",), _PLUGIN_ID),
        (market, ("owner", "name"), _AUTHOR_NAME),
        (entry, ("name",), _PLUGIN_ID),
        (entry, ("version",), _RELEASE_VERSION),
        (entry, ("license",), "Apache-2.0"),
        (entry, ("author", "name"), _AUTHOR_NAME),
    )
    for document, steps, wanted in expected:
        found = _field(document, *steps)
        if found != wanted:
            raise AssertionError(f"{'.'.join(map(str, steps))} is {found!r}, not {wanted!r}")
    for holder in (
        _field(plugin, "author"),
        _field(market, "owner"),
        _field(entry, "author"),
    ):
        for text in _strings_under(holder):
            if "@" in text:
                raise AssertionError(f"an author or owner field holds an address: {text!r}")
    for key in ("description", "keywords", "homepage", "repository", "license", "version"):
        if _field(plugin, key) != _field(entry, key):
            raise AssertionError(f"the marketplace entry differs from plugin.json at {key}")


def _section_three_commands(readme: str) -> tuple[str, ...]:
    """The lines at column 0 of fenced blocks in section 3 that start a claude command."""

    start = readme.index("## 3. ")
    end = readme.index("## 4. ")
    lines: list[str] = []
    for block in _FENCE.findall(readme[start:end]):
        lines.extend(line for line in block.splitlines() if line.startswith("claude plugin "))
    return tuple(lines)


def _assert_readme_is_software_factory(readme: str) -> None:
    numbers = [int(number) for number in _SECTION_HEADING.findall(readme)]
    if numbers != list(range(1, 11)):
        raise AssertionError(f"the README sections are {numbers}, not 1 to 10 in order")
    if _section_three_commands(readme) != _CLAUDE_COMMANDS:
        raise AssertionError("section 3 does not hold exactly the five Claude Code commands")
    if "codex plugin add software-factory@software-factory --json" not in readme:
        raise AssertionError("the README lacks the Codex plugin add step")
    if "johnny-install.cmd" in readme:
        raise AssertionError("the README names johnny-install.cmd")
    for heading in re.findall(r"^#+ .*$", readme, re.M):
        if re.search(r"Level 2", heading) and re.search(r"安裝|install", heading, re.I):
            raise AssertionError(f"a Level 2 install section is back: {heading}")


class ShippedManifestTests(unittest.TestCase):
    """Software Factory 0.5.0: the id, the version, the licence and the author."""

    def setUp(self) -> None:
        self.plugin: object = json.loads(_PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        self.market: object = json.loads(_MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
        self.readme = (_REPO_ROOT / "README.md").read_text(encoding="utf-8")

    def test_the_shipped_manifests_carry_the_id_version_licence_and_author(self) -> None:
        _assert_shipped_manifests(self.plugin, self.market)

    def test_the_pin_source_names_the_publication_repository(self) -> None:
        source = pinned_plugin_source(_MARKETPLACE_MANIFEST)
        self.assertEqual(source["url"], _PUBLICATION_REPOSITORY + ".git")

    def test_no_shipped_manifest_holds_an_email_address(self) -> None:
        for manifest in (_PLUGIN_MANIFEST, _MARKETPLACE_MANIFEST):
            with self.subTest(manifest=manifest.name):
                self.assertIsNone(_EMAIL.search(manifest.read_text(encoding="utf-8")))

    def test_a_wrong_manifest_value_is_red_and_the_real_pair_is_restored_green(self) -> None:
        mutations: tuple[tuple[str, tuple[str | int, ...], object], ...] = (
            ("plugin", ("license",), "Proprietary"),
            ("market", ("plugins", 0, "license"), "Proprietary"),
            ("plugin", ("name",), "johnny-ai-skill"),
            ("market", ("name",), "johnny-ai-skill"),
            ("market", ("plugins", 0, "name"), "johnny-ai-skill"),
            ("plugin", ("version",), "0.4.14"),
            ("market", ("plugins", 0, "version"), "0.5.1"),
            ("plugin", ("author", "name"), "Johnny AI Skill"),
            ("plugin", ("author", "name"), ""),
            ("market", ("owner", "name"), ""),
            ("market", ("plugins", 0, "author", "name"), "Someone Else"),
            ("plugin", ("author", "email"), "johnny@example.org"),
            ("market", ("owner", "email"), "johnny@example.org"),
            ("market", ("plugins", 0, "author", "email"), "johnny@example.org"),
        )
        for which, steps, value in mutations:
            with self.subTest(manifest=which, steps=steps, value=value):
                plugin = self.plugin
                market = self.market
                if which == "plugin":
                    plugin = _with_field(plugin, value, *steps)
                else:
                    market = _with_field(market, value, *steps)
                with self.assertRaises(AssertionError):
                    _assert_shipped_manifests(plugin, market)
        _assert_shipped_manifests(self.plugin, self.market)

    def test_the_readme_is_the_software_factory_readme(self) -> None:
        _assert_readme_is_software_factory(self.readme)

    def test_a_level_two_install_step_or_a_missing_codex_step_in_the_readme_is_red(self) -> None:
        old_section = (
            "## Level 2：安裝完整 Router Runtime\n\n"
            "1. 把 johnny-install.cmd 和 release 的 zip 下載到同一個資料夾\n"
        )
        mutations = (
            self.readme + "\n" + old_section,
            self.readme + "\n## Level 2：安裝完整 Runtime\n",
            self.readme + "\nRun johnny-install.cmd to install.\n",
            self.readme.replace(
                "codex plugin add software-factory@software-factory --json", "codex plugin list"
            ),
            self.readme.replace(
                "claude plugin install software-factory@software-factory --scope user",
                "claude plugin install johnny-ai-skill@johnny-ai-skill --scope user",
            ),
            self.readme.replace("## 6. ", "## 7. ", 1),
        )
        for index, mutated in enumerate(mutations):
            with self.subTest(mutation=index):
                self.assertNotEqual(mutated, self.readme)
                with self.assertRaises(AssertionError):
                    _assert_readme_is_software_factory(mutated)
        _assert_readme_is_software_factory(self.readme)

    def test_notice_names_the_product_and_the_publication_repository(self) -> None:
        notice = (_REPO_ROOT / "NOTICE").read_text(encoding="utf-8")
        self.assertEqual(notice.splitlines()[0], "Software Factory")
        self.assertIn(f"Repository: {_PUBLICATION_REPOSITORY}\n", notice)
        self.assertIn("Copyright 2026 Johnny Liu", notice)


class PublicationTreeContentTests(unittest.TestCase):
    """The publication tree carries the licence texts and no Level 2 file."""

    _CARRIED: Final[tuple[str, ...]] = ("LICENSE", "NOTICE", "README.md")

    def _assert_carried(self, payload: dict[str, object]) -> None:
        declared = set(declared_payload_paths(_REPO_ROOT, payload))
        for required in self._CARRIED:
            if required not in declared:
                raise AssertionError(f"the publication tree does not carry {required}")

    def test_the_publication_tree_carries_license_notice_and_readme(self) -> None:
        self._assert_carried(load_payload_declaration(_PLUGIN_MANIFEST))

    def test_dropping_notice_from_the_payload_is_red_and_restores_green(self) -> None:
        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        files = [entry for entry in _payload_entries(payload, "files") if entry != "NOTICE"]
        self.assertNotEqual(files, list(_payload_entries(payload, "files")))
        with self.assertRaises(AssertionError):
            self._assert_carried({**payload, "files": files})
        self._assert_carried(payload)

    def test_the_publication_tree_holds_no_codex_manifest_and_no_level_two_file(self) -> None:
        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        declared = declared_payload_paths(_REPO_ROOT, payload)
        for path in declared:
            with self.subTest(path=path):
                self.assertFalse(path.startswith(".codex-plugin"))
                self.assertFalse(path.startswith("library/local_orchestration/"))
                self.assertNotIn(path, _LEVEL_TWO_FILES)

    def test_the_materialised_tree_carries_the_licence_texts(self) -> None:
        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        with TemporaryDirectory(ignore_cleanup_errors=True) as raw:
            destination = Path(raw) / "payload"
            materialise_publication_tree(_REPO_ROOT, payload, destination)
            for required in self._CARRIED:
                with self.subTest(path=required):
                    self.assertEqual(
                        (destination / required).read_bytes(),
                        (_REPO_ROOT / required).read_bytes(),
                    )


class ManifestIndependenceTests(unittest.TestCase):
    """Level 1 and Level 2 hold separate data; neither edit reaches the other."""

    def test_level_one_does_not_import_the_level_two_manifest(self) -> None:
        module = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imported = {
            node.module
            for node in ast.walk(module)
            if isinstance(node, ast.ImportFrom) and node.module
        } | {
            alias.name
            for node in ast.walk(module)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        for name in imported:
            with self.subTest(module=name):
                self.assertNotIn("windows_package_manifest", name)

    def test_the_two_payload_lists_are_different_literals(self) -> None:
        """Same shape, separate data: Level 2 ships no template/, Level 1 no root lock."""

        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        level_two = _read_level_two_tree_roots()
        trees = set(_payload_entries(payload, "trees"))
        self.assertNotEqual(trees, level_two)
        self.assertIn("template", trees)
        self.assertNotIn("template", level_two)

    def test_the_level_two_manifest_is_untouched_by_this_ticket(self) -> None:
        """Its exclusion of tests/ is the precedent Level 1 copied, not shared."""

        source = _LEVEL_TWO_MANIFEST.read_text(encoding="utf-8")
        self.assertIn('_PAYLOAD_TREE_ROOTS', source)
        self.assertNotIn("payload", json.loads(_PLUGIN_MANIFEST.read_text(encoding="utf-8")).get("nothing", {}))


class PayloadPythonImportTests(unittest.TestCase):
    """No shipped Python module imports a package the payload leaves behind."""

    def test_no_payload_module_imports_an_excluded_tree(self) -> None:
        payload = load_payload_declaration(_PLUGIN_MANIFEST)
        offenders: list[tuple[str, str]] = []
        for path in declared_payload_files(_REPO_ROOT, payload):
            if path.suffix != ".py":
                continue
            relative = path.relative_to(_REPO_ROOT).as_posix()
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, SyntaxError, UnicodeDecodeError) as error:
                raise ReferenceScanError(f"payload module cannot be parsed: {relative}") from error
            names: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    names.add(node.module)
            for name in names:
                root_package = name.split(".")[0]
                if _is_forbidden((root_package,)):
                    offenders.append((relative, name))
        self.assertEqual(offenders, [], f"payload modules import excluded trees: {offenders}")


def _read_level_two_tree_roots() -> set[str]:
    """Parse Level 2's frozenset literal without importing its dependencies."""

    tree = ast.parse(_LEVEL_TWO_MANIFEST.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "_PAYLOAD_TREE_ROOTS" and node.value is not None:
                call = node.value
                if isinstance(call, ast.Call) and call.args:
                    return set(ast.literal_eval(call.args[0]))
    raise AssertionError("_PAYLOAD_TREE_ROOTS could not be read from Level 2")


if __name__ == "__main__":
    unittest.main()
