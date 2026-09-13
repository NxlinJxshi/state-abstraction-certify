<!-- Update this file at the end of every future week. -->

# STATUS

## Day 1 (Part 9 checklist)
- [x] Public repo created, README states the TraceToChain thesis
- [x] OTel export configured — `CLAUDE_CODE_ENABLE_TELEMETRY` + `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`
      set via `otel/env.sh`, OTLP → local `opentelemetry-collector-contrib` → file exporter.
      Verified end-to-end: a live session produced `claude_code.interaction` /
      `claude_code.llm_request` / `claude_code.tool` / `claude_code.tool.execution` spans in the
      output file. See `docs/otel-setup.md`.
- [ ] Read TraceToChain end to end (§IV-A, §IX) — manual, mark done yourself, I cannot verify this
- [ ] Acquire Kemeny & Snell, Finite Markov Chains — manual, mark done yourself, I cannot verify this
- [ ] RunPod/Vast account + pricing check — no pricing-check artifact or commit evidence found in
      this repo (searched for "runpod"/"vast.ai"/"pricing" across tracked files and commit log);
      the vLLM bench commit ran on an RTX PRO 4500 SE, which may have been rented, but that's not
      documented here — confirm in STATUS.md yourself

## Week 1 ([M]/[C] deliverables)
- [x] [M] "What is a rollout, formally?" — `notes/week1-rollout.md`
- [x] [C] vLLM harness + throughput plot — `scripts/bench_throughput.py`,
      `scripts/plot_throughput.py`, `scripts/throughput_plot.png` confirmed present on `main`
      after merging in the vLLM bench commit, the README commit, and the CI-workflow branch
      (all three had diverged from a common ancestor onto separate branches; merged cleanly,
      no conflicts, since each touched disjoint files)
