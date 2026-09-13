# OpenTelemetry export for Claude Code sessions

This repo captures OTel trace/metric/log data from Claude Code CLI sessions run
against it, for later offline ingestion (trajectory data for the
state-abstraction-certify pipeline itself). Setup follows
https://code.claude.com/docs/en/agent-sdk/observability.

## What the pieces are

- `otel/env.sh` — env vars that turn on telemetry and point the OTLP exporter
  at a local collector. Meant to be `source`d, not executed.
- `otel/collector-config.yaml` — an OpenTelemetry Collector config: an OTLP
  receiver (grpc :4317, http :4318) feeding a `file` exporter per signal.
- `scripts/start_otel_collector.sh` — brings up the collector as a Docker
  container (`otel/opentelemetry-collector-contrib`, not the plain
  `opentelemetry-collector` image — the file exporter only ships in the
  `-contrib` distribution), with `otel/collector-config.yaml` and a local
  `.otel-data/` directory mounted in.

## Required env vars, and why the beta flag matters

`CLAUDE_CODE_ENABLE_TELEMETRY=1` alone only gets you aggregate *metrics*
(counters, no per-call structure). Getting the actual
`claude_code.interaction` → `claude_code.llm_request` /
`claude_code.tool` → `claude_code.tool.execution` span hierarchy — i.e.
trajectory-shaped trace data with one span per tool call — additionally
requires:

```
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
```

Both flags are set in `otel/env.sh`, along with:

```
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

The `console` exporter is not used here — the docs warn it competes with
Claude Code's own message channel on stdout/stderr, so it's unusable
alongside normal interactive use.

## Starting a work session

1. Start the collector (requires Docker running):
   ```bash
   ./scripts/start_otel_collector.sh
   ```
2. In the shell you'll launch `claude` from, load the env vars:
   ```bash
   source otel/env.sh
   ```
   To make this automatic in new shells, add this line to your `~/.zshrc` /
   `~/.bashrc` yourself (not done automatically by tooling in this repo):
   ```bash
   source /Users/nalinguest/state-abstraction-certify/state-abstraction-certify/otel/env.sh
   ```
3. Run Claude Code as usual. Spans/metrics/logs stream to the collector over
   OTLP and land in:
   - `.otel-data/traces.ndjson`
   - `.otel-data/metrics.ndjson`
   - `.otel-data/logs.ndjson`

   (NDJSON: one OTLP export payload, as JSON, per line. `.otel-data/` is
   gitignored — it's local scratch output, not committed.)

4. Stop the collector when done: `docker rm -f sac-otel-collector`.

## Verified

Ran a trivial non-interactive session (`claude -p "run ls, reply done"`)
against this repo with the env vars sourced and the collector up. Confirmed
`.otel-data/traces.ndjson` contains the full span hierarchy — parent
`claude_code.interaction`, with child `claude_code.llm_request` and
`claude_code.tool` spans, and `claude_code.tool` itself parenting a
`claude_code.tool.execution` span for the `Bash` tool call. Structure of the
`claude_code.tool` span observed (IDs/user info redacted):

```json
{
  "traceId": "<redacted>",
  "spanId": "<redacted>",
  "parentSpanId": "<redacted>",
  "name": "claude_code.tool",
  "kind": 1,
  "startTimeUnixNano": "...",
  "endTimeUnixNano": "...",
  "attributes": [
    { "key": "span.type", "value": { "stringValue": "tool" } },
    { "key": "tool_name", "value": { "stringValue": "Bash" } },
    { "key": "tool_name_safe", "value": { "stringValue": "Bash" } },
    { "key": "bash_command_class", "value": { "stringValue": "file_search" } },
    { "key": "bash_argv0", "value": { "stringValue": "ls" } },
    { "key": "tool_use_id", "value": { "stringValue": "<redacted>" } },
    { "key": "gen_ai.tool.call.id", "value": { "stringValue": "<redacted>" } },
    { "key": "duration_ms", "value": { "intValue": "5712" } }
  ]
}
```

Note: real spans also carry `user.email`, `user.account_uuid`,
`organization.id`, and `session.id` attributes — treat `.otel-data/` as
sensitive local output, not something to commit or share verbatim.
