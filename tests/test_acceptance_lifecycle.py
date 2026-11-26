"""Ticket 77: the 0.5.0 install lifecycle script, run against fake host CLIs, and the locks on acceptance.yml.

A fake host CLI is a Python file started through `sys.executable`, so every case here runs on both runners of
`ci.yml`. The fake keeps its state in the step directory the script gives it, and logs every call with the
environment it received. A case that needs Windows is skipped elsewhere, with its reason.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / "ci" / "acceptance"
sys.path.insert(0, str(ACCEPTANCE))

import lifecycle  # noqa: E402  (found through the path above)

README = ACCEPTANCE / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "acceptance.yml"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
REPOSITORY_README = ROOT / "README.md"
ZEROS = "0" * 40
TICKET_ENV_ALLOW_LIST = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TEMP",
    "TMP",
    "LOCALAPPDATA",
    "APPDATA",
    "PROGRAMDATA",
)

FAKE_CLI = r'''
import json, os, shutil, subprocess, sys
from pathlib import Path

host, log_path, mode, pinned = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
args = sys.argv[5:]
home = Path(os.environ["CLAUDE_CONFIG_DIR" if host == "claude" else "CODEX_HOME"])
with open(log_path, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({"host": host, "args": args, "cwd": os.getcwd(), "env": dict(os.environ)}) + "\n")
state_file = home / "fake-state.json"
state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {"marketplaces": {}, "installed": {}}


def save():
    state_file.write_text(json.dumps(state), encoding="utf-8")


def fail(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def marketplace_file(root, for_host):
    first = ".agents/plugins/marketplace.json" if for_host == "codex" else ".claude-plugin/marketplace.json"
    second = ".claude-plugin/marketplace.json"
    for relative in (first, second) if for_host == "codex" else (first,):
        candidate = Path(root) / relative
        if candidate.is_file():
            return candidate
    fail("Error: no marketplace file")


def entry_of(path):
    document = json.loads(path.read_text(encoding="utf-8"))
    return document["name"], document["plugins"][0]


def git(*arguments):
    subprocess.run(["git", *arguments], check=True, capture_output=True)


if args == ["--version"]:
    print(host + " 9.9.9 (fake) maintainer@example.com")
    sys.exit(0)
if args[:3] == ["plugin", "marketplace", "add"]:
    source = args[3]
    if mode == "no_file_url" and source.startswith("file:"):
        fail("Error: invalid marketplace source format; expected owner/repo, a git URL, or a local marketplace path")
    if source.startswith("http") or source.startswith("johnnyliu365-sys/"):
        state["marketplaces"]["johnny-ai-skill"] = {"kind": "old"}
    elif source.startswith("file:"):
        reference = args[args.index("--ref") + 1]
        destination = home / "mk"
        git("clone", "-q", "-b", reference, source, str(destination))
        name, _ = entry_of(destination / ".claude-plugin" / "marketplace.json")
        state["marketplaces"][name] = {"kind": "git", "root": str(destination)}
    else:
        path = marketplace_file(source, host)
        name, _ = entry_of(path)
        state["marketplaces"][name] = {"kind": "dir", "root": source, "file": str(path)}
    save()
    print("added")
    sys.exit(0)
if args[:3] == ["plugin", "marketplace", "remove"]:
    state["marketplaces"].pop(args[3], None)
    save()
    if mode == "leftover":
        (home / "settings.json").write_text('{"extraKnownMarketplaces": {"software-factory": {}}}\n', encoding="utf-8")
    if mode == "prefix_only":
        (home / "settings.json").write_text('{"x": "software-factory-plugin", "y": "my-software-factory"}\n', encoding="utf-8")
    print("removed")
    sys.exit(0)
if args[:3] == ["plugin", "marketplace", "list"]:
    names = sorted(state["marketplaces"])
    if host == "claude":
        print(json.dumps([{"name": name} for name in names]))
    else:
        print(json.dumps({"marketplaces": [{"name": name, "root": "x"} for name in names]}))
    sys.exit(0)
if args[0:2] in (["plugin", "install"], ["plugin", "add"]):
    if mode == "fail_install":
        fail("Error: the install failed")
    identity = args[2]
    name, market = identity.split("@")
    known = state["marketplaces"].get(market)
    if known is None:
        fail("Error: marketplace not found")
    installed_path = home / "plugins" / "cache" / market / name
    if known["kind"] == "old":
        state["installed"][identity] = {"version": "0.4.14"}
        if host == "claude":
            plugins = home / "plugins"
            plugins.mkdir(parents=True, exist_ok=True)
            commit = pinned if mode != "wrong_commit" else "1" * 40
            (plugins / "installed_plugins.json").write_text(
                json.dumps({"version": 2, "plugins": {identity: [{"gitCommitSha": commit}]}}), encoding="utf-8"
            )
    elif known["kind"] == "git":
        _, entry = entry_of(Path(known["root"]) / ".claude-plugin" / "marketplace.json")
        source = entry["source"]
        installed_path = installed_path / source["sha"]
        git("clone", "-q", source["url"], str(installed_path))
        if mode != "ignore_sha":
            git("-C", str(installed_path), "checkout", "-q", source["sha"])
        state["installed"][identity] = {"version": entry["version"]}
    else:
        _, entry = entry_of(Path(known["file"]))
        source = entry["source"]
        if isinstance(source, dict) and "sha" in source:
            if mode == "old_refused":
                fail("Error: git checkout " + source["sha"] + " failed with status exit code: 128")
            installed_path = installed_path / entry["version"]
            git("clone", "-q", source["url"], str(installed_path))
            git("-C", str(installed_path), "checkout", "-q", source["sha"])
            state["installed"][identity] = {"version": entry["version"]}
            save()
            print(json.dumps({"pluginId": identity, "name": name, "marketplaceName": market,
                              "version": entry["version"], "installedPath": str(installed_path)}))
            sys.exit(0)
        relative = source if isinstance(source, str) else source["path"]
        target = Path(known["root"]) / relative
        if not target.is_dir() and mode != "lenient":
            fail("Error: Source path does not exist: " + str(target))
        state["installed"][identity] = {"version": entry["version"]}
        installed_path = installed_path / entry["version"]
        installed_path.mkdir(parents=True, exist_ok=True)
        (installed_path / "plugin.json").write_text('{"name": "software-factory"}\n', encoding="utf-8")
    save()
    if host == "codex":
        print(json.dumps({"pluginId": identity, "name": name, "marketplaceName": market,
                          "version": state["installed"][identity]["version"], "installedPath": str(installed_path)}))
    else:
        print("installed " + identity)
    sys.exit(0)
if args[0:2] == ["plugin", "list"]:
    if mode == "no_list_json":
        fail("error: unknown option '--json'")
    rows = state["installed"]
    on = mode != "disabled"
    if host == "claude":
        listed = [{"id": key, "version": value["version"], "scope": "user", "enabled": on} for key, value in rows.items()]
        if mode == "flagless":
            for row in listed:
                del row["enabled"]
        print(json.dumps(listed))
    else:
        market = args[args.index("--marketplace") + 1]
        listed = [
            {"pluginId": key, "name": key.split("@")[0], "marketplaceName": key.split("@")[1],
             "version": value["version"], "installed": True, "enabled": on}
            for key, value in rows.items() if key.endswith("@" + market)
        ]
        if mode == "flagless":
            for row in listed:
                del row["enabled"]
        print(json.dumps({"installed": listed, "available": []}))
    sys.exit(0)
if args[0:2] == ["plugin", "update"]:
    print("nothing to update")
    sys.exit(0)
if args[0:2] in (["plugin", "uninstall"], ["plugin", "remove"]):
    identity = args[2]
    if identity not in state["installed"]:
        fail("Error: not found in installed plugins")
    del state["installed"][identity]
    save()
    if host == "codex":
        name, market = identity.split("@")
        shutil.rmtree(home / "plugins" / "cache" / market / name, ignore_errors=True)
        print(json.dumps({"pluginId": identity}))
    sys.exit(0)
fail("error: unknown command " + " ".join(args), 2)
'''

FAKE_LEVEL2 = r'''
import json, os, shutil, sys
from pathlib import Path

action, log_path, mode = sys.argv[1], sys.argv[2], sys.argv[3]
root = Path(os.environ["JOHNNY_ROOT"])
if action == "install":
    answer = sys.stdin.read()
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"answer": answer, "root_entries": sorted(item.name for item in root.iterdir()),
                                 "has_userprofile": "USERPROFILE" in os.environ, "cwd": os.getcwd(),
                                 "wrapper": sys.argv[4], "home": os.environ.get("HOME"),
                                 "env_names": sorted(name.upper() for name in os.environ)}) + "\n")
    if answer != "INSTALL\n":
        sys.exit(2)
    (root / "launcher").mkdir()
    (root / "launcher" / "johnny-router.ps1").write_text("fake\n", encoding="utf-8")
    (root / "venv").mkdir()
    (root / "venv" / "python.exe").write_text("fake\n", encoding="utf-8")
else:
    for child in list(root.iterdir()):
        if child.is_dir():
            shutil.rmtree(child)
        elif not (mode == "stray" and child.name == "stray.txt"):
            child.unlink()
    if mode == "stray":
        (root / "stray.txt").write_text("left behind\n", encoding="utf-8")
    elif mode != "keep_root":
        root.rmdir()
'''


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in [name for name in env if name.startswith("GIT_")]:
        del env[key]
    env.update(
        {
            "GIT_AUTHOR_NAME": "test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def run_git(cwd: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-c", "core.autocrlf=false", *args],
        cwd=str(cwd),
        env=git_env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return completed.stdout.strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


class Fixture:
    """A tiny repository that carries the real publication generator and a payload of three files."""

    def __init__(self, base: Path) -> None:
        self.repo = base / "source"
        generator = ROOT / "library" / "local_orchestration" / "plugin_publication.py"
        write_text(self.repo / "library" / "__init__.py", "")
        write_text(self.repo / "library" / "local_orchestration" / "__init__.py", "")
        shutil.copyfile(generator, self.repo / "library" / "local_orchestration" / "plugin_publication.py")
        write_text(self.repo / "README.md", "fixture\n")
        write_text(self.repo / "skills" / "x" / "SKILL.md", "skill\n")
        write_text(
            self.repo / ".claude-plugin" / "plugin.json",
            json.dumps(
                {
                    "name": "software-factory",
                    "version": "0.5.0",
                    "author": {"name": "Fixture"},
                    "payload": {
                        "schemaVersion": 1,
                        "trees": [".claude-plugin", "skills"],
                        "files": ["README.md"],
                        "excludedSegments": ["__pycache__", ".git"],
                        "excludedSuffixes": [".pyc"],
                    },
                },
                indent=2,
            )
            + "\n",
        )
        write_text(
            self.repo / ".claude-plugin" / "marketplace.json",
            json.dumps(
                {
                    "name": "software-factory",
                    "owner": {"name": "Fixture"},
                    "plugins": [
                        {
                            "name": "software-factory",
                            "version": "0.5.0",
                            "source": {"source": "url", "url": "https://example.invalid/x.git", "sha": ZEROS},
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
        )
        run_git(base, "init", "-q", "-b", "main", str(self.repo))
        run_git(self.repo, "add", "-A")
        run_git(self.repo, "commit", "-q", "-m", "fixture")
        self.candidate = run_git(self.repo, "rev-parse", "HEAD")
        # the 0.4.14 marketplace of this fixture: a commit off the candidate, on a side branch, that names the
        # candidate's own commit as its plugin source
        run_git(self.repo, "checkout", "-q", "-b", "old")
        write_text(
            self.repo / ".claude-plugin" / "marketplace.json",
            json.dumps(
                {
                    "name": "johnny-ai-skill",
                    "owner": {"name": "Fixture"},
                    "plugins": [
                        {
                            "name": "johnny-ai-skill",
                            "version": "0.4.14",
                            "source": {"source": "url", "url": str(self.repo), "sha": self.candidate},
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
        )
        run_git(self.repo, "commit", "-q", "-am", "the 0.4.14 marketplace")
        self.old_commit = run_git(self.repo, "rev-parse", "HEAD")
        run_git(self.repo, "checkout", "-q", "main")
        generated = base / "generated"
        run_git(base, "clone", "-q", "--no-hardlinks", str(self.repo), str(generated))
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "library.local_orchestration.plugin_publication",
                "--repo",
                ".",
                "--manifest",
                ".claude-plugin/plugin.json",
                "--marketplace",
                ".claude-plugin/marketplace.json",
                "--ref",
                lifecycle.PUBLICATION_REF,
            ],
            cwd=str(generated),
            env={**git_env(), "PYTHONUTF8": "1"},
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        found = re.search(r"^publication commit ([0-9a-f]{40})$", completed.stdout, re.MULTILINE)
        assert found is not None
        self.expected = found.group(1)


_FIXTURE_DIR: tempfile.TemporaryDirectory[str] | None = None
_FIXTURE: Fixture | None = None


def setUpModule() -> None:
    global _FIXTURE_DIR, _FIXTURE
    _FIXTURE_DIR = tempfile.TemporaryDirectory(prefix="jas77-fixture-")
    _FIXTURE = Fixture(Path(_FIXTURE_DIR.name))


def tearDownModule() -> None:
    if _FIXTURE_DIR is not None:
        _FIXTURE_DIR.cleanup()


def fixture() -> Fixture:
    assert _FIXTURE is not None
    return _FIXTURE


Report = list[dict[str, object]]


class LifecycleCase(unittest.TestCase):
    """A scratch directory, the fake CLIs, and a way to run the script and read its report."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="jas77-case-")
        self.addCleanup(self._tmp.cleanup)
        # resolved, because the script resolves its run root and a runner's temp path has an 8.3 short form
        self.tmp = Path(self._tmp.name).resolve()
        self.cli = self.tmp / "fake_cli.py"
        self.cli.write_text(FAKE_CLI, encoding="utf-8")
        self.level2 = self.tmp / "fake_level2.py"
        self.level2.write_text(FAKE_LEVEL2, encoding="utf-8")
        self.log = self.tmp / "calls.jsonl"
        self.level2_log = self.tmp / "level2.jsonl"
        self.runs = 0

    def launchers(self, mode: str = "ok") -> dict[str, list[str]]:
        return {
            host: [sys.executable, str(self.cli), host, str(self.log), mode, fixture().candidate]
            for host in ("claude", "codex")
        }

    def services(
        self, mode: str = "ok", level2_mode: str = "ok", environ: dict[str, str] | None = None
    ) -> lifecycle.Services:
        level2 = self.level2
        level2_log = self.level2_log
        return lifecycle.Services(
            launchers=self.launchers(mode),
            source_repo=fixture().repo,
            environ=environ,
            downloader=self.download,
            level2_install=lambda wrapper: [sys.executable, str(level2), "install", str(level2_log), level2_mode, str(wrapper)],
            level2_uninstall=lambda root: [sys.executable, str(level2), "uninstall", str(level2_log), level2_mode],
        )

    @staticmethod
    def download(url: str, destination: Path) -> None:
        destination.write_bytes(b"fake " + url.rsplit("/", 1)[-1].encode("ascii"))

    def run_script(
        self,
        steps: str,
        host: str = "both",
        mode: str = "ok",
        expected: str | None = None,
        services: lifecycle.Services | None = None,
        level2_mode: str = "ok",
    ) -> tuple[int, Report, Path]:
        self.runs += 1
        run_root = self.tmp / f"run{self.runs}"
        chosen = services or self.services(mode, level2_mode)
        digests = {name: sha256_hex(b"fake " + name.encode("ascii")) for name in lifecycle.LEVEL2_ASSETS}
        with mock.patch.object(lifecycle, "LEVEL2_ASSETS", digests), mock.patch.object(
            lifecycle, "OLD_MARKETPLACE_COMMIT", fixture().old_commit
        ), mock.patch.object(lifecycle, "OLD_PINNED_COMMIT", fixture().candidate):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = lifecycle.main(
                    [
                        "--candidate",
                        fixture().candidate,
                        "--expected-publication",
                        expected or fixture().expected,
                        "--host",
                        host,
                        "--steps",
                        steps,
                        "--run-root",
                        str(run_root),
                    ],
                    chosen,
                )
        report_file = run_root / "report.jsonl"
        lines = report_file.read_text(encoding="utf-8").splitlines() if report_file.exists() else []
        report: Report = [json.loads(line) for line in lines]
        return code, report, run_root

    def calls(self) -> list[dict[str, object]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    @staticmethod
    def verdicts(report: Report) -> dict[str, str]:
        return {f"{row['step']}/{row['host']}": str(row["verdict"]) for row in report}


def environment_of(call: dict[str, object]) -> dict[str, str]:
    raw = call["env"]
    assert isinstance(raw, dict)
    return {str(key): str(value) for key, value in raw.items()}


def evidence_of(row: dict[str, object]) -> list[str]:
    raw = row["evidence"]
    assert isinstance(raw, list)
    return [str(item) for item in raw]


def arguments_of(call: dict[str, object]) -> list[str]:
    raw = call["args"]
    assert isinstance(raw, list)
    return [str(item) for item in raw]


class NormalBehaviourTests(LifecycleCase):
    def test_fresh_issues_the_readmes_commands_with_the_steps_own_directory(self) -> None:
        code, report, run_root = self.run_script("build,fresh")
        self.assertEqual(code, 0, report)
        self.assertEqual(self.verdicts(report), {"build/none": "PASS", "fresh/claude": "PASS", "fresh/codex": "PASS"})
        marketplace = str(run_root / "build" / "marketplace")
        wanted = {
            "claude": [
                ["--version"],
                ["plugin", "marketplace", "add", marketplace],
                ["plugin", "install", "software-factory@software-factory", "--scope", "user"],
                ["plugin", "list", "--json"],
                ["plugin", "update", "software-factory@software-factory", "--scope", "user"],
                ["plugin", "list", "--json"],
            ],
            "codex": [
                ["--version"],
                ["plugin", "marketplace", "add", marketplace],
                ["plugin", "add", "software-factory@software-factory", "--json"],
                ["plugin", "list", "--marketplace", "software-factory", "--json"],
            ],
        }
        for host in ("claude", "codex"):
            mine = [call for call in self.calls() if call["host"] == host]
            self.assertEqual([arguments_of(call) for call in mine], wanted[host])
            step = run_root / f"fresh-{host}"
            variable = "CLAUDE_CONFIG_DIR" if host == "claude" else "CODEX_HOME"
            for call in mine:
                env = environment_of(call)
                self.assertEqual(env[variable], str(step))
                self.assertEqual(env["HOME"], str(step / "home"))
                self.assertEqual(env["USERPROFILE"], str(step / "home"))
                self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")
                self.assertEqual(env["DISABLE_AUTOUPDATER"], "1")
                self.assertEqual(Path(env["GIT_CONFIG_GLOBAL"]).read_text(encoding="utf-8"), "")
                self.assertEqual(Path(str(call["cwd"])).resolve(), step.resolve())

    def test_no_variable_outside_the_allow_list_reaches_a_host_cli(self) -> None:
        environ = {
            **os.environ,
            "ACCEPTANCE_SENTINEL": "leak",
            "CODEX_HOME": "/the/users/own",
            "GITHUB_TOKEN": "x",
            "ANTHROPIC_API_KEY": "leak",
            "OPENAI_API_KEY": "leak",
        }
        services = self.services(environ=environ)
        code, report, _ = self.run_script("build,fresh", services=services)
        self.assertEqual(code, 0, report)
        # pinned against the ticket's ten names, not against the constant the script itself reads
        self.assertEqual(lifecycle.ENV_ALLOW_LIST, TICKET_ENV_ALLOW_LIST)
        allowed = set(TICKET_ENV_ALLOW_LIST) | {
            "CLAUDE_CONFIG_DIR",
            "CODEX_HOME",
            "HOME",
            "USERPROFILE",
            "GIT_CONFIG_GLOBAL",
            "GIT_TERMINAL_PROMPT",
            "DISABLE_AUTOUPDATER",
        }
        for call in self.calls():
            names = {name.upper() for name in environment_of(call)}
            self.assertNotIn("ACCEPTANCE_SENTINEL", names)
            self.assertNotIn("GITHUB_TOKEN", names)
            self.assertNotIn("ANTHROPIC_API_KEY", names)
            self.assertNotIn("OPENAI_API_KEY", names)
            self.assertEqual(names - allowed - {"LC_CTYPE", "__PYVENV_LAUNCHER__"}, set(), call["args"])
            self.assertNotEqual(environment_of(call).get("CODEX_HOME"), "/the/users/own")

    def test_every_report_line_has_the_schema_and_no_address_or_credential(self) -> None:
        code, report, run_root = self.run_script("build,fresh")
        self.assertEqual(code, 0)
        text = (run_root / "report.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("maintainer@example.com", text)
        self.assertIn("<email>", text)
        for row in report:
            self.assertEqual(set(row), {"step", "host", "verdict", "commands", "evidence"})
            self.assertIn(row["verdict"], {"PASS", "FAIL", "NOT_SUPPORTED"})
            commands = row["commands"]
            assert isinstance(commands, list)
            for command in commands:
                assert isinstance(command, dict)
                self.assertTrue({"argv", "exit", "output"} <= set(command))

    def test_upgrade_installs_the_old_plugin_removes_it_and_lists_only_the_new_one(self) -> None:
        code, report, run_root = self.run_script("build,upgrade", host="claude")
        self.assertEqual(code, 0, report)
        arguments = [arguments_of(call) for call in self.calls()]
        self.assertIn(["plugin", "marketplace", "add", lifecycle.CLAUDE_OLD_MARKETPLACE_URL], arguments)
        self.assertIn(["plugin", "install", "johnny-ai-skill@johnny-ai-skill", "--scope", "user"], arguments)
        self.assertIn(["plugin", "uninstall", "johnny-ai-skill@johnny-ai-skill", "--scope", "user"], arguments)
        self.assertIn(["plugin", "marketplace", "remove", "johnny-ai-skill"], arguments)
        self.assertIn(["plugin", "marketplace", "add", str(run_root / "build" / "marketplace")], arguments)

    def test_the_upgrade_needs_the_commit_the_ticket_names(self) -> None:
        code, report, _ = self.run_script("build,upgrade", host="claude", mode="wrong_commit")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["upgrade/claude"], "FAIL")

    def test_codex_installs_0414_from_a_local_marketplace_written_byte_for_byte(self) -> None:
        code, report, run_root = self.run_script("build,upgrade", host="codex")
        self.assertEqual(code, 0, report)
        step = run_root / "upgrade-codex"
        local = step / "marketplace-0414"
        files = sorted(item.relative_to(local).as_posix() for item in local.rglob("*") if item.is_file())
        self.assertEqual(files, [".claude-plugin/marketplace.json"])
        stored = subprocess.run(
            ["git", "-C", str(fixture().repo), "cat-file", "blob", f"{fixture().old_commit}:.claude-plugin/marketplace.json"],
            capture_output=True,
            check=True,
            env=git_env(),
        ).stdout
        self.assertEqual((local / ".claude-plugin" / "marketplace.json").read_bytes(), stored)
        added = [arguments_of(call) for call in self.calls() if arguments_of(call)[:3] == ["plugin", "marketplace", "add"]]
        self.assertEqual(added[0], ["plugin", "marketplace", "add", str(local)])
        self.assertIn("installed from " + fixture().candidate, json.dumps(report[-1]["evidence"]))

    def test_codex_refusing_the_0414_install_is_a_fail(self) -> None:
        code, report, _ = self.run_script("build,upgrade", host="codex", mode="old_refused")
        self.assertEqual(code, 1)
        self.assertEqual(report[-1]["verdict"], "FAIL")
        self.assertIn("refused", json.dumps(report[-1]["evidence"]))

    def test_an_entry_that_does_not_say_it_is_enabled_is_not_enabled(self) -> None:
        code, report, _ = self.run_script("build,fresh", mode="flagless")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["fresh/claude"], "FAIL")
        self.assertEqual(self.verdicts(report)["fresh/codex"], "FAIL")
        self.assertIn("enabled=None", json.dumps(report[-1]["evidence"]))

    def test_a_disabled_entry_is_not_installed_and_enabled(self) -> None:
        code, report, _ = self.run_script("build,fresh", mode="disabled")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["fresh/claude"], "FAIL")
        self.assertEqual(self.verdicts(report)["fresh/codex"], "FAIL")
        self.assertIn("enabled=False", json.dumps(report[-1]["evidence"]))

    def test_uninstall_leaves_only_the_allow_listed_cache(self) -> None:
        code, report, _ = self.run_script("build,uninstall")
        self.assertEqual(code, 0, report)

    def test_recover_ends_with_exactly_one_listed_entry(self) -> None:
        code, report, _ = self.run_script("build,recover")
        self.assertEqual(code, 0, report)
        listed = [arguments_of(call) for call in self.calls() if arguments_of(call)[:2] == ["plugin", "list"]]
        self.assertEqual(len(listed), 2)


