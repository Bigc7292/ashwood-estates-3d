#!/usr/bin/env bash
# Ashwood pre-commit guard (Optimizer Bot). Free, local only.
# Blocks files >95 MB. Warns when staged add >50 MB.
# Runs verify_incremental.py, handoff_guard.py, asset_audit.py.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${ROOT}" ]]; then
  echo "precommit_guard: not inside a git work tree" >&2
  exit 1
fi
cd "$ROOT"

OPT="${ROOT}/optimizer"
MAX_FILE_BYTES=$((95 * 1024 * 1024))
WARN_ADD_BYTES=$((50 * 1024 * 1024))

echo "precommit_guard: scanning staged files..."

# Staged files (Added/Copied/Modified/renamed)
mapfile -t STAGED < <(git diff --cached --name-only --diff-filter=ACMR || true)
if [[ ${#STAGED[@]} -eq 0 ]]; then
  echo "precommit_guard: nothing staged; running read-only audits only."
fi

blocked=0
add_bytes=0
for rel in "${STAGED[@]:-}"; do
  [[ -z "$rel" ]] && continue
  if [[ -f "$rel" ]]; then
    sz=$(wc -c <"$rel" | tr -d ' ')
    add_bytes=$((add_bytes + sz))
    if (( sz > MAX_FILE_BYTES )); then
      echo "BLOCK: $rel is ${sz} bytes (>95 MB). Split or omit; no Git LFS." >&2
      blocked=1
    fi
  fi
done

if (( add_bytes > WARN_ADD_BYTES )); then
  mb=$(python3 -c "print(round(${add_bytes}/1024/1024, 2))")
  echo "WARN: staged add ~${mb} MB (>50 MB). Prefer smaller commits or omit regenerable blobs." >&2
fi

if (( blocked )); then
  echo "precommit_guard: blocked oversized file(s)." >&2
  exit 1
fi

run_py() {
  local script="$1"
  if [[ ! -f "$script" ]]; then
    echo "WARN: missing $script" >&2
    return 0
  fi
  echo "precommit_guard: python3 $script"
  python3 "$script"
}

# Audits: non-zero from asset_audit / handoff breaches fail the commit.
run_py "${OPT}/verify_incremental.py"
run_py "${OPT}/handoff_guard.py"
run_py "${OPT}/asset_audit.py"

echo "precommit_guard: OK"
exit 0
