"""CLI entry: check posture or replay a documented scar."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .gate import Posture, check

SCARS = {
    "001": {
        "title": "Stale mirror before send",
        "steps": [
            (
                "mail_send",
                Posture(mirror_ok=False, phrase=True, note="draft ready, mirror lagging"),
                "Agent had a good draft; mirror stale → block",
            ),
            (
                "mail_send",
                Posture(mirror_ok=True, phrase=True, note="ops reply"),
                "Mirror fixed + phrase → allow send",
            ),
        ],
    },
    "002": {
        "title": "Wrong host, wrong truth",
        "steps": [
            (
                "other",
                Posture(host_pinned=False, note="path exists on multiple boxes"),
                "Identical path, no host pin → block",
            ),
            (
                "other",
                Posture(host_pinned=True, note="machine named"),
                "Host pinned → allow mutate",
            ),
        ],
    },
    "003": {
        "title": "Irreversible without held phrase",
        "steps": [
            (
                "mail_send",
                Posture(mirror_ok=True, phrase=False, note="thread felt approved"),
                "Vibes ≠ phrase → block",
            ),
            (
                "mail_send",
                Posture(mirror_ok=True, phrase=True, note="exact phrase this turn"),
                "Fresh phrase → allow send",
            ),
        ],
    },
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="operator-gates",
        description="Fail-closed GO/NO-GO cards for mail/money/outreach paths",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Emit one card from flags or JSON posture")
    p_check.add_argument(
        "path",
        choices=["mail_send", "outreach", "money", "voice", "other"],
    )
    p_check.add_argument("--json", dest="json_path", help="Path to posture JSON file")
    p_check.add_argument("--mirror-ok", action="store_true")
    p_check.add_argument("--phrase", action="store_true")
    p_check.add_argument("--host-pinned", action="store_true")
    p_check.add_argument("--outreach-live", action="store_true")
    p_check.add_argument("--hold", action="append", default=[], help="Repeatable hold id")
    p_check.add_argument("--note", default="")

    p_replay = sub.add_parser("replay", help="Replay a documented scar by id")
    p_replay.add_argument("scar_id", help="e.g. 001")

    p_list = sub.add_parser("scars", help="List scar ids")

    args = parser.parse_args(argv)

    if args.cmd == "scars":
        for sid, meta in SCARS.items():
            print(f"{sid}\t{meta['title']}")
        return 0

    if args.cmd == "replay":
        sid = args.scar_id
        if sid.isdigit() and len(sid) < 3:
            sid = sid.zfill(3)
        if sid not in SCARS:
            print(f"unknown scar: {args.scar_id}", file=sys.stderr)
            print("known:", ", ".join(SCARS), file=sys.stderr)
            return 2
        meta = SCARS[sid]
        print(f"# scar {sid} — {meta['title']}")
        for path, posture, label in meta["steps"]:
            card = check(path, posture)  # type: ignore[arg-type]
            print(f"# {label}")
            print(card)
        return 0

    # check
    posture = _posture_from_args(args)
    card = check(args.path, posture)  # type: ignore[arg-type]
    print(card)
    return 0 if card.go else 1


def _posture_from_args(args: argparse.Namespace) -> Posture:
    if args.json_path:
        data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
        return Posture(
            mirror_ok=bool(data.get("mirror_ok", False)),
            outreach_live=bool(data.get("outreach_live", False)),
            outreach_paused=bool(data.get("outreach_paused", True)),
            holds=list(data.get("holds") or []),
            phrase=bool(data.get("phrase", False)),
            host_pinned=bool(data.get("host_pinned", False)),
            note=str(data.get("note") or ""),
        )
    outreach_live = bool(args.outreach_live)
    return Posture(
        mirror_ok=bool(args.mirror_ok),
        outreach_live=outreach_live,
        outreach_paused=not outreach_live,
        holds=list(args.hold or []),
        phrase=bool(args.phrase),
        host_pinned=bool(args.host_pinned),
        note=args.note or "",
    )


if __name__ == "__main__":
    raise SystemExit(main())
