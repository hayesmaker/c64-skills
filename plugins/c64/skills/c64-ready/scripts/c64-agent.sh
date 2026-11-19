#!/usr/bin/env bash
# c64-agent.sh — run the c64-ready agent CLI, wherever it is installed.
#
#   c64-agent.sh <file.prg|.crt|.d64|.c64> [c64-agent options]
#   c64-agent.sh --help
#
# Resolution order:
#   1. $C64_READY_DIR/bin/agent.mjs   (a local clone of github.com/hayesmaker/c64-ready)
#   2. c64-agent on PATH              (npm install -g c64-ready)
#   3. ./node_modules/.bin/c64-agent  (npm install c64-ready in this project)
#   4. npx -y -p c64-ready@^3.2.0 c64-agent
set -euo pipefail

command -v node >/dev/null || { echo "c64-agent.sh: node not found — install Node.js 24+" >&2; exit 2; }
major="$(node -p 'process.versions.node.split(".")[0]')"
if (( major < 22 )); then
  echo "c64-agent.sh: Node $(node -v) is too old — c64-ready needs Node 24+" >&2
  exit 2
fi

if [[ -n "${C64_READY_DIR:-}" ]]; then
  [[ -f "$C64_READY_DIR/bin/agent.mjs" ]] || {
    echo "c64-agent.sh: C64_READY_DIR=$C64_READY_DIR has no bin/agent.mjs (needs c64-ready 3.2.0+)" >&2
    exit 2
  }
  exec node "$C64_READY_DIR/bin/agent.mjs" "$@"
fi
if command -v c64-agent >/dev/null; then exec c64-agent "$@"; fi
if [[ -x ./node_modules/.bin/c64-agent ]]; then exec ./node_modules/.bin/c64-agent "$@"; fi
exec npx -y -p 'c64-ready@^3.2.0' c64-agent "$@"
