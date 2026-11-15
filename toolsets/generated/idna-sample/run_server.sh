#!/bin/sh
# Start these generated tools as an MCP server, in their own environment and sandbox.
# No arguments: stdio. `--http PORT`: Streamable HTTP at http://127.0.0.1:PORT/mcp.
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
ENV_DIR="$ROOT/.cache/envs/idna-sample"
if [ ! -x "$ENV_DIR/bin/python" ]; then
    echo "No environment yet. Run: uv run repo2tools generate https://github.com/kjd/idna --commit d357725082245ff90f5cf8800a3fc297b1f2319a --tag sample --env-only" >&2
    exit 1
fi
PROFILE="$ROOT/.cache/envs/idna-sample.sb"
PREFIX=""
if [ -f "$PROFILE" ] && command -v sandbox-exec >/dev/null 2>&1; then
    exec env -i PATH=/usr/bin:/bin HOME="$ENV_DIR.tmp" TMPDIR="$ENV_DIR.tmp" PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8 \
        sandbox-exec -f "$PROFILE" "$ENV_DIR/bin/python" -I "$HERE/server.py" "$@"
fi
echo "WARNING: running generated code without a sandbox" >&2
exec env -i PATH=/usr/bin:/bin HOME="$ENV_DIR.tmp" TMPDIR="$ENV_DIR.tmp" PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8 \
    "$ENV_DIR/bin/python" -I "$HERE/server.py" "$@"
