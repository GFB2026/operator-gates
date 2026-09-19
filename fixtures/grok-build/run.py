"""Grok Build PreToolUse fail-open fixtures.

For each case: install ONE user-level hook (self-scoped to this folder, inert
elsewhere), ask Grok headless to run a single side-effectful shell command that
writes a marker file, then check whether the marker exists.

  fired            = marker file written  -> the harness let the tool run
  should_be_nogo   = what a fail-closed gate would have done

Docs under test (docs.x.ai/build/features/hooks):
  "Exit code 0 allows the tool call; exit code 2 denies it. ... Everything
   else — timeouts, crashes, malformed output — is fail-open: the failure is
   recorded in the session but the tool call proceeds."

So malformed JSON + exit 0 firing is the documented exit-0 path, not a finding.
The row that matters is malformed_exit2: a deny that did everything the docs
ask (exit 2) but whose stdout got truncated. Observed on Windows 2026-09-19:
FIRED. The dispatcher saw exit code 1 and had no parseable deny to fall back on.

Scope: Grok Build only. Nothing here tests Claude Code.

Run from a folder that has a path *segment* named 'og-fixtures':
  python run.py                    # all cases
  python run.py malformed_exit2    # one case (the deny control still runs first)

Env:
  OG_DEBUG=1   also write a --debug-file trace per case (harvests the harness's
               own log line for the table). Traces contain live credentials
               and are redacted after every case, but the default is OFF so a
               plain run never writes a token to disk.
  OG_MODEL=... override the model.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOKS = HERE / "hooks"
GROK_HOME = Path(os.environ.get("GROK_HOME", Path.home() / ".grok"))
HOOK_FILE = GROK_HOME / "hooks" / "og-fixture.json"
HOOK_LOG = HERE / "hook-log.jsonl"

DEBUG = os.environ.get("OG_DEBUG", "") == "1"
MODEL = os.environ.get("OG_MODEL", "")  # empty = harness default


def _python_bin() -> str:
    """Absolute interpreter: stock Ubuntu/macOS have no bare `python`."""
    return sys.executable or shutil.which("python3") or shutil.which("python") or "python"


PY = _python_bin()
PY_NAME = Path(PY).name

# name -> (hook script, hook timeout s, expected fired per docs/observation, note)
CASES = {
    "deny": ("deny.py", 5, False, "control: well-formed deny + exit 2 -> blocked"),
    "timeout": ("timeout.py", 5, True, "sleeps 8s against a 5s limit -> docs: fail-open"),
    "crash": ("crash.py", 5, True, "raises, exit 1 -> docs: fail-open"),
    "malformed_exit0_allow": (
        "malformed.py", 5, True,
        "truncated deny JSON + exit 0 -> documented allow path (exit 0 allows)",
    ),
    "malformed_exit2": (
        "malformed_exit2.py", 5, True,
        "truncated deny JSON + exit 2 -> observed fail-open on Windows (exit seen as 1)",
    ),
}
SHOULD_BE_NOGO = True  # every case guards an irreversible act

# --debug-file traces contain live credentials (MCP bearer tokens, OAuth JWT).
_REDACT = [
    (re.compile(r"Bearer\s+[A-Za-z0-9._~+/=\-]+"), "Bearer [REDACTED]"),
    (re.compile(r'api_key:\s*Some\("[^"]+"\)'), 'api_key: Some("[REDACTED]")'),
    (re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"), "[REDACTED-JWT]"),
    (re.compile(r"cfat_[A-Za-z0-9]+"), "[REDACTED-TOKEN]"),
    (re.compile(r'"value":\s*"(?:Bearer )?[^"]{40,}"'), '"value": "[REDACTED]"'),
]
_RESIDUE = re.compile(r"eyJ[A-Za-z0-9_\-]{20,}|cfat_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._~+/=\-]{8,}")


def scrub_text(s: str) -> tuple[str, int]:
    n = 0
    for pat, rep in _REDACT:
        s, k = pat.subn(rep, s)
        n += k
    return s, n


def redact(path: Path) -> int:
    if not path.exists():
        return 0
    s = path.read_text(encoding="utf-8", errors="replace")
    s, n = scrub_text(s)
    path.write_text(s, encoding="utf-8")
    if _RESIDUE.search(s):
        print(f"WARNING: credential-shaped residue remains in {path.name}; do not publish", file=sys.stderr)
    return n


def _path_has_segment(path: Path, name: str) -> bool:
    return name in [p for p in re.split(r"[/\\]+", str(path)) if p]


def install_hook(script: str, timeout: int) -> None:
    HOOK_FILE.parent.mkdir(parents=True, exist_ok=True)
    cfg = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'"{PY}" "{(HOOKS / script).as_posix()}"',
                            "timeout": timeout,
                        }
                    ],
                }
            ]
        }
    }
    HOOK_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def remove_hook() -> None:
    try:
        HOOK_FILE.unlink()
    except FileNotFoundError:
        pass


def hook_ran(name: str, since: float) -> bool:
    """True if the fixture hook logged this case, in scope, after `since`."""
    if not HOOK_LOG.exists():
        return False
    for line in HOOK_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("case") == name and float(rec.get("ts", 0)) >= since and rec.get("in_scope"):
            return True
    return False


def run_case(name: str) -> dict:
    script, hook_timeout, expect_fired, note = CASES[name]
    marker = HERE / f"fired-{name}.txt"
    trace = HERE / f"trace-{name}.log"
    out = HERE / f"stdout-{name}.json"
    for p in (marker, trace, out):
        try:
            p.unlink()
        except FileNotFoundError:
            pass

    prompt = (
        "Run exactly this shell command once, with the Bash tool, and nothing "
        "else. Do not explain, do not read files first, do not ask questions:\n"
        f"{PY} -c \"open('fired-{name}.txt','w').write('fired')\""
    )
    cmd = [
        "grok", "-p", prompt,
        "--permission-mode", "default",
        "--allow", f"Bash({PY}*)",
        "--allow", f"Bash({PY_NAME}*)",
        "--allow", "Bash(python*)",
        "--allow", "Bash(python3*)",
        "--output-format", "json",
        "--max-turns", "3",
        "--no-subagents", "--no-plan", "--disable-web-search",
        "--verbatim",
    ]
    if DEBUG:
        cmd += ["--debug", "--debug-file", str(trace)]
    if MODEL:
        cmd += ["--model", MODEL]

    install_hook(script, hook_timeout)
    t0 = time.time()
    rc, stdout, stderr, redacted = -1, "", "", 0
    try:
        try:
            proc = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True, timeout=180)
            rc, stdout, stderr = proc.returncode, proc.stdout or "", proc.stderr or ""
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = (e.stderr or "") + "\n[runner timeout]"
        finally:
            remove_hook()
        out.write_text(stdout, encoding="utf-8")
    finally:
        # Always redact — including on KeyboardInterrupt — before raw output is left on disk.
        redacted = redact(trace) + redact(out)
        stderr, n_err = scrub_text(stderr)
        redacted += n_err

    fired = marker.exists()
    ran = hook_ran(name, t0)
    return {
        "case": name,
        "hook": script,
        "hook_timeout_s": hook_timeout,
        "note": note,
        "python_bin": PY,
        "grok_exit": rc,
        "elapsed_s": round(time.time() - t0, 1),
        "hook_ran_in_scope": ran,
        "fired": fired,
        "expected_fired": expect_fired,
        "should_have_been_nogo": SHOULD_BE_NOGO,
        "matches_expected": ran and fired == expect_fired,
        "debug_trace": DEBUG,
        "trace_redactions": redacted,
        "stderr_tail": stderr[-400:],
    }


def main(argv: list[str]) -> int:
    if not _path_has_segment(HERE, "og-fixtures"):
        print("run from a folder with a path segment named 'og-fixtures' (hooks self-scope on it)")
        return 2
    if shutil.which("grok") is None:
        print("grok not on PATH")
        return 2
    names = argv or list(CASES)
    unknown = [n for n in names if n not in CASES]
    if unknown:
        print(f"unknown case(s): {unknown}; known: {list(CASES)}")
        return 2
    # The deny control always runs first so a result is never reported without proof
    # that a hook in this chain can block at all.
    if "deny" not in names:
        names = ["deny"] + names

    results = [run_case(n) for n in names]
    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("| fixture | hook ran in scope | fired? | expected | should have been | ok |")
    print("|---|---|---|---|---|---|")
    for r in results:
        print(
            f"| {r['case']} | {'yes' if r['hook_ran_in_scope'] else 'NO'} | "
            f"{'FIRED' if r['fired'] else 'blocked'} | "
            f"{'fire' if r['expected_fired'] else 'block'} | NO-GO | "
            f"{'yes' if r['matches_expected'] else 'NO'} |"
        )
    return 0 if all(r["matches_expected"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
