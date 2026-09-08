"""Fail-closed posture gate.

Reference shape only. Wire your own live boot / phrase / holds into Posture.
Never infer money or bulk outreach permission from chat alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PathClass = Literal["mail_send", "outreach", "money", "voice", "other"]


@dataclass
class Posture:
    """Signals your control plane already knows.

    Fill from live state (boot, holds, mirror health). Do not invent greens.
    """

    mirror_ok: bool = False
    outreach_live: bool = False
    outreach_paused: bool = True
    holds: list[str] = field(default_factory=list)
    phrase: bool = False  # human said the exact approve phrase for this path
    note: str = ""


@dataclass(frozen=True)
class Card:
    go: bool
    path: PathClass
    reason: str = ""
    need: str = ""
    note: str = ""

    def render(self) -> str:
        if self.go:
            bits = [
                "ARMED-CHECK: GO",
                f"path={self.path}",
            ]
            if self.note:
                bits.append(f"note={_short(self.note)}")
            return " | ".join(bits)
        bits = [
            "ARMED-CHECK: NO-GO",
            f"path={self.path}",
            f"reason={_short(self.reason) or 'blocked'}",
        ]
        if self.need:
            bits.append(f"need={_short(self.need)}")
        return " | ".join(bits)

    def __str__(self) -> str:
        return self.render()


def check(path: PathClass, posture: Posture | None = None) -> Card:
    """Emit one GO / NO-GO card. NO-GO means do not mutate in this turn."""
    p = posture or Posture()

    if path == "mail_send":
        if not p.mirror_ok:
            return Card(
                False,
                path,
                reason="mirror not ok",
                need="fix mirror or use read-only",
            )
        blocking = [h for h in p.holds if _blocks_mail(h)]
        if blocking:
            return Card(
                False,
                path,
                reason=f"hold:{blocking[0]}",
                need="clear hold or park send",
            )
        if not p.phrase:
            return Card(
                False,
                path,
                reason="missing phrase",
                need="exact send approve for this thread",
            )
        return Card(True, path, note=p.note or "ops reply")

    if path == "outreach":
        if p.outreach_paused or not p.outreach_live:
            return Card(
                False,
                path,
                reason="outreach not live",
                need="enable campaign or stay dry",
            )
        if not p.phrase:
            return Card(
                False,
                path,
                reason="missing phrase",
                need="exact campaign approve phrase",
            )
        return Card(True, path, note=p.note or "outreach")

    if path == "money":
        if not p.phrase:
            return Card(
                False,
                path,
                reason="missing phrase",
                need="exact money approve",
            )
        blocking = [h for h in p.holds if "dry" in h.lower() or "pause" in h.lower()]
        if blocking:
            return Card(
                False,
                path,
                reason=f"hold:{blocking[0]}",
                need="clear money hold",
            )
        return Card(True, path, note=p.note or "money")

    if path == "voice":
        if not p.phrase:
            return Card(
                False,
                path,
                reason="missing phrase",
                need="voice ramp approve",
            )
        return Card(True, path, note=p.note or "voice")

    return Card(False, path, reason="unknown path", need="pick mail_send|outreach|money|voice")


def _blocks_mail(hold: str) -> bool:
    h = hold.lower()
    return any(x in h for x in ("mail_paused", "send_frozen", "class_live_paused"))


def _short(s: str, n: int = 48) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"