class RuleViolationTests(LifecycleCase):
    def refuse(self, **overrides: str) -> int:
        arguments = {
            "--candidate": fixture().candidate,
            "--expected-publication": fixture().expected,
            "--host": "both",
            "--steps": "build",
            "--run-root": str(self.tmp / "refused-run"),
        }
        arguments.update({f"--{key.replace('_', '-')}": value for key, value in overrides.items()})
        flat = [item for pair in arguments.items() for item in pair]
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            try:
                return lifecycle.main(flat, self.services())
            except SystemExit as stop:
                return int(str(stop.code))

    def test_a_run_root_that_is_not_empty_is_refused(self) -> None:
        occupied = self.tmp / "occupied"
        occupied.mkdir()
        (occupied / "leftover.txt").write_text("x", encoding="utf-8")
        self.assertEqual(self.refuse(run_root=str(occupied)), 2)
        self.assertEqual(sorted(item.name for item in occupied.iterdir()), ["leftover.txt"])

    def test_an_empty_existing_run_root_is_accepted(self) -> None:
        empty = self.tmp / "empty"
        empty.mkdir()
        self.assertEqual(self.refuse(run_root=str(empty)), 0)

    def test_an_empty_run_root_path_is_refused(self) -> None:
        self.assertEqual(self.refuse(run_root=""), 2)
        self.assertEqual(self.refuse(run_root="   "), 2)

    def test_a_run_root_inside_a_git_work_tree_is_refused(self) -> None:
        work_tree = self.tmp / "work-tree"
        (work_tree / ".git").mkdir(parents=True)
        self.assertEqual(self.refuse(run_root=str(work_tree / "run")), 2)
        self.assertFalse((work_tree / "run").exists())

    def test_a_run_root_inside_a_configuration_directory_of_the_user_is_refused(self) -> None:
        home = self.tmp / "home"
        environ = {**os.environ, "USERPROFILE": str(home), "HOME": str(home)}
        for name in (".claude", ".codex"):
            with self.assertRaises(lifecycle.Refusal):
                lifecycle.check_run_root(str(home / name / "run"), environ)
            self.assertFalse((home / name).exists())

    def test_an_unknown_step_or_host_is_refused(self) -> None:
        self.assertEqual(self.refuse(steps="build,teleport"), 2)
        self.assertEqual(self.refuse(host="gemini"), 2)
        self.assertEqual(self.refuse(host="Claude"), 2)

    def test_empty_and_malformed_step_lists_are_refused(self) -> None:
        for steps in ("", ",", "build,", "build,,fresh", " build", "build,build"):
            self.assertEqual(self.refuse(steps=steps), 2, repr(steps))

    def test_no_step_runs_without_build_first(self) -> None:
        self.assertEqual(self.refuse(steps="fresh"), 2)
        self.assertEqual(self.refuse(steps="fresh,build"), 2)

    def test_the_codex_only_steps_refuse_the_claude_host(self) -> None:
        self.assertEqual(self.refuse(host="claude", steps="build,codex-ref"), 2)
        self.assertEqual(self.refuse(host="claude", steps="build,codex-files"), 2)

    def test_commit_ids_are_exactly_forty_lower_case_hex(self) -> None:
        good = fixture().candidate
        for bad in (good[:39], good + "0", good.upper(), good[:39] + "g", good + "\n", "", "HEAD"):
            self.assertEqual(self.refuse(candidate=bad), 2, repr(bad))
            self.assertEqual(self.refuse(expected_publication=bad), 2, repr(bad))

    def test_a_regenerated_commit_other_than_the_expected_one_fails_build(self) -> None:
        wrong = ("1" if fixture().expected[0] != "1" else "2") + fixture().expected[1:]
        code, report, _ = self.run_script("build,fresh", expected=wrong)
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["build/none"], "FAIL")
        self.assertEqual(self.verdicts(report)["fresh/claude"], "FAIL")
        self.assertIn("not the expected", json.dumps(report[0]["evidence"]))
        self.assertEqual(self.calls(), [])


