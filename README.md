# operator-gates

Fail-closed **GO / NO-GO cards** before agents touch mail, money, or outreach.

Not a harness framework. Not a product SKU. A small, forkable contract from running companies where agents already sit on real inboxes and charges.

Peer desk: [gregfredabytes.com](https://gregfredabytes.com/) · essay: [Mail is the front door](https://gregfredabytes.com/essay/mail-as-front-door/) · inventory: [what I run](https://gregfredabytes.com/running/)

---

## Why this exists

Harness builders ship shells. Operator companies live where agents already touch **customers and money**. The hard part is not “make the model act” — it is deciding what it is allowed to **send, charge, or promise**, and proving the gate held.

| Piece | What it is |
|-------|------------|
| `gate.py` | Posture → one-line GO / NO-GO card |
| `operator-gates` CLI | `check` / `replay` / `scars` |
| `scars/` | Anonymized production incidents |
| `ANTI_PATTERNS.md` | Refuse patterns that keep agents from fighting the human |

No Relish guts. No private fleet paths.

### Honest scope

- Not Dex-style thesis depth (`12-factor-agents` grade)
- Not wired to a live boot plane — you pass posture (flags or JSON)
- Proof you run a company is [what I run](https://gregfredabytes.com/running/), not this repo alone

---

## Install / try

```bash
python -m pip install -e .
operator-gates scars
operator-gates replay 001
operator-gates replay 002
operator-gates replay 004
operator-gates check mail_send --phrase          # exits 1 — NO-GO (mirror not ok)
operator-gates check mail_send --mirror-ok --phrase   # exits 0 — GO
operator-gates check other --host-pinned         # exits 0 — GO
```

Or:

```bash
python -m operator_gates replay 001
python examples/stale_mirror.py
python examples/wrong_host.py
```

JSON posture:

```bash
operator-gates check mail_send --json examples/posture.stale.json
```

---

## Scars

### 001 — Stale mirror before send

[`scars/001-stale-mirror-before-send.md`](scars/001-stale-mirror-before-send.md) · essay: [Mail is the front door](https://gregfredabytes.com/essay/mail-as-front-door/)

Good draft; stale mailbox mirror; **NO-GO**; sync + phrase; **GO**. Draft never left on a lying I/O plane.

### 002 — Wrong host, wrong truth

[`scars/002-wrong-host-wrong-truth.md`](scars/002-wrong-host-wrong-truth.md)

Identical path on more than one machine; no host pin; **NO-GO**; pin named; **GO**. Near-identical trees fork companies.

### 003 — Irreversible without held phrase

[`scars/003-irreversible-without-held-phrase.md`](scars/003-irreversible-without-held-phrase.md)

Thread *felt* green; no exact phrase in this turn; **NO-GO**. Vibes don’t authorize send/money. Compaction is how irreversible actions sneak out.

### 004 — Capitulation after disagreement

[`scars/004-capitulation-after-disagreement.md`](scars/004-capitulation-after-disagreement.md) · essay: [Capitulation after disagreement](https://gregfredabytes.com/essay/capitulation-after-disagreement/)

Operator scolds; agent agrees, locks a rule, **stops**. **NO-GO** until spine revised **and** next artifact ships. Disagreement must not be taxed.

```bash
operator-gates replay 004
```

---

## The card (contract)

Every mutator on send / money / outreach emits **exactly one** card first:

```text
ARMED-CHECK: GO | path=mail_send | note=ops reply
ARMED-CHECK: NO-GO | path=mail_send | reason=mirror not ok | need=fix mirror or use read-only
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
