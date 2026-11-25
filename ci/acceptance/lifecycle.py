"""The 0.5.0 install lifecycle, run in isolated directories."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

ENV_ALLOW_LIST: tuple[str, ...] = (
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
HOST_TIMEOUT_SECONDS = 600
VERSION_TIMEOUT_SECONDS = 60
EXCERPT_CHARACTERS = 600


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_SUPPORTED = "NOT_SUPPORTED"


@dataclass(frozen=True)
class CommandRecord:
    argv: tuple[str, ...]
    exit_code: int | None
    stdout: str
    stderr: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.error is None

    @property
    def output(self) -> str:
        return (self.stdout + self.stderr).strip()


_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_TOKEN_SHAPES = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}"),
)
_SECRET_FIELD = re.compile(
    r'(?i)("?(?:access_?token|refresh_?token|id_?token|api_?key|secret|password|authorization)"?\s*[:=]\s*)'
    r'("[^"]*"|\S+)'
)


def redact(text: str) -> str:
    """Remove e-mail addresses and credential shapes before text enters a report."""

    text = _EMAIL.sub("<email>", text)
    for shape in _TOKEN_SHAPES:
        text = shape.sub("<token>", text)
    return _SECRET_FIELD.sub(lambda match: match.group(1) + '"<secret>"', text)


def excerpt(text: str, limit: int = EXCERPT_CHARACTERS) -> str:
    text = redact(text.strip())
    if len(text) <= limit:
        return text
    return text[:limit] + "...[+" + str(len(text) - limit) + " chars]"


def build_environment(
    step_dir: Path,
    extra: Mapping[str, str],
    source: Mapping[str, str] | None = None,
    omit: Sequence[str] = (),
) -> dict[str, str]:
    """The environment of a host CLI: an allow-list, the step's home, and the step's own variables."""

    inherited = os.environ if source is None else source
    upper = {key.upper(): value for key, value in inherited.items()}
    environment = {name: upper[name] for name in ENV_ALLOW_LIST if name in upper}
    home = step_dir / "home"
    home.mkdir(parents=True, exist_ok=True)
    git_config = home / "empty.gitconfig"
    git_config.write_text("", encoding="utf-8")
    environment["HOME"] = str(home)
    environment["USERPROFILE"] = str(home)
    environment["GIT_CONFIG_GLOBAL"] = str(git_config)
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["DISABLE_AUTOUPDATER"] = "1"
    environment.update(extra)
    for name in omit:
        environment.pop(name, None)
    return environment


def run_command(
    argv: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    stdin: str | None = None,
    timeout: int = HOST_TIMEOUT_SECONDS,
) -> CommandRecord:
    """Run one command. A command that cannot start, or times out, is a record with a reason."""

    command = tuple(argv)
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd),
            env=dict(env),
            input=stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return CommandRecord(command, None, "", "", f"timeout after {error.timeout} s")
    except (OSError, ValueError) as error:
        return CommandRecord(command, None, "", "", f"cannot start: {type(error).__name__}: {error}")
    return CommandRecord(command, completed.returncode, completed.stdout or "", completed.stderr or "")


def resolve_executable(name: str, env: Mapping[str, str]) -> str | None:
    return shutil.which(name, path=env.get("PATH"))


@dataclass
class StepLog:
    commands: list[CommandRecord] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def note(self, line: str) -> None:
        self.evidence.append(line)




# --------------------------------------------------------------------------- #
# constants named by the ticket
# --------------------------------------------------------------------------- #

SOURCE_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VERSION = "0.5.0"
PLUGIN_NAME = "software-factory"
MARKETPLACE_NAME = "software-factory"
PLUGIN_ID = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
OLD_PLUGIN_NAME = "johnny-ai-skill"
OLD_PLUGIN_ID = "johnny-ai-skill@johnny-ai-skill"
OLD_MARKETPLACE_NAME = "johnny-ai-skill"
OLD_VERSION = "0.4.14"
OLD_PINNED_COMMIT = "0b3afd3645946f97662c336f0e6ac0dcae502e69"
CLAUDE_OLD_MARKETPLACE_URL = (
    "https://raw.githubusercontent.com/johnnyliu365-sys/Software-Factory/"
    "01b810f096b1201005d26922e2c8a474bdd5a0a0/.claude-plugin/marketplace.json"
)
CODEX_OLD_MARKETPLACE_SOURCE = "johnnyliu365-sys/Johnny_AI_Skill_publication"
PUBLICATION_REF = "refs/heads/publication-0.5.0"
LEVEL2_RELEASE_URL = "https://github.com/johnnyliu365-sys/Software-Factory/releases/download/v0.4.9/"
LEVEL2_ASSETS: Mapping[str, str] = {
    "johnny-ai-skill-0.4.9.zip": "2365b6f70a06f00ae0aed008371f7cc0b5afd0cb148a77e7476416bf25854aef",
    "johnny-install.cmd": "906b067238f05841ba87b5c59d88d0a8a5499821d8ebc660df9cee17296f532b",
}
LEVEL2_BUNDLE = "johnny-ai-skill-0.4.9.zip"
LEVEL2_WRAPPER = "johnny-install.cmd"
LEVEL2_CONFIRMATION = "INSTALL\n"

STEP_NAMES: tuple[str, ...] = (
    "build",
    "fresh",
    "upgrade",
    "uninstall",
    "recover",
    "level2",
    "codex-ref",
    "codex-files",
)
NO_HOST_STEPS = ("build", "level2")
CODEX_ONLY_STEPS = ("codex-ref", "codex-files")
HOST_NAMES = ("claude", "codex")
HOST_CHOICES = ("claude", "codex", "both")
HOST_VARIABLE = {"claude": "CLAUDE_CONFIG_DIR", "codex": "CODEX_HOME"}

_FULL_SHA = re.compile(r"[0-9a-f]{40}")
_MISSING_COMMAND = re.compile(
    r"(?i)unknown (?:command|option|subcommand)|unrecognized (?:subcommand|option|command)"
    r"|unexpected argument|invalid subcommand|no such (?:sub)?command|did you mean"
)


class Refusal(Exception):
    """The arguments are refused before any step runs."""


class StepFail(Exception):
    """The step ended FAIL for the stated reason."""


class StepNotSupported(Exception):
    """The host CLI lacks a command, or refuses a form the step needs."""


# --------------------------------------------------------------------------- #
# arguments
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Plan:
    candidate: str
    expected_publication: str
    host: str
    steps: tuple[str, ...]
    run_root: Path


def require_full_sha(label: str, value: str) -> str:
    if _FULL_SHA.fullmatch(value) is None:
        raise Refusal(f"{label} must be 40 lower-case hexadecimal characters, exactly")
    return value


def _inside_any(path: Path, parents: Sequence[Path]) -> bool:
    for parent in parents:
        try:
            path.relative_to(parent)
        except ValueError:
            continue
        return True
    return False


def user_owned_directories(environ: Mapping[str, str] | None = None) -> list[Path]:
    source = os.environ if environ is None else environ
    home = Path(source.get("USERPROFILE") or source.get("HOME") or str(Path.home()))
    owned = [home / ".claude", home / ".codex", home / ".config" / "claude", home / ".config" / "codex"]
    local = source.get("LOCALAPPDATA")
    if local:
        owned.append(Path(local) / "JohnnyRouter")
    return [item.resolve() for item in owned]


def check_run_root(text: str, environ: Mapping[str, str] | None = None) -> Path:
    if text.strip() == "":
        raise Refusal("the run root is empty")
    root = Path(text).resolve()
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            raise Refusal(f"the run root is inside a Git work tree: {candidate}")
    if _inside_any(root, user_owned_directories(environ)):
        raise Refusal("the run root is inside a configuration directory of the user")
    if root.exists():
        if not root.is_dir():
            raise Refusal("the run root is not a directory")
        if any(root.iterdir()):
            raise Refusal("the run root is not empty")
    return root


def validate_plan(
    candidate: str,
    expected_publication: str,
    host: str,
    steps_text: str,
    run_root_text: str,
    environ: Mapping[str, str] | None = None,
) -> Plan:
    require_full_sha("--candidate", candidate)
    require_full_sha("--expected-publication", expected_publication)
    if host not in HOST_CHOICES:
        raise Refusal(f"--host must be one of {', '.join(HOST_CHOICES)}")
    if steps_text == "":
        raise Refusal("--steps is empty")
    steps = tuple(steps_text.split(","))
    for name in steps:
        if name not in STEP_NAMES:
            raise Refusal(f"unknown step {name!r}")
    if len(set(steps)) != len(steps):
        raise Refusal("a step is named twice")
    if steps[0] != "build":
        raise Refusal("no step runs without build first in the same run")
    if host == "claude" and any(name in CODEX_ONLY_STEPS for name in steps):
        raise Refusal("codex-ref and codex-files run for codex only")
    return Plan(candidate, expected_publication, host, steps, check_run_root(run_root_text, environ))


def hosts_for(step: str, host: str) -> tuple[str, ...]:
    """The hosts a step runs for. build and level2 run once, with host none."""

    if step in NO_HOST_STEPS:
        return ("none",)
    if step in CODEX_ONLY_STEPS:
        return ("codex",)
    return HOST_NAMES if host == "both" else (host,)


# --------------------------------------------------------------------------- #
# services and the step context
# --------------------------------------------------------------------------- #


def download_to(url: str, destination: Path) -> None:
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": "software-factory-acceptance"})
    with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310 - fixed https URLs
        destination.write_bytes(response.read())


def level2_install_argv(wrapper: Path) -> list[str]:
    return [os.environ.get("COMSPEC", "cmd.exe"), "/c", str(wrapper)]


def level2_uninstall_argv(root: Path) -> list[str]:
    launcher = root / "launcher" / "johnny-router.ps1"
    return ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher), "uninstall"]


@dataclass
class Services:
    """What a run depends on from outside. A test replaces these; a real run keeps the defaults."""

    launchers: Mapping[str, Sequence[str]] = field(default_factory=dict)
    source_repo: Path = SOURCE_ROOT
    environ: Mapping[str, str] | None = None
    downloader: Callable[[str, Path], None] = download_to
    level2_install: Callable[[Path], list[str]] = level2_install_argv
    level2_uninstall: Callable[[Path], list[str]] = level2_uninstall_argv
    readme: Path = SOURCE_ROOT / "ci" / "acceptance" / "README.md"
    host_timeout: int = HOST_TIMEOUT_SECONDS


@dataclass
class Shared:
    """What `build` hands to the later steps of the same run."""

    repo: Path | None = None
    marketplace: Path | None = None
    package: Path | None = None
    publication: str | None = None


@dataclass
class Context:
    plan: Plan
    services: Services
    step: str
    host: str
    step_dir: Path
    log: StepLog
    shared: Shared

    def environment(self, extra: Mapping[str, str] | None = None, omit: Sequence[str] = ()) -> dict[str, str]:
        return build_environment(self.step_dir, extra or {}, self.services.environ, omit)

    def local_marketplace(self) -> Path:
        if self.shared.marketplace is None:
            raise StepFail("no local marketplace: build did not pass in this run")
        return self.shared.marketplace


class HostSession:
    """One host CLI, with the step directory as its configuration directory."""

    def __init__(self, ctx: Context, host: str, step_dir: Path | None = None) -> None:
        self.ctx = ctx
        self.host = host
        self.step_dir = step_dir or ctx.step_dir
        self.env = build_environment(
            self.step_dir, {HOST_VARIABLE[host]: str(self.step_dir)}, ctx.services.environ
        )
        injected = ctx.services.launchers.get(host)
        if injected is not None:
            self.launcher: list[str] | None = list(injected)
        else:
            found = resolve_executable(host, self.env)
            self.launcher = None if found is None else [found]

    def run(self, *args: str, timeout: int | None = None) -> CommandRecord:
        if self.launcher is None:
            record = CommandRecord(
                (self.host, *args), None, "", "", f"cannot start: {self.host} is not on PATH"
            )
        else:
            record = run_command(
                [*self.launcher, *args],
                cwd=self.step_dir,
                env=self.env,
                timeout=timeout or self.ctx.services.host_timeout,
            )
        self.ctx.log.commands.append(record)
        return record

    def version(self) -> CommandRecord:
        return self.run("--version", timeout=VERSION_TIMEOUT_SECONDS)


def is_missing_command(record: CommandRecord) -> bool:
    return record.exit_code not in (0, None) and _MISSING_COMMAND.search(record.output) is not None


# --------------------------------------------------------------------------- #
# commands of the README, by host
# --------------------------------------------------------------------------- #


def marketplace_add_args(host: str, source: str, ref: str | None = None) -> tuple[str, ...]:
    args = ["plugin", "marketplace", "add", source]
    if ref is not None:
        args += ["--ref", ref]
    return tuple(args)


def install_args(host: str, plugin_id: str) -> tuple[str, ...]:
    if host == "claude":
        return ("plugin", "install", plugin_id, "--scope", "user")
    return ("plugin", "add", plugin_id, "--json")


def update_args(plugin_id: str) -> tuple[str, ...]:
    return ("plugin", "update", plugin_id, "--scope", "user")


def uninstall_args(host: str, plugin_id: str) -> tuple[str, ...]:
    if host == "claude":
        return ("plugin", "uninstall", plugin_id, "--scope", "user")
    return ("plugin", "remove", plugin_id, "--json")


def marketplace_remove_args(host: str, name: str) -> tuple[str, ...]:
    if host == "claude":
        return ("plugin", "marketplace", "remove", name)
    return ("plugin", "marketplace", "remove", name, "--json")


def list_args(host: str, marketplace: str = MARKETPLACE_NAME) -> tuple[str, ...]:
    if host == "claude":
        return ("plugin", "list", "--json")
    return ("plugin", "list", "--marketplace", marketplace, "--json")


def marketplace_list_args(host: str) -> tuple[str, ...]:
    return ("plugin", "marketplace", "list", "--json")


# --------------------------------------------------------------------------- #
# reading a host's plugin list back
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class PluginEntry:
    plugin_id: str
    version: str | None
    installed: bool | None
    enabled: bool | None

    @property
    def is_installed_and_enabled(self) -> bool:
        return self.installed is not False and self.enabled is True


def _as_text(value: object) -> str | None:
    return value if isinstance(value, str) and value != "" else None


def _as_flag(value: object) -> bool | None:
    return value if isinstance(value, bool) else None


def _walk_entries(node: object, found: list[PluginEntry]) -> None:
    if isinstance(node, list):
        for item in node:
            _walk_entries(item, found)
        return
    if not isinstance(node, dict):
        return
    identity = _as_text(node.get("id")) or _as_text(node.get("pluginId"))
    name = _as_text(node.get("name"))
    owner = _as_text(node.get("marketplaceName")) or _as_text(node.get("marketplace"))
    if identity is None and name is not None and owner is not None:
        identity = f"{name}@{owner}"
    if identity is not None:
        found.append(
            PluginEntry(
                plugin_id=identity,
                version=_as_text(node.get("version")),
                installed=_as_flag(node.get("installed")),
                enabled=_as_flag(node.get("enabled")),
            )
        )
        return
    for value in node.values():
        _walk_entries(value, found)


def parse_entries(text: str) -> list[PluginEntry] | None:
    """The plugin entries of a host's JSON list, or None when the text is not JSON."""

    try:
        data: object = json.loads(text)
    except json.JSONDecodeError:
        return None
    found: list[PluginEntry] = []
    _walk_entries(data, found)
    return found


