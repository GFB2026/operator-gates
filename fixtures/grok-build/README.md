# Fixture: Grok Build `PreToolUse` fails open

A `PreToolUse` hook is the only blocking event in Grok Build. If the hook does
not answer cleanly, the tool call runs anyway. This fixture proves it against a
real harness, with a side effect you can check on disk — and adds the case the
docs do not mention: a deny that did everything right and still lost.

## Result

Grok Build 1.0.34 (3736acbc8658) [stable] · Windows · 2026-09-19 · grok-4.6
`--permission-mode default` plus allow rules for the Python interpreter only.
One fixture hook installed per case. The operator's own fleet safety hook was
also in the chain on every run and allowed each time (see excerpts).

| fixture | hook did | tool fired? | should have been | harness log line |
|---|---|---|---|---|
| **deny** (control) | well-formed `{"decision":"deny"}`, exit 2 | **blocked** | NO-GO | `gate hook blocked … reason=operator-gates fixture: NO-GO` |
| **timeout** | slept 8 s against a 5 s limit | **FIRED** | NO-GO | `gate hook failed; ignoring (fail-open) … timed out after 5000ms` |
| **crash** | raised, exit 1 | **FIRED** | NO-GO | `gate hook failed; ignoring (fail-open) … exit code 1: Traceback` |
| **malformed_exit0_allow** | truncated deny JSON, exit 0 | **FIRED** | NO-GO | `hook allowed` — *documented: exit 0 allows* |
| **malformed_exit2** | truncated deny JSON, **exit 2** | **FIRED** | NO-GO | `gate hook failed; ignoring (fail-open) … hook_failure=exit code 1` |

Timeout and crash fail open exactly as xAI documents. The exit-0 row is not a
finding — the docs say exit 0 allows — it is there as the pair to the last row.

The last row is the one to read twice. The hook exited **2**, the documented
deny code. On this Windows box the harness saw the exit as **1** (the deny
control shows the same collapse: `JSON decision is 'deny' but exit code is not
0 or 2 — using JSON decision … exit_code=1`). For the control, the parsed JSON
rescued the deny. Here the stdout was truncated, there was nothing to parse,
and the dispatcher logged `ignoring (fail-open)`. A deny hook that satisfied
the contract still let the tool fire. Reproduced on Windows only so far;
confirm on other platforms before generalising the exit-code collapse.

Evidence: [`results/trace-excerpts.txt`](results/trace-excerpts.txt) (harness
dispatcher/runner lines, credentials redacted) and
[`results/hook-log.jsonl`](results/hook-log.jsonl) (what each hook received on
stdin, with `cwd` and whether it judged itself in scope).

## What the vendor says

docs.x.ai/build/features/hooks, read 2026-09-19:

> Exit code 0 allows the tool call; exit code 2 denies it. … Everything else —
> timeouts, crashes, malformed output — is fail-open: the failure is recorded
> in the session but the tool call proceeds.

> The default timeout is 5 seconds

Claude Code's hook docs, read the same day, describe the same posture in their
own words ("don't count on a stalled hook to act as a gate"; exit 1 "proceeds
with the action"). **This fixture tests Grok Build only.** Nothing here was run
against Claude Code; quote its docs, do not cite this suite for it.

## Why this matters for a card

The operator-gates contract is one card before any irreversible act, and
**no card is a NO-GO**. A harness hook cannot express that: silence means GO,
a slow disk means GO, a truncated pipe means GO even with the right exit code.
So the hook can *decorate* the gate, but the gate has to live where silence
blocks — in the mutator itself, before the send/charge/file call, with the
card as the only way through.

## Side findings

1. **Exit codes on Windows.** `sys.exit(2)` from a hook reached the harness as
   `exit_code=1` in both exit-2 runs. Do not rely on the exit code alone on
   Windows; always print the JSON — and know that if the JSON is truncated,
   you are fail-open anyway.
2. **`--debug-file` writes live credentials in plaintext** — MCP bearer tokens
   and the OAuth access token appear in the session-setup lines. The runner
   only enables it with `OG_DEBUG=1`, redacts every trace in a `finally`
   (including on Ctrl-C), scrubs `stderr_tail` before it reaches
   `results.json`, and warns if credential-shaped residue survives. Do not
   `grok trace upload` a raw trace.

## Run it yourself

Requires `grok` on PATH and Python 3.10+. The folder must have a path
*segment* named `og-fixtures` (`~/blog-fixtures` does not count): the hooks
self-scope on that segment, log every invocation with `cwd`, and exit 0
without acting anywhere else, so one left installed by accident is inert.

```bash
mkdir og-fixtures && cp -r fixtures/grok-build/* og-fixtures/ && cd og-fixtures
python run.py                    # all five cases, ~1–2 minutes, five short model calls
python run.py malformed_exit2    # one case; the deny control always runs first
OG_DEBUG=1 python run.py         # also capture (redacted) harness traces
```

Each case installs `~/.grok/hooks/og-fixture.json` for one headless call and
removes it in a `finally`. The runner reports `hook ran in scope` from the
hook's own log line, not from the marker file, so a hook that never executed
cannot masquerade as fail-open. Exit status is non-zero if any row disagrees
with the expected outcome. Outputs: a markdown table, `results.json`,
`hook-log.jsonl`, and with `OG_DEBUG=1` a redacted `trace-<case>.log`.

`--permission-mode default` is passed explicitly so the row reads the same
regardless of your `config.toml`; it does not disable other hooks in
`~/.grok/hooks`, which is why the fleet hook appears in the traces.
