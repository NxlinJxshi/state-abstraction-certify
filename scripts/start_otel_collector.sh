#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$REPO_ROOT/.otel-data"
CONTAINER_NAME="sac-otel-collector"

mkdir -p "$DATA_DIR"

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  docker rm -f "$CONTAINER_NAME" >/dev/null
fi

docker run -d \
  --name "$CONTAINER_NAME" \
  -p 4317:4317 \
  -p 4318:4318 \
  -v "$REPO_ROOT/otel/collector-config.yaml:/etc/otelcol-contrib/config.yaml" \
  -v "$DATA_DIR:/data" \
  otel/opentelemetry-collector-contrib:latest

echo "OTel collector running as '$CONTAINER_NAME'."
echo "OTLP endpoints: grpc://localhost:4317, http://localhost:4318"
echo "Span/metric/log output: $DATA_DIR/{traces,metrics,logs}.ndjson"
echo "Stop with: docker rm -f $CONTAINER_NAME"