def read_entries(session: HostSession, *, marketplace: str = MARKETPLACE_NAME) -> list[PluginEntry]:
    record = session.run(*list_args(session.host, marketplace))
    if is_missing_command(record):
        raise StepNotSupported(f"{session.host} has no `plugin list --json`: {excerpt(record.output)}")
    if not record.ok:
        raise StepFail(f"the plugin list command failed: {describe(record)}")
    entries = parse_entries(record.stdout)
    if entries is None:
        raise StepFail(f"the plugin list is not JSON: {excerpt(record.stdout)}")
    return entries


def describe(record: CommandRecord) -> str:
    if record.error is not None:
        return record.error
    return f"exit {record.exit_code}: {excerpt(record.output)}"


def entries_named(entries: Sequence[PluginEntry], name: str) -> list[PluginEntry]:
    return [item for item in entries if item.plugin_id.split("@", 1)[0] == name]


def require_listed(
    entries: Sequence[PluginEntry], plugin_id: str, version: str, label: str, log: StepLog
) -> None:
    matches = [item for item in entries if item.plugin_id == plugin_id]
    if len(matches) != 1:
        raise StepFail(f"{label}: {plugin_id} is listed {len(matches)} times; list: {[e.plugin_id for e in entries]}")
    entry = matches[0]
    if entry.version != version or not entry.is_installed_and_enabled:
        raise StepFail(
            f"{label}: {plugin_id} shows version={entry.version} installed={entry.installed} "
            f"enabled={entry.enabled}, wanted {version} installed and enabled"
        )
    log.note(f"{label}: {plugin_id} version {entry.version} installed={entry.installed} enabled={entry.enabled}")


