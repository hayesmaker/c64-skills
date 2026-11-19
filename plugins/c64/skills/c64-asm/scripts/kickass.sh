#!/usr/bin/env bash
# kickass.sh — build a KickAssembler source into a .prg plus symbol files.
#
#   kickass.sh <source.asm> [output-dir] [-- extra KickAss args]
#
# Writes <output-dir>/<name>.prg, <name>.sym (KickAss symbols) and <name>.vs (VICE
# labels). output-dir defaults to ./build. Exits non-zero, with KickAssembler's error
# message, if the build fails.
#
# KickAss.jar is found from $KICKASS_JAR, then `kickass` / `KickAss.jar` next to a
# `kickass` command on PATH, then common install locations.
set -euo pipefail

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi

src="$1"; shift
outdir="build"
if [[ $# -gt 0 && "$1" != "--" ]]; then outdir="$1"; shift; fi
[[ "${1:-}" == "--" ]] && shift

[[ -f "$src" ]] || { echo "kickass.sh: source not found: $src" >&2; exit 2; }
command -v java >/dev/null || { echo "kickass.sh: java not found — install a JRE (8+), e.g. openjdk" >&2; exit 2; }

find_jar() {
  if [[ -n "${KICKASS_JAR:-}" ]]; then echo "$KICKASS_JAR"; return; fi
  local c
  for c in \
    ./KickAss.jar ./tools/KickAss.jar ./tools/bin/KickAss.jar \
    "$HOME/KickAssembler/KickAss.jar" "$HOME/kickassembler/KickAss.jar" "$HOME/.local/share/KickAssembler/KickAss.jar" \
    /opt/KickAss.jar /opt/KickAssembler/KickAss.jar /opt/kickassembler/KickAss.jar \
    /usr/local/share/KickAssembler/KickAss.jar /usr/share/java/KickAss.jar \
    "/Applications/KickAssembler/KickAss.jar"; do
    [[ -f "$c" ]] && { echo "$c"; return; }
  done
}

jar="$(find_jar || true)"
if [[ -z "$jar" || ! -f "$jar" ]]; then
  cat >&2 <<'EOF'
kickass.sh: KickAss.jar not found.
  Download KickAssembler from https://theweb.dk/KickAssembler/ and either
  set KICKASS_JAR=/path/to/KickAss.jar or place KickAss.jar in ./tools/.
EOF
  exit 2
fi

mkdir -p "$outdir"
outdir_abs="$(cd "$outdir" && pwd)"
name="$(basename "${src%.*}")"

# Absolute -o and -odir: KickAss resolves -o against the CWD but -odir against the source.
set +e
log="$(java -jar "$jar" "$src" \
  -o "$outdir_abs/$name.prg" \
  -odir "$outdir_abs" \
  -symbolfile -vicesymbols \
  "$@" 2>&1)"
status=$?
set -e
# Drop KickAss progress chatter; keep errors, warnings, .print output and memory maps.
printf '%s\n' "$log" | grep -v -E '^(parsing|flex pass|Output pass|pass [0-9]+|Writing |Made |Output dir:|//|$)' || true

if [[ $status -ne 0 ]]; then
  echo "kickass.sh: build FAILED ($src)" >&2
  exit $status
fi
echo "built: $outdir_abs/$name.prg  symbols: $outdir_abs/$name.sym"