class ExternalFailureTests(LifecycleCase):
    def test_a_cli_that_exits_non_zero_fails_the_step_and_the_script(self) -> None:
        code, report, _ = self.run_script("build,fresh", mode="fail_install")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["fresh/claude"], "FAIL")
        self.assertEqual(self.verdicts(report)["fresh/codex"], "FAIL")

    def test_a_missing_subcommand_is_not_supported_and_the_script_exits_non_zero(self) -> None:
        code, report, _ = self.run_script("build,fresh", host="claude", mode="no_list_json")
        self.assertEqual(self.verdicts(report)["fresh/claude"], "NOT_SUPPORTED")
        self.assertNotEqual(code, 0)

    def test_the_three_verdicts_stay_distinct_in_one_run(self) -> None:
        code, report, _ = self.run_script("build,fresh,codex-ref", host="codex", mode="no_file_url")
        self.assertEqual(self.verdicts(report), {"build/none": "PASS", "fresh/codex": "PASS", "codex-ref/codex": "NOT_SUPPORTED"})
        self.assertEqual(code, 1)

    def test_recover_fails_when_the_broken_install_exits_zero(self) -> None:
        code, report, _ = self.run_script("build,recover", mode="lenient")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["recover/claude"], "FAIL")
        self.assertEqual(self.verdicts(report)["recover/codex"], "FAIL")
        self.assertIn("exited 0", json.dumps(report[-1]["evidence"]))

    def test_a_cli_that_cannot_be_started_is_a_fail_with_the_reason_not_a_traceback(self) -> None:
        missing = str(self.tmp / "no-such-cli")
        services = self.services()
        services.launchers = {"claude": [missing], "codex": [missing]}
        code, report, _ = self.run_script("build,fresh", services=services)
        self.assertEqual(code, 1)
        row = report[-1]
        self.assertEqual(row["verdict"], "FAIL")
        text = json.dumps(row)
        self.assertIn("cannot start", text)
        self.assertNotIn("Traceback", text)

    def test_a_step_that_raises_unexpectedly_is_a_fail_not_a_crash(self) -> None:
        def explode(ctx: lifecycle.Context) -> None:
            raise KeyError("boom")

        steps = dict(lifecycle.STEP_FUNCTIONS)
        steps["fresh"] = explode
        with mock.patch.object(lifecycle, "STEP_FUNCTIONS", steps):
            code, report, _ = self.run_script("build,fresh")
        self.assertEqual(code, 1)
        self.assertIn("unexpected KeyError", json.dumps(report[-1]["evidence"]))

    def test_a_failed_build_stops_every_later_step(self) -> None:
        wrong = ("1" if fixture().expected[0] != "1" else "2") + fixture().expected[1:]
        _, report, _ = self.run_script("build,fresh,uninstall,level2", expected=wrong)
        self.assertEqual({row["verdict"] for row in report}, {"FAIL"})
        self.assertEqual(self.calls(), [])