def must_succeed(record: CommandRecord, what: str) -> CommandRecord:
    if not record.ok:
        raise StepFail(f"{what} failed: {describe(record)}")
    return record


# --------------------------------------------------------------------------- #
# git, in the step's own environment
# --------------------------------------------------------------------------- #


def run_in_step(
    ctx: Context,
    argv: Sequence[str],
    cwd: Path,
    extra: Mapping[str, str] | None = None,
    timeout: int | None = None,
    omit: Sequence[str] = (),
) -> CommandRecord:
    record = run_command(
        argv,
        cwd=cwd,
        env=ctx.environment(extra, omit),
        timeout=timeout or ctx.services.host_timeout,
    )
    ctx.log.commands.append(record)
    return record


def git(ctx: Context, *args: str, cwd: Path | None = None, extra: Mapping[str, str] | None = None) -> CommandRecord:
    executable = resolve_executable("git", ctx.environment())
    if executable is None:
        raise StepFail("git is not on PATH")
    return run_in_step(ctx, [executable, *args], cwd or ctx.step_dir, extra)


PYTHON_EXTRA = {"PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #


def safe_extract(archive: Path, destination: Path) -> int:
    import zipfile

    destination.mkdir(parents=True, exist_ok=False)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        for name in names:
            target = (root / name).resolve()
            if root != target and root not in target.parents:
                raise StepFail(f"the archive names a path outside its directory: {name}")
        bundle.extractall(root)
    return len(names)


def read_json_object(path: Path) -> dict[str, object]:
    try:
        data: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise StepFail(f"{path.name} cannot be read: {type(error).__name__}: {error}") from error
    if not isinstance(data, dict):
        raise StepFail(f"{path.name} is not a JSON object")
    return {str(key): value for key, value in data.items()}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def with_source(marketplace: Mapping[str, object], source: object) -> dict[str, object]:
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        raise StepFail("the marketplace must hold exactly one plugin entry")
    entry = {str(key): value for key, value in plugins[0].items()}
    if entry.get("name") != PLUGIN_NAME:
        raise StepFail(f"the marketplace plugin is {entry.get('name')!r}, not {PLUGIN_NAME}")
    entry["source"] = source
    result = {str(key): value for key, value in marketplace.items()}
    result["plugins"] = [entry]
    return result


def write_local_marketplace(root: Path, marketplace: Mapping[str, object]) -> None:
    """The layout of ticket 71 item 8: one `.claude-plugin` file and one `.agents/plugins` file."""

    write_json(root / ".claude-plugin" / "marketplace.json", with_source(marketplace, "./plugins/software-factory"))
    write_json(
        root / ".agents" / "plugins" / "marketplace.json",
        with_source(marketplace, {"source": "local", "path": "./plugins/software-factory"}),
    )


def step_build(ctx: Context) -> None:
    base = ctx.step_dir
    plan = ctx.plan
    must_succeed(
        git(ctx, "clone", "--no-hardlinks", "-c", "core.autocrlf=false", str(ctx.services.source_repo), "repo", cwd=base),
        "clone",
    )
    repo = base / "repo"
    must_succeed(git(ctx, "-C", "repo", "checkout", "--detach", plan.candidate), "checkout of the candidate")
    head = must_succeed(git(ctx, "-C", "repo", "rev-parse", "HEAD"), "rev-parse").stdout.strip()
    if head != plan.candidate:
        raise StepFail(f"HEAD is {head}, not the candidate {plan.candidate}")
    ctx.log.note(f"cloned with --no-hardlinks and checked out {head} detached")
    generated = run_in_step(
        ctx,
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
            PUBLICATION_REF,
        ],
        repo,
        PYTHON_EXTRA,
    )
    must_succeed(generated, "the publication generator")
    printed = re.search(r"^publication commit ([0-9a-f]{40})\s*$", generated.stdout, re.MULTILINE)
    if printed is None:
        raise StepFail(f"the generator printed no publication commit: {excerpt(generated.output)}")
    commit = printed.group(1)
    if commit != plan.expected_publication:
        raise StepFail(f"the regenerated publication commit {commit} is not the expected {plan.expected_publication}")
    ctx.log.note(f"regenerated publication commit {commit} equals the expected one")
    archive = base / "publication.zip"
    must_succeed(
        git(ctx, "-C", "repo", "archive", "--format=zip", f"--output={archive}", commit),
        "git archive of the publication commit",
    )
    marketplace_root = base / "marketplace"
    package = marketplace_root / "plugins" / PLUGIN_NAME
    count = safe_extract(archive, package)
    manifest = read_json_object(package / ".claude-plugin" / "plugin.json")
    if manifest.get("name") != PLUGIN_NAME or manifest.get("version") != EXPECTED_VERSION:
        raise StepFail(f"the package says {manifest.get('name')} {manifest.get('version')}, not {PLUGIN_NAME} {EXPECTED_VERSION}")
    write_local_marketplace(marketplace_root, read_json_object(repo / ".claude-plugin" / "marketplace.json"))
    ctx.log.note(f"extracted {count} files and built the local marketplace with both files")
    ctx.shared.repo = repo
    ctx.shared.marketplace = marketplace_root
    ctx.shared.package = package
    ctx.shared.publication = commit


