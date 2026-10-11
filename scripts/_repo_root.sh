#!/usr/bin/env bash
# Sourced by scripts/*/*.sh: sets ROOT to the neura_chess repo root
# (parent of this scripts/ directory). Override with NEURA_CHESS_ROOT.
ROOT="${NEURA_CHESS_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
export ROOT
