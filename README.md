# state-abstraction-certify

## Prior work this builds on

This library builds directly on **TraceToChain** (arXiv 2604.24579).

TraceToChain certifies chain adequacy given a state abstraction; this repo
certifies the abstraction itself — a condition called lumpability, from Kemeny &
Snell, that TraceToChain's own goodness-of-fit test can't see because it only
ever observes the already-abstracted process.

## What this is

`state-abstraction-certify` is a pip-installable, OpenTelemetry-native library.
It exposes six capabilities, one per module: `ingest` OTel/OpenInference traces,
`abstract` them into states, `certify` the abstraction by computing a
lumpability defect, `transfer` abstractions across agents, `decide` ship/no-ship
with statistical tests, and `train` to shape RL rewards for GRPO.

## Install

```bash
pip install state-abstraction-certify
```

## Status

Early scaffold. The six modules are stubs; APIs land capability by capability.
