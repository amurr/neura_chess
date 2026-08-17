# Shared by scripts under scripts/<function>/. Sets ROOT = repo (parent of scripts/).
# Usage from a nested script:
#   # shellcheck source=/dev/null
#   source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/_repo_root.sh"
# shellcheck disable=SC2034
_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${_SCRIPTS_DIR}/.." && pwd)"
SCRIPTS_DIR="${_SCRIPTS_DIR}"