def collect_names(node: object, found: list[str]) -> None:
    if isinstance(node, list):
        for item in node:
            collect_names(item, found)
    elif isinstance(node, dict):
        name = _as_text(node.get("name"))
        if name is not None:
            found.append(name)
        for value in node.values():
            if isinstance(value, (list, dict)):
                collect_names(value, found)


def marketplace_names(session: HostSession) -> list[str]:
    record = must_succeed(session.run(*marketplace_list_args(session.host)), "marketplace list")
    try:
        data: object = json.loads(record.stdout)
    except json.JSONDecodeError as error:
        raise StepFail(f"the marketplace list is not JSON: {excerpt(record.stdout)}") from error
    names: list[str] = []
    collect_names(data, names)
    return names


# --------------------------------------------------------------------------- #
# steps that drive a host CLI
# --------------------------------------------------------------------------- #


def open_session(ctx: Context) -> HostSession:
    session = HostSession(ctx, ctx.host)
    version = session.version()
    if not version.ok:
        raise StepFail(f"{ctx.host} --version failed: {describe(version)}")
    ctx.log.note(f"{ctx.host} --version: {excerpt(version.output, 80)}")
    return session


def install_from_local(ctx: Context, session: HostSession) -> None:
    source = str(ctx.local_marketplace())
    must_succeed(session.run(*marketplace_add_args(session.host, source)), "marketplace add of the local marketplace")
    must_succeed(session.run(*install_args(session.host, PLUGIN_ID)), f"install of {PLUGIN_ID}")


def fresh_sequence(ctx: Context, session: HostSession) -> None:
    """Install from the local marketplace and read it back; Claude Code then runs the README's update."""

    install_from_local(ctx, session)
    require_listed(read_entries(session), PLUGIN_ID, EXPECTED_VERSION, "after install", ctx.log)
    if session.host == "claude":
        must_succeed(session.run(*update_args(PLUGIN_ID)), "the README's plugin update")
        require_listed(read_entries(session), PLUGIN_ID, EXPECTED_VERSION, "after update", ctx.log)


