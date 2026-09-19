"""Shared by every fixture hook. Reads the PreToolUse envelope, logs it, and
self-scopes: outside the fixture workspace the hook exits 0 immediately so it is
inert if installed at user level.

Scope rule: cwd must contain a path *segment* exactly equal to ``og-fixtures``
(split on ``/`` and ``\\``). A substring is not enough — ``~/blog-fixtures``
must not match.

Every hook logs BEFORE acting, including out-of-scope invocations, so run.py can
prove the hook ran (and where) rather than inferring it from the marker file.
"""
from __future__ import annotations
import json, os, re, sys, time
from pathlib import Path

FIXTURE_DIR_NAME = "og-fixtures"


def read_event() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}


def _cwd(ev: dict) -> str:
    return str(ev.get("cwd") or ev.get("workspaceRoot") or os.environ.get("GROK_WORKSPACE_ROOT") or "")


def in_scope(ev: dict) -> bool:
    parts = [p for p in re.split(r"[/\\]+", _cwd(ev)) if p]
    return FIXTURE_DIR_NAME in parts


def log(case: str, ev: dict, note: str) -> None:
    scoped = in_scope(ev)
    root = Path(_cwd(ev) or ".") if scoped else Path(os.path.dirname(os.path.abspath(__file__))).parent
    line = {
        "ts": time.time(), "case": case, "note": note, "in_scope": scoped,
        "cwd": _cwd(ev),
        "hookEventName": ev.get("hookEventName"), "toolName": ev.get("toolName"),
        "toolInput": ev.get("toolInput"), "sessionId": ev.get("sessionId"),
    }
    try:
        with open(root / "hook-log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")
    except Exception:
        pass


def guard(case: str, ev: dict, note: str) -> None:
    """Log, then exit 0 (inert) when out of scope."""
    log(case, ev, note)
    if not in_scope(ev):
        sys.exit(0)