class ResidueTests(LifecycleCase):
    def test_the_name_matches_as_a_whole_name_and_never_as_a_prefix_or_suffix(self) -> None:
        for text in (
            "software-factory",
            "plugins/software-factory",
            "plugins/software-factory/0.5.0",
            "software-factory.json",
            '"software-factory@software-factory"',
            "a software-factory b",
        ):
            self.assertTrue(lifecycle.names_whole(text), text)
        for text in (
            "software-factory-plugin",
            "my-software-factory",
            "software-factory2",
            "software_factory",
            "xsoftware-factory",
            "software-factoryx",
            "",
        ):
            self.assertFalse(lifecycle.names_whole(text), text)

    def test_a_leftover_line_outside_the_allow_list_fails_the_uninstall(self) -> None:
        code, report, _ = self.run_script("build,uninstall", mode="leftover")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["uninstall/claude"], "FAIL")
        self.assertIn("settings.json", json.dumps(report[1]["evidence"]))

    def test_names_that_only_start_or_end_like_the_plugin_are_not_residue(self) -> None:
        code, report, _ = self.run_script("build,uninstall", mode="prefix_only")
        self.assertEqual(code, 0, report)

    def test_the_scan_honours_each_kind_of_allow_entry(self) -> None:
        step = self.tmp / "scan"
        write_text(step / "plugins" / "cache" / "software-factory" / "a.json", '{"n": "software-factory"}\n')
        write_text(step / "settings.json", '{"n": "software-factory"}\n')
        (step / "empty" / "software-factory").mkdir(parents=True)
        entries = [
            lifecycle.AllowEntry("path", "claude", "plugins/cache/software-factory", "r"),
            lifecycle.AllowEntry("emptydir", "claude", "empty/software-factory", "r"),
        ]
        self.assertEqual(lifecycle.scan_residue(step, "claude", entries), ["line settings.json:1"])
        entries.append(lifecycle.AllowEntry("line", "claude", "settings.json", "r"))
        self.assertEqual(lifecycle.scan_residue(step, "claude", entries), [])
        self.assertEqual(len(lifecycle.scan_residue(step, "codex", entries)), 5)
        write_text(step / "empty" / "software-factory" / "file.txt", "x")
        self.assertIn("path empty/software-factory", lifecycle.scan_residue(step, "claude", entries))
        # an allow-listed path is a whole path component: a sibling that only starts like it is residue
        write_text(step / "plugins" / "cache" / "software-factory.old" / "a.json", '{"n": "software-factory"}\n')
        self.assertIn("path plugins/cache/software-factory.old", lifecycle.scan_residue(step, "claude", entries))

    def test_a_malformed_allow_list_entry_is_a_fail_closed_error(self) -> None:
        with self.assertRaises(lifecycle.StepFail):
            lifecycle.parse_allowlist("```lifecycle-allowlist\npath | claude | only three fields\n```\n")
        with self.assertRaises(lifecycle.StepFail):
            lifecycle.parse_allowlist("```lifecycle-allowlist\nweird | claude | a | b\n```\n")
        with self.assertRaises(lifecycle.StepFail):
            lifecycle.parse_allowlist("```lifecycle-allowlist\npath | claude | a | b\n")

    def test_the_real_allow_list_names_a_reason_for_every_entry(self) -> None:
        entries = lifecycle.load_allowlist(README)
        self.assertGreaterEqual(len(entries), 2)
        for entry in entries:
            self.assertGreater(len(entry.reason), 20, entry)