def step_fresh(ctx: Context) -> None:
    fresh_sequence(ctx, open_session(ctx))


def installed_commit(session: HostSession, plugin_id: str, install_json: str) -> str | None:
    """The commit a host installed a plugin from, read from the host's own state."""

    if session.host == "claude":
        state = session.step_dir / "plugins" / "installed_plugins.json"
        try:
            data: object = json.loads(state.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        plugins = data.get("plugins") if isinstance(data, dict) else None
        records = plugins.get(plugin_id) if isinstance(plugins, dict) else None
        if isinstance(records, list) and records and isinstance(records[0], dict):
            return _as_text(records[0].get("gitCommitSha"))
        return None
    try:
        document: object = json.loads(install_json)
    except json.JSONDecodeError:
        return None
    location = _as_text(document.get("installedPath")) if isinstance(document, dict) else None
    if location is None:
        return None
    head = run_command(
        ["git", "-C", location, "rev-parse", "HEAD"], cwd=session.step_dir, env=session.env, timeout=60
    )
    session.ctx.log.commands.append(head)
    found = head.stdout.strip()
    return found if head.ok and _FULL_SHA.fullmatch(found) is not None else None


def old_install(ctx: Context, session: HostSession) -> None:
    """Install johnny-ai-skill 0.4.14 from the public marketplace and say which commit it came from."""

    if session.host == "claude":
        source = CLAUDE_OLD_MARKETPLACE_URL
    else:
        source = CODEX_OLD_MARKETPLACE_SOURCE
    must_succeed(session.run(*marketplace_add_args(session.host, source)), "marketplace add of the 0.4.14 marketplace")
    installed = session.run(*install_args(session.host, OLD_PLUGIN_ID))
    if not installed.ok:
        if session.host == "codex":
            honoured = "0" * 40 in installed.output
            ctx.log.note(
                "Codex "
                + ("honoured `sha`: it tried to check out the pinned forty zeros" if honoured else "refused the install")
                + " (CHANGE_DETECTED: the 0.4.14 Codex install path does not work as the ticket assumes)"
            )
        raise StepFail(f"the 0.4.14 install was refused: {describe(installed)}")
    require_listed(read_entries(session, marketplace=OLD_MARKETPLACE_NAME), OLD_PLUGIN_ID, OLD_VERSION, "0.4.14", ctx.log)
    commit = installed_commit(session, OLD_PLUGIN_ID, installed.stdout)
    if commit != OLD_PINNED_COMMIT:
        raise StepFail(f"0.4.14 was installed from {commit}, not from {OLD_PINNED_COMMIT}")
    ctx.log.note(f"0.4.14 installed from {commit}, the publication main")


def remove_old(session: HostSession) -> None:
    must_succeed(session.run(*uninstall_args(session.host, OLD_PLUGIN_ID)), "removal of the old plugin")
    must_succeed(
        session.run(*marketplace_remove_args(session.host, OLD_MARKETPLACE_NAME)), "removal of the old marketplace"
    )


def step_upgrade(ctx: Context) -> None:
    session = open_session(ctx)
    old_install(ctx, session)
    remove_old(session)
    install_from_local(ctx, session)
    entries = read_entries(session)
    require_listed(entries, PLUGIN_ID, EXPECTED_VERSION, "after the upgrade", ctx.log)
    if entries_named(entries, OLD_PLUGIN_NAME):
        raise StepFail("the plugin list still shows a johnny-ai-skill plugin")
    if OLD_MARKETPLACE_NAME in marketplace_names(session):
        raise StepFail("the marketplace list still shows johnny-ai-skill")
    ctx.log.note("the list shows software-factory 0.5.0 and no johnny-ai-skill plugin or marketplace")


def step_uninstall(ctx: Context) -> None:
    session = open_session(ctx)
    allowed = load_allowlist(ctx.services.readme)
    fresh_sequence(ctx, session)
    must_succeed(session.run(*uninstall_args(session.host, PLUGIN_ID)), "the README's plugin uninstall")
    must_succeed(
        session.run(*marketplace_remove_args(session.host, MARKETPLACE_NAME)), "the README's marketplace remove"
    )
    findings = scan_residue(ctx.step_dir, session.host, allowed)
    if findings:
        for finding in findings[:20]:
            ctx.log.note(f"residue: {finding}")
        raise StepFail(f"{len(findings)} residue finding(s) outside the allow-list")
    ctx.log.note(f"no residue naming {MARKETPLACE_NAME} outside the {len(allowed)} allow-listed entries")


def write_broken_marketplace(root: Path) -> None:
    """A marketplace named software-factory whose one plugin names a directory that does not exist."""

    def document(source: object) -> dict[str, object]:
        entry: dict[str, object] = {"name": PLUGIN_NAME, "version": EXPECTED_VERSION, "source": source}
        return {"name": MARKETPLACE_NAME, "owner": {"name": "acceptance"}, "plugins": [entry]}

    write_json(root / ".claude-plugin" / "marketplace.json", document("./plugins/missing"))
    write_json(root / ".agents" / "plugins" / "marketplace.json", document({"source": "local", "path": "./plugins/missing"}))


def step_recover(ctx: Context) -> None:
    session = open_session(ctx)
    broken = ctx.step_dir / "broken-marketplace"
    write_broken_marketplace(broken)
    added = session.run(*marketplace_add_args(session.host, str(broken)))
    installed = session.run(*install_args(session.host, PLUGIN_ID))
    if added.ok and installed.ok:
        raise StepFail("the broken install exited 0 in both of its commands")
    first = added if not added.ok else installed
    ctx.log.note(f"expected failure: {'marketplace add' if first is added else 'install'}: {describe(first)}")
    first_out = session.run(*uninstall_args(session.host, PLUGIN_ID))
    second_out = session.run(*marketplace_remove_args(session.host, MARKETPLACE_NAME))
    ctx.log.note(f"cleanup exits, not judged: uninstall {first_out.exit_code}, marketplace remove {second_out.exit_code}")
    install_from_local(ctx, session)
    entries = read_entries(session)
    if len(entries) != 1:
        raise StepFail(f"the list shows {len(entries)} entries, not exactly one: {[e.plugin_id for e in entries]}")
    require_listed(entries, PLUGIN_ID, EXPECTED_VERSION, "after recovery", ctx.log)


# --------------------------------------------------------------------------- #
# residue: the allow-lists live in ci/acceptance/README.md
# --------------------------------------------------------------------------- #

_WHOLE_NAME = re.compile(r"(?<![A-Za-z0-9_-])software-factory(?![A-Za-z0-9_-])")
RESIDUE_SUFFIXES = (".json", ".toml")
ALLOW_KINDS = ("path", "line", "emptydir")


@dataclass(frozen=True)
class AllowEntry:
    kind: str
    host: str
    target: str
    reason: str


def names_whole(text: str) -> bool:
    """True when `text` names software-factory as a whole name, never as a prefix or suffix of another."""

    return _WHOLE_NAME.search(text) is not None


def fenced_block(text: str, label: str) -> list[str]:
    """The lines of the fenced block opened by ```<label>; an absent block is an empty list."""

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == f"```{label}":
            body: list[str] = []
            for follower in lines[index + 1 :]:
                if follower.strip() == "```":
                    return body
                body.append(follower)
            raise StepFail(f"the {label} block in the README is not closed")
    return []


def read_readme(readme: Path) -> str:
    try:
        return readme.read_text(encoding="utf-8")
    except OSError as error:
        raise StepFail(f"the allow-list README cannot be read: {error}") from error


def parse_allowlist(text: str) -> list[AllowEntry]:
    entries: list[AllowEntry] = []
    for line in fenced_block(text, "lifecycle-allowlist"):
        if line.strip() == "" or line.lstrip().startswith("#"):
            continue
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != 4 or fields[0] not in ALLOW_KINDS or fields[1] not in HOST_NAMES or "" in fields:
            raise StepFail(f"a malformed allow-list entry: {line!r}")
        entries.append(AllowEntry(fields[0], fields[1], fields[2], fields[3]))
    return entries


def load_allowlist(readme: Path) -> list[AllowEntry]:
    return parse_allowlist(read_readme(readme))


def parse_level2_allowlist(text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in fenced_block(text, "lifecycle-level2-allowlist"):
        if line.strip() == "" or line.lstrip().startswith("#"):
            continue
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != 2 or "" in fields:
            raise StepFail(f"a malformed Level 2 allow-list entry: {line!r}")
        entries.append((fields[0], fields[1]))
    return entries


def _path_allowed(relative: str, host: str, allowed: Sequence[AllowEntry]) -> bool:
    for entry in allowed:
        if entry.kind == "path" and entry.host == host and (
            relative == entry.target or relative.startswith(entry.target + "/")
        ):
            return True
    return False


def _empty_dir_allowed(path: Path, relative: str, host: str, allowed: Sequence[AllowEntry]) -> bool:
    """An `emptydir` entry admits a directory that holds no file at any depth."""

    if not path.is_dir() or not any(item.kind == "emptydir" and item.host == host and item.target == relative for item in allowed):
        return False
    return not any(child.is_file() for child in path.rglob("*"))


def _line_allowed(relative: str, host: str, allowed: Sequence[AllowEntry]) -> bool:
    return any(item.kind == "line" and item.host == host and item.target == relative for item in allowed)


def scan_residue(step_dir: Path, host: str, allowed: Sequence[AllowEntry]) -> list[str]:
    """Paths and `.json`/`.toml` lines under the step directory that name software-factory as a whole name."""

    findings: list[str] = []
    for path in sorted(step_dir.rglob("*")):
        relative = path.relative_to(step_dir).as_posix()
        if (
            names_whole(relative)
            and not _path_allowed(relative, host, allowed)
            and not _empty_dir_allowed(path, relative, host, allowed)
        ):
            findings.append(f"path {relative}")
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in RESIDUE_SUFFIXES:
            if _path_allowed(relative, host, allowed) or _line_allowed(relative, host, allowed):
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError as error:
                findings.append(f"unreadable {relative}: {error}")
                continue
            for number, line in enumerate(lines, start=1):
                if names_whole(line):
                    findings.append(f"line {relative}:{number}")
    return findings


# --------------------------------------------------------------------------- #
# level2: the 0.4.9 runtime is installed and removed by its own commands
# --------------------------------------------------------------------------- #


def sha256_of(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def step_level2(ctx: Context) -> None:
    allowed = parse_level2_allowlist(read_readme(ctx.services.readme))
    downloads = ctx.step_dir / "download"
    downloads.mkdir()
    for name, digest in LEVEL2_ASSETS.items():
        ctx.services.downloader(LEVEL2_RELEASE_URL + name, downloads / name)
        actual = sha256_of(downloads / name)
        if actual != digest:
            raise StepFail(f"{name} has sha256 {actual}, not the approved {digest}")
    ctx.log.note("both 0.4.9 assets match their approved sha256 values")
    root = ctx.step_dir / "root"
    root.mkdir()
    if any(root.iterdir()):
        raise StepFail("JOHNNY_ROOT is not empty; the INSTALL answer is authorised for an empty root only")
    extra = {"JOHNNY_ROOT": str(root)}
    # The `py` launcher that install.ps1 calls exits 109 under any USERPROFILE other than the real one, and the
    # step must not expose the real profile, so this step, which runs the 0.4.9 installer and not a host CLI,
    # leaves USERPROFILE out. HOME stays the step's own. JOHNNY_ROOT relocates the whole runtime.
    omitted = ("USERPROFILE",)
    # Owner decision of 2026-11-26 (S77R-01): this script answers the 0.4.9 installer's INSTALL prompt on
    # standard input, only for an install into the empty JOHNNY_ROOT made for this acceptance.
    installed = run_command(
        ctx.services.level2_install(downloads / LEVEL2_WRAPPER),
        cwd=downloads,
        env=ctx.environment(extra, omitted),
        stdin=LEVEL2_CONFIRMATION,
        timeout=1800,
    )
    ctx.log.commands.append(installed)
    must_succeed(installed, "the 0.4.9 install")
    if not (root / "launcher" / "johnny-router.ps1").is_file():
        raise StepFail("the 0.4.9 install left no launcher in JOHNNY_ROOT")
    ctx.log.note(f"the 0.4.9 install exited 0 and JOHNNY_ROOT holds {sum(1 for _ in root.rglob('*'))} paths")
    removed = run_command(
        ctx.services.level2_uninstall(root),
        cwd=ctx.step_dir,
        env=ctx.environment(extra, omitted),
        timeout=1800,
    )
    ctx.log.commands.append(removed)
    must_succeed(removed, "the 0.4.9 uninstall")
    if root.exists():
        listed = {item for item, _ in allowed}
        leftovers = sorted(
            path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
        )
        unexpected = [item for item in leftovers if item not in listed]
        for item in unexpected[:20]:
            ctx.log.note(f"residue: {item}")
        if unexpected:
            raise StepFail(f"{len(unexpected)} file(s) left in JOHNNY_ROOT outside the allow-list")
    ctx.log.note("after uninstall JOHNNY_ROOT holds no file outside the allow-list")


# --------------------------------------------------------------------------- #
# codex-ref and codex-files
# --------------------------------------------------------------------------- #

GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "acceptance",
    "GIT_AUTHOR_EMAIL": "acceptance@example.invalid",
    "GIT_COMMITTER_NAME": "acceptance",
    "GIT_COMMITTER_EMAIL": "acceptance@example.invalid",
}


def tree_digest(root: Path) -> dict[str, str]:
    """Relative path to sha256 of the content, without `.git`; CRLF in a text file reads as LF."""

    import hashlib

    digest: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or relative == ".git" or relative.startswith(".git/"):
            continue
        data = path.read_bytes()
        if b"\0" not in data:
            data = data.replace(b"\r\n", b"\n")
        digest[relative] = hashlib.sha256(data).hexdigest()
    return digest


def commit_all(ctx: Context, repo: Path, message: str) -> str:
    must_succeed(git(ctx, "-C", str(repo), "-c", "core.autocrlf=false", "add", "-A", extra=GIT_IDENTITY), "git add")
    must_succeed(
        git(ctx, "-C", str(repo), "-c", "core.autocrlf=false", "commit", "-q", "-m", message, extra=GIT_IDENTITY),
        "git commit",
    )
    return must_succeed(git(ctx, "-C", str(repo), "rev-parse", "HEAD"), "git rev-parse").stdout.strip()


def extract_commit(ctx: Context, repo: Path, commit: str, destination: Path) -> dict[str, str]:
    archive = destination.with_suffix(".zip")
    must_succeed(git(ctx, "-C", str(repo), "archive", "--format=zip", f"--output={archive}", commit), "git archive")
    safe_extract(archive, destination)
    return tree_digest(destination)


def require_package(ctx: Context) -> tuple[Path, Path]:
    if ctx.shared.package is None or ctx.shared.repo is None:
        raise StepFail("no package: build did not pass in this run")
    return ctx.shared.package, ctx.shared.repo


def step_codex_ref(ctx: Context) -> None:
    session = open_session(ctx)
    package, repo = require_package(ctx)
    work = ctx.step_dir / "work"
    market = ctx.step_dir / "market"
    remote = ctx.step_dir / "remote.git"
    must_succeed(git(ctx, "init", "-q", "-b", "main", str(work)), "git init of the plugin repository")
    shutil.copytree(package, work, dirs_exist_ok=True)
    pinned = commit_all(ctx, work, "the pinned commit")
    (work / "after-the-pin.txt").write_text("a later commit on the default branch\n", encoding="utf-8", newline="\n")
    tip = commit_all(ctx, work, "after the pin")
    if tip == pinned:
        raise StepFail("the default branch tip equals the pinned commit")
    must_succeed(git(ctx, "init", "-q", "--bare", "-b", "main", str(remote)), "git init --bare")
    must_succeed(git(ctx, "-C", str(work), "push", "-q", str(remote), "main"), "push of main")
    remote_url = remote.resolve().as_uri()
    must_succeed(git(ctx, "init", "-q", "-b", "marketplace", str(market)), "git init of the marketplace branch")
    write_json(
        market / ".claude-plugin" / "marketplace.json",
        with_source(
            read_json_object(repo / ".claude-plugin" / "marketplace.json"),
            {"source": "url", "url": remote_url, "sha": pinned},
        ),
    )
    commit_all(ctx, market, "the marketplace branch")
    must_succeed(git(ctx, "-C", str(market), "push", "-q", str(remote), "marketplace"), "push of marketplace")
    ctx.log.note(f"pinned commit {pinned}; default branch tip {tip}; the marketplace branch holds only .claude-plugin/marketplace.json")
    added = session.run(*marketplace_add_args("codex", remote_url, ref="marketplace"))
    if not added.ok:
        raise StepNotSupported(f"codex marketplace add refused the file:// URL: {describe(added)}")
    installed = must_succeed(session.run(*install_args("codex", PLUGIN_ID)), "plugin add")
    try:
        document: object = json.loads(installed.stdout)
    except json.JSONDecodeError as error:
        raise StepFail(f"plugin add printed no JSON: {excerpt(installed.stdout)}") from error
    location = _as_text(document.get("installedPath")) if isinstance(document, dict) else None
    if location is None or not Path(location).is_dir():
        raise StepFail(f"plugin add named no installed directory: {excerpt(installed.stdout)}")
    actual = tree_digest(Path(location))
    wanted = extract_commit(ctx, work, pinned, ctx.step_dir / "pinned-tree")
    if actual == wanted:
        ctx.log.note("Codex honoured `sha`: the installed tree equals the pinned commit's tree")
        return
    other = extract_commit(ctx, work, tip, ctx.step_dir / "tip-tree")
    reason = "the installed tree equals the default branch tip, so `sha` was ignored" if actual == other else (
        f"the installed tree matches neither the pin nor the tip ({len(set(actual) ^ set(wanted))} differing paths)"
    )
    raise StepFail(reason)


def case_marketplace(ctx: Context, case: str, package: Path, template: Mapping[str, object]) -> Path:
    root = ctx.step_dir / f"files-{case}"
    claude_file = case in ("both", "claude-only")
    agents_file = case in ("both", "agents-only")
    if case == "both":
        shutil.copytree(package, root / "plugins" / "sf-claude")
        shutil.copytree(package, root / "plugins" / "sf-agents")
        newer = read_json_object(root / "plugins" / "sf-agents" / ".claude-plugin" / "plugin.json")
        newer["version"] = "0.5.1"
        write_json(root / "plugins" / "sf-agents" / ".claude-plugin" / "plugin.json", newer)
        claude_path, agents_path = "./plugins/sf-claude", "./plugins/sf-agents"
    else:
        shutil.copytree(package, root / "plugins" / PLUGIN_NAME)
        claude_path = agents_path = "./plugins/software-factory"
    if claude_file:
        write_json(root / ".claude-plugin" / "marketplace.json", with_source(template, claude_path))
    if agents_file:
        entry = with_source(template, {"source": "local", "path": agents_path})
        if case == "both":
            plugins = entry["plugins"]
            if isinstance(plugins, list) and isinstance(plugins[0], dict):
                plugins[0]["version"] = "0.5.1"
        write_json(root / ".agents" / "plugins" / "marketplace.json", entry)
    return root


def step_codex_files(ctx: Context) -> None:
    session = open_session(ctx)
    package, repo = require_package(ctx)
    template = read_json_object(repo / ".claude-plugin" / "marketplace.json")
    crashed: list[str] = []
    for case in ("both", "claude-only", "agents-only"):
        root = case_marketplace(ctx, case, package, template)
        added = session.run(*marketplace_add_args("codex", str(root)))
        installed = session.run(*install_args("codex", PLUGIN_ID))
        listing = session.run(*list_args("codex"))
        version = "none"
        parsed = parse_entries(listing.stdout) if listing.ok else None
        for entry in entries_named(parsed or [], PLUGIN_NAME):
            version = f"{entry.version} installed={entry.installed}"
        removed = session.run(*uninstall_args("codex", PLUGIN_ID))
        gone = session.run(*marketplace_remove_args("codex", MARKETPLACE_NAME))
        for record in (added, installed, listing, removed, gone):
            if record.error is not None:
                crashed.append(f"{case}: {describe(record)}")
        ctx.log.note(
            f"{case}: marketplace add exit {added.exit_code}; plugin add exit {installed.exit_code}; "
            f"listed version {version}; plugin remove exit {removed.exit_code}; marketplace remove exit {gone.exit_code}"
        )
    if crashed:
        raise StepFail("a command did not complete: " + "; ".join(crashed))


# --------------------------------------------------------------------------- #
# the run
# --------------------------------------------------------------------------- #

STEP_FUNCTIONS: Mapping[str, Callable[[Context], None]] = {
    "build": step_build,
    "fresh": step_fresh,
    "upgrade": step_upgrade,
    "uninstall": step_uninstall,
    "recover": step_recover,
    "level2": step_level2,
    "codex-ref": step_codex_ref,
    "codex-files": step_codex_files,
}


def command_row(record: CommandRecord) -> dict[str, object]:
    row: dict[str, object] = {
        "argv": [redact(part) for part in record.argv],
        "exit": record.exit_code,
        "output": excerpt(record.output),
    }
    if record.error is not None:
        row["error"] = redact(record.error)
    return row


def report_line(step: str, host: str, verdict: Verdict, log: StepLog) -> str:
    line: dict[str, object] = {
        "step": step,
        "host": host,
        "verdict": verdict.value,
        "commands": [command_row(record) for record in log.commands],
        "evidence": [redact(item) for item in log.evidence],
    }
    return json.dumps(line, ensure_ascii=True)


def run_step(plan: Plan, services: Services, shared: Shared, step: str, host: str) -> tuple[Verdict, StepLog]:
    log = StepLog()
    directory = plan.run_root / (step if host == "none" else f"{step}-{host}")
    try:
        directory.mkdir(parents=True, exist_ok=False)
        ctx = Context(plan, services, step, host, directory, log, shared)
        STEP_FUNCTIONS[step](ctx)
    except StepNotSupported as error:
        log.note(f"NOT_SUPPORTED: {error}")
        return Verdict.NOT_SUPPORTED, log
    except StepFail as error:
        log.note(f"FAIL: {error}")
        return Verdict.FAIL, log
    except Exception as error:  # a step never ends as a traceback: it is a FAIL with the reason
        log.note(f"FAIL: unexpected {type(error).__name__}: {error}")
        return Verdict.FAIL, log
    return Verdict.PASS, log


def run_plan(plan: Plan, services: Services) -> list[tuple[str, str, Verdict]]:
    plan.run_root.mkdir(parents=True, exist_ok=True)
    report = plan.run_root / "report.jsonl"
    shared = Shared()
    results: list[tuple[str, str, Verdict]] = []
    build_passed = False
    for step in plan.steps:
        for host in hosts_for(step, plan.host):
            if step != "build" and not build_passed:
                log = StepLog()
                log.note("FAIL: not run, because build did not pass in this run")
                verdict = Verdict.FAIL
            else:
                verdict, log = run_step(plan, services, shared, step, host)
                if step == "build":
                    build_passed = verdict is Verdict.PASS
            with open(report, "a", encoding="utf-8", newline="\n") as handle:
                handle.write(report_line(step, host, verdict, log) + "\n")
            results.append((step, host, verdict))
    return results


def main(argv: Sequence[str] | None = None, services: Services | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run the 0.5.0 install lifecycle in isolated directories.")
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--expected-publication", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--steps", required=True)
    parser.add_argument("--run-root", required=True)
    try:
        parsed = parser.parse_args(argv)
        plan = validate_plan(
            parsed.candidate,
            parsed.expected_publication,
            parsed.host,
            parsed.steps,
            parsed.run_root,
            None if services is None else services.environ,
        )
    except Refusal as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    results = run_plan(plan, services or Services())
    for step, host, verdict in results:
        print(f"{verdict.value} {step} {host}")
    return 0 if all(verdict is Verdict.PASS for _, _, verdict in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
