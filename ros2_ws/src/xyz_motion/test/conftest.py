"""pytest configuration for xyz_motion."""

import sys
from pathlib import Path

# Allow `pytest` from package root without prior install.
_PKG_ROOT = Path(__file__).resolve().parents[1]
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))