class CodexStepTests(LifecycleCase):
    def test_codex_ref_passes_when_the_installed_tree_is_the_pinned_commits_tree(self) -> None:
        code, report, _ = self.run_script("build,codex-ref", host="codex")
        self.assertEqual(code, 0, report)
        self.assertIn("honoured `sha`", json.dumps(report[-1]["evidence"]))
        added = [arguments_of(call) for call in self.calls() if arguments_of(call)[:3] == ["plugin", "marketplace", "add"]]
        self.assertTrue(added[0][3].startswith("file:///") or added[0][3].startswith("file://"), added)
        self.assertEqual(added[0][4:], ["--ref", "marketplace"])

    def test_codex_ref_fails_when_the_default_branch_tip_was_installed(self) -> None:
        code, report, _ = self.run_script("build,codex-ref", host="codex", mode="ignore_sha")
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["codex-ref/codex"], "FAIL")
        self.assertIn("`sha` was ignored", json.dumps(report[-1]["evidence"]))

    def test_codex_ref_refusing_the_file_url_is_not_supported_with_the_output_recorded(self) -> None:
        code, report, _ = self.run_script("build,codex-ref", host="codex", mode="no_file_url")
        self.assertEqual(code, 1)
        row = report[-1]
        self.assertEqual(row["verdict"], "NOT_SUPPORTED")
        self.assertIn("invalid marketplace source format", json.dumps(row))

    def test_codex_files_records_one_outcome_per_marketplace(self) -> None:
        code, report, _ = self.run_script("build,codex-files", host="codex")
        self.assertEqual(code, 0, report)
        evidence = evidence_of(report[-1])
        for case, version in (("both", "0.5.1"), ("claude-only", "0.5.0"), ("agents-only", "0.5.0")):
            line = [item for item in evidence if item.startswith(case + ":")]
            self.assertEqual(len(line), 1, evidence)
            self.assertIn("plugin add exit 0", line[0])
            self.assertIn(f"listed version {version}", line[0])

    def test_codex_files_fails_when_a_command_cannot_be_started(self) -> None:
        services = self.services()
        services.launchers = {"codex": [str(self.tmp / "no-such-cli")]}
        code, report, _ = self.run_script("build,codex-files", host="codex", services=services)
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["codex-files/codex"], "FAIL")


