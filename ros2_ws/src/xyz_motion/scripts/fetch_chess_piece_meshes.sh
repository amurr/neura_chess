#!/usr/bin/env bash
# Download Staunton chess piece STLs (clarkerubber/Staunton-Pieces, MIT).
set -eo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MESH_DIR="$(cd "${SCRIPT_DIR}/../meshes/chess_pieces/staunton" && pwd)"
RAW="https://raw.githubusercontent.com/clarkerubber/Staunton-Pieces/master/Source/Staunton"
mkdir -p "${MESH_DIR}"
for piece in Pawn Rook Knight Bishop Queen King; do
  out="${MESH_DIR}/$(echo "${piece}" | tr '[:upper:]' '[:lower:]').stl"
  curl -fsSL -o "${out}" "${RAW}/${piece}/${piece}.STL"
done
echo "Installed Staunton source meshes in ${MESH_DIR}"
