# Scar 002 — Wrong host, wrong truth

**Path:** `other` (ops mutate) · adjacent to `mail_send` when the agent “helps” by writing state  
**Outcome:** NO-GO on acting until the machine pin is explicit  
**Altitude:** anonymized production pattern (no fleet hostnames, no private paths)

---

## What happened

An agent was asked to fix a live config. The path existed on more than one machine in the fleet. Without an explicit pin, it would have written the “obvious” box — the one that answered first — and forked state silently. Same filename, different truth.

We treat that as a gate, not a style preference:

```text
ARMED-CHECK: NO-GO | path=other | reason=host not pinned | need=explicit machine before mutate
```

After the human named the host, the mutate proceeded. No dual-write. No “both sides look fine until Friday.”

---

## Why the gate mattered

Harness demos usually have one filesystem. Operator companies often have several near-identical trees. An agent that can `write_file` without a host pin will eventually fork your company.

Same family as scar 001: **the model can be ready while the I/O plane is lying** — here the lie is which world you’re in.

---

## Replay locally

```bash
operator-gates replay 002
```

---

## What we did *not* open

Machine names, IP maps, client data, regulated fields. The reusable part is: pin the host before any mutate that looks identical across boxes.
