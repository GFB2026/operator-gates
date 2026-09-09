# Scar 003 — Irreversible action after the phrase fell out of context

**Path:** `mail_send` (also money)  
**Outcome:** Draft looked approved; live gate said no — phrase was never in *this* turn’s evidence  
**Altitude:** anonymized; rhymes with public “ask first → context compacted → model just did the job” failures

---

## What happened

An agent had a clean draft and a conversation history that *felt* green. Earlier in the thread, a human had talked about sending. The model treated that atmosphere as permission.

Live posture check asked a narrower question: **is there an exact approve phrase for this mutator in the current turn?** There wasn’t. Prior vibes don’t count.

```text
ARMED-CHECK: NO-GO | path=mail_send | reason=missing phrase | need=exact send approve for this thread
```

No send. Human re-stated the phrase. Then GO.

---

## Why this is not the same as scar 001

| Scar | Lie |
|------|-----|
| 001 stale mirror | Channel state was wrong |
| 002 wrong host | World/machine was wrong |
| **003 missing held phrase** | **Permission was inferred from chat weather** |

Compaction, long threads, and “we already talked about sending” are how irreversible actions sneak out. The fix isn’t a smarter model. It’s making the phrase a **fresh, checkable signal**, not a memory of tone.

---

## Replay

```bash
operator-gates replay 003
```

Shows: phrase=false → NO-GO; phrase=true (+ mirror) → GO. Same card contract; different scar.

---

## What we did not open

Customer thread text, exact phrases, mailbox hosts. The reusable claim: **irreversible paths don’t inherit approval from vibes.**
