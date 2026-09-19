"""Shared by every fixture hook. Reads the PreToolUse envelope, logs it, and
self-scopes: outside the fixture workspace the hook exits 0 immediately so it is
inert if installed at user level."""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path

FIXTURE_DIR_NAME = "og-fixtures"

def read_event() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}

def in_scope(ev: dict) -> bool:
    cwd = str(ev.get("cwd") or ev.get("workspaceRoot") or os.environ.get("GROK_WORKSPACE_ROOT") or "")
    return FIXTURE_DIR_NAME in cwd.replace("\\", "/")

def log(case: str, ev: dict, note: str) -> None:
    root = Path(str(ev.get("cwd") or ".")).expanduser()
    line = {
        "ts": time.time(), "case": case, "note": note,
        "hookEventName": ev.get("hookEventName"), "toolName": ev.get("toolName"),
        "toolInput": ev.get("toolInput"), "sessionId": ev.get("sessionId"),
    }
    try:
        with open(root / "hook-log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")
    except Exception:
        pass
