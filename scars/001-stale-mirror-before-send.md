# Scar 001 — Stale mirror before send

**Path:** `mail_send`  
**Outcome:** NO-GO held; customer never got a half-true reply  
**Altitude:** anonymized production pattern (no customer IDs, no private paths)

---

## What happened

An agent drafted a correct-looking reply on a live customer thread. The draft was good. The send path was about to fire.

Live posture said the mailbox **mirror was stale** — the agent’s view of the inbox was lagging the real mailbox. A send from that view risks answering a question that already moved, duplicating a human reply, or missing a newer exception in the thread.

Card:

```text
ARMED-CHECK: NO-GO | path=mail_send | reason=mirror not ok | need=fix mirror or use read-only
```

No send that turn. Human fixed sync. Phrase given. Second card:

```text
ARMED-CHECK: GO | path=mail_send | note=ops reply
```

Then send.

---

## Why the gate mattered

Chat demos treat “good draft” as success. Operator companies treat **fresh channel state + human phrase** as the bar. The draft can be perfect and still must not leave if the I/O plane is lying.

This is the mail-as-front-door point in one incident: the channel is the product surface; the gate is how you keep trust when the model is ready and the mirror is not.

---

## Replay locally

```bash
python -m operator_gates replay 001
# or
operator-gates replay 001
```

---

## What we did *not* open

Customer names, mailbox hosts, fleet paths, regulated fields. The reusable part is the card contract and the refusal to send on stale I/O.
