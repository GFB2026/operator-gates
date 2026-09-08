# operator-gates

**Fail-closed send / money / outreach gates for agent-operated companies.**

Reference patterns from running real businesses with agents on mail, desk, and charges — not a product SKU, not a harness pitch.

Peer desk: [gregfredabytes.com](https://gregfredabytes.com/) · thesis: [agent-operated companies](https://gregfredabytes.com/essay/agent-operated-companies/) · inventory: [what I run](https://gregfredabytes.com/running/)

---

## Why this exists

Harness builders ship shells. Operator companies live where agents already touch **customers and money**. The hard part is not “make the model act” — it is deciding what it is allowed to **send, charge, or promise**, and proving the gate held.

This repo is a thin, forkable shape of that seat:

| Piece | What it is |
|-------|------------|
| `gate.py` | Fail-closed posture check → one-line GO / NO-GO card |
| `examples/` | Mail send, outreach, money path sketches |
| `ANTI_PATTERNS.md` | Operator refuse patterns that keep agents from fighting the human |

No Relish guts. No private fleet paths. Patterns only.

---

## Install / try

```bash
python -m pip install -e .
python -c "from operator_gates import check; print(check(path='mail_send', posture={'mirror_ok': True, 'phrase': True}))"
```

Or run the examples:

```bash
python examples/mail_send.py
python examples/money.py
```

---

## The card (contract)

Every mutator on send / money / outreach emits **exactly one** card first:

```text
ARMED-CHECK: GO | path=mail_send | mirror=ok | phrase=satisfied | note=ops reply
ARMED-CHECK: NO-GO | path=money | reason=missing phrase | need=exact money approve
```

- **NO-GO → block.** Do not send or charge in the same turn.
- **GO → still honor phrase / capability rules.** Infrastructure green ≠ permission invented from chat.

---

## Identity

> I run companies with agents in production — mail, desk, money, human gates.

If you build harness / HITL / agent I/O and this rhyme matters, write: [greg@gregfredabytes.com](mailto:greg@gregfredabytes.com)

X: [@gregfredabytes](https://x.com/gregfredabytes) · GitHub: [GFB2026](https://github.com/GFB2026)

## License

MIT