class Level2Tests(LifecycleCase):
    def test_the_install_prompt_is_answered_only_into_an_empty_root_and_the_root_is_clean_after_uninstall(self) -> None:
        code, report, run_root = self.run_script("build,level2")
        self.assertEqual(code, 0, report)
        answers = [json.loads(line) for line in self.level2_log.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(answers), 1)
        entry = answers[0]
        step = run_root / "level2"
        self.assertEqual(entry["answer"], "INSTALL\n")
        self.assertEqual(entry["root_entries"], [])
        self.assertFalse(entry["has_userprofile"])
        self.assertEqual(Path(entry["cwd"]).resolve(), step.resolve())
        self.assertEqual(Path(entry["wrapper"]), step / "download" / lifecycle.LEVEL2_WRAPPER)
        self.assertTrue(Path(entry["wrapper"]).is_absolute())
        self.assertEqual(Path(entry["home"]), step / "home")
        allowed = set(TICKET_ENV_ALLOW_LIST) | {"HOME", "GIT_CONFIG_GLOBAL", "GIT_TERMINAL_PROMPT", "DISABLE_AUTOUPDATER", "JOHNNY_ROOT"}
        self.assertEqual(set(entry["env_names"]) - allowed - {"LC_CTYPE", "__PYVENV_LAUNCHER__"}, set())
        self.assertTrue((run_root / "level2" / "download" / lifecycle.LEVEL2_BUNDLE).is_file())
        self.assertFalse((run_root / "level2" / "root").exists())

    def test_a_download_with_the_wrong_sha256_fails_before_anything_runs(self) -> None:
        def wrong(url: str, destination: Path) -> None:
            destination.write_bytes(b"tampered")

        services = self.services()
        services.downloader = wrong
        code, report, _ = self.run_script("build,level2", services=services)
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(report)["level2/none"], "FAIL")
        self.assertIn("not the approved", json.dumps(report[-1]["evidence"]))
        self.assertFalse(self.level2_log.exists())

    def test_a_file_left_in_the_root_after_uninstall_is_a_fail(self) -> None:
        code, report, _ = self.run_script("build,level2", level2_mode="stray")
        self.assertEqual(code, 1)
        self.assertIn("stray.txt", json.dumps(report[-1]["evidence"]))

    def test_the_default_argv_shapes_name_the_wrapper_and_the_launcher(self) -> None:
        argv = lifecycle.level2_install_argv(Path("x") / lifecycle.LEVEL2_WRAPPER)
        self.assertEqual(argv[1], "/c")
        self.assertTrue(argv[2].endswith(lifecycle.LEVEL2_WRAPPER))
        removal = lifecycle.level2_uninstall_argv(Path("root"))
        self.assertEqual(removal[-1], "uninstall")
        self.assertTrue(removal[-2].endswith("johnny-router.ps1"))

    @unittest.skipUnless(sys.platform == "win32", "the wrapper is a .cmd file and needs cmd.exe")
    def test_a_cmd_wrapper_started_by_the_default_argv_reads_the_answer_from_standard_input(self) -> None:
        wrapper = self.tmp / "answer.cmd"
        wrapper.write_text("@echo off\r\nset /p ANSWER=\r\necho answer=%ANSWER%\r\n", encoding="utf-8", newline="")
        record = lifecycle.run_command(
            lifecycle.level2_install_argv(wrapper),
            cwd=self.tmp,
            env=lifecycle.build_environment(self.tmp, {}),
            stdin=lifecycle.LEVEL2_CONFIRMATION,
            timeout=60,
        )
        self.assertEqual(record.exit_code, 0, record)
        self.assertIn("answer=INSTALL", record.stdout)


class RedactionTests(unittest.TestCase):
    def test_addresses_and_credential_shapes_never_reach_a_report(self) -> None:
        text = (
            "mail me at person@example.com; token ghp_abcdefghijklmnopqrstuvwxyz0123456789; "
            'Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456 and "access_token": "s3cr3t"'
        )
        cleaned = lifecycle.redact(text)
        for leaked in ("person@example.com", "ghp_abcdefghij", "abcdefghijklmnopqrstuvwxyz123456", "s3cr3t"):
            self.assertNotIn(leaked, cleaned)

    def test_a_plugin_id_is_not_an_address(self) -> None:
        self.assertEqual(lifecycle.redact("software-factory@software-factory"), "software-factory@software-factory")

    def test_a_command_that_times_out_is_a_record_with_a_reason(self) -> None:
        record = lifecycle.run_command(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            cwd=Path(tempfile.gettempdir()),
            env=dict(os.environ),
            timeout=1,
        )
        self.assertIsNone(record.exit_code)
        self.assertIn("timeout", str(record.error))


def top_level_block(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == f"{key}:":
            block: list[str] = []
            for follower in lines[index + 1 :]:
                if follower and not follower.startswith((" ", "#")):
                    break
                block.append(follower)
            return block
    return []


def key_names(block: list[str], indent: int) -> list[str]:
    pattern = re.compile(r"^" + " " * indent + r"([A-Za-z_][\w-]*):")
    return [match.group(1) for match in (pattern.match(line) for line in block) if match is not None]


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_the_only_trigger_is_workflow_dispatch_with_the_two_inputs(self) -> None:
        on = top_level_block(self.text, "on")
        self.assertEqual(key_names(on, 2), ["workflow_dispatch"])
        self.assertEqual(key_names(on, 6), ["candidate", "expected_publication"])
        self.assertIsNone(re.search(r"^\s*(push|pull_request\w*|schedule|workflow_run)\s*:", self.text, re.MULTILINE))

    def test_the_job_runs_on_windows_for_at_most_sixty_minutes_with_read_only_contents(self) -> None:
        self.assertEqual(self.text.count("runs-on:"), 1)
        self.assertIn("runs-on: windows-latest", self.text)
        self.assertIn("timeout-minutes: 60", self.text)
        self.assertEqual([line for line in top_level_block(self.text, "permissions") if line.strip()], ["  contents: read"])
        self.assertEqual(self.text.count("permissions:"), 1)

    def test_it_holds_no_secret_token_or_oidc_reference(self) -> None:
        for forbidden in ("secrets.", "GITHUB_TOKEN", "github.token", "id-token"):
            self.assertNotIn(forbidden, self.text)
        self.assertIsNone(re.search(r"(?i)\blogin\b", self.text))

    def test_every_action_is_a_full_sha_with_its_version_in_a_comment(self) -> None:
        lines = self.text.splitlines()
        uses = [(index, line) for index, line in enumerate(lines) if re.match(r"^\s*-?\s*uses:", line)]
        self.assertGreaterEqual(len(uses), 3)
        for index, line in uses:
            self.assertRegex(line, r"uses:\s+[\w.-]+/[\w.-]+@[0-9a-f]{40}\s*$")
            self.assertRegex(lines[index - 1], r"^\s*#\s+[\w./-]+\s+v\d+\.\d+\.\d+\s*$")

    def test_the_checkout_is_the_one_of_ci_yml_without_persisted_credentials(self) -> None:
        pattern = re.compile(r"actions/checkout@[0-9a-f]{40}")
        mine = pattern.search(self.text)
        theirs = pattern.search(CI_WORKFLOW.read_text(encoding="utf-8"))
        assert mine is not None and theirs is not None
        self.assertEqual(mine.group(0), theirs.group(0))
        block = self.text[mine.end() : mine.end() + 120]
        self.assertIn("fetch-depth: 0", block)
        self.assertIn("persist-credentials: false", block)

    def test_the_inputs_reach_the_script_through_the_environment_and_the_command_is_the_ticket_s(self) -> None:
        self.assertIn("CANDIDATE: ${{ inputs.candidate }}", self.text)
        self.assertIn("EXPECTED_PUBLICATION: ${{ inputs.expected_publication }}", self.text)
        for line in self.text.splitlines():
            if line.lstrip().startswith(("python ", "run:")) or "ci/acceptance/lifecycle.py" in line:
                self.assertNotIn("${{", line)
        self.assertIn(
            'python ci/acceptance/lifecycle.py --candidate "$CANDIDATE" --expected-publication "$EXPECTED_PUBLICATION" '
            '--host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root "$RUNNER_TEMP/acceptance"',
            self.text,
        )
        self.assertIn("report.jsonl", self.text)

    def test_the_host_cli_versions_equal_the_ones_in_the_readme(self) -> None:
        readme = README.read_text(encoding="utf-8")
        for package in ("@anthropic-ai/claude-code", "@openai/codex"):
            workflow_version = re.search(re.escape(package) + r"@([\w.-]+)", self.text)
            readme_version = re.search(re.escape(package) + r"@([\w.-]+)", readme)
            assert workflow_version is not None and readme_version is not None
            self.assertEqual(workflow_version.group(1), readme_version.group(1))
        table = re.findall(r"^\| (claude|codex) \| ([\w.-]+) \|", readme, re.MULTILINE)
        self.assertEqual(sorted(name for name, _ in table), ["claude", "codex"])


class ReadmeTests(unittest.TestCase):
    def test_the_level2_allow_list_quotes_section_six_of_the_repository_readme(self) -> None:
        readme = README.read_text(encoding="utf-8")
        section = REPOSITORY_README.read_text(encoding="utf-8").split("## 6. ", 1)[1].split("\n## 7.", 1)[0]
        for entry, quote in lifecycle.parse_level2_allowlist(readme):
            self.assertIn(quote, section, entry)
        for quoted in ("全部移除後，再清掉安裝日誌與已空的根目錄", "下載來的安裝檔與 zip，它們在下載資料夾，不在根目錄"):
            self.assertIn(quoted, section)
            self.assertIn(quoted, readme)

    def test_the_four_conditions_and_the_trigger_command_are_written_down(self) -> None:
        readme = README.read_text(encoding="utf-8")
        for number in ("| 1 |", "| 2 |", "| 3 |", "| 4 |"):
            self.assertIn(number, readme)
        self.assertIn("gh workflow run acceptance.yml --ref main -f candidate=", readme)

    def test_the_readme_commands_the_script_issues_are_the_readmes_own(self) -> None:
        shipped = REPOSITORY_README.read_text(encoding="utf-8")
        plugin, market = lifecycle.PLUGIN_ID, lifecycle.MARKETPLACE_NAME
        old_plugin, old_market = lifecycle.OLD_PLUGIN_ID, lifecycle.OLD_MARKETPLACE_NAME
        for host, args in (
            ("claude", lifecycle.install_args("claude", plugin)),
            ("claude", lifecycle.update_args(plugin)),
            ("claude", lifecycle.uninstall_args("claude", plugin)),
            ("claude", lifecycle.marketplace_remove_args("claude", market)),
            ("codex", lifecycle.install_args("codex", plugin)),
            ("codex", lifecycle.list_args("codex")),
            ("codex", lifecycle.uninstall_args("codex", plugin)),
            ("codex", lifecycle.marketplace_remove_args("codex", market)),
            ("claude", lifecycle.uninstall_args("claude", old_plugin)),
            ("claude", lifecycle.marketplace_remove_args("claude", old_market)),
            ("codex", lifecycle.uninstall_args("codex", old_plugin)),
            ("codex", lifecycle.marketplace_remove_args("codex", old_market)),
        ):
            self.assertIn(f"{host} {' '.join(args)}", shipped)


if __name__ == "__main__":
    unittest.main()
