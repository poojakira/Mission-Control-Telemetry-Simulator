import logging
import os
from typing import Dict
from skyfield.api import EarthSatellite, load

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TLE_Ingest")

# FIX: resolve the TLE catalog path relative to THIS file's location, not CWD
_DEFAULT_CATALOG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'spacetrack_full_catalog.3le.txt'
)

class TLEProcessor:
    def __init__(self, filepath: str = _DEFAULT_CATALOG):
        self.filepath = filepath
        self.ts = load.timescale()

    def load_catalog(self) -> Dict[str, EarthSatellite]:
        if not os.path.exists(self.filepath):
            logger.error(f"Catalog file missing: {self.filepath}")
            return {}

        satellites = {}
        try:
            # FIX: explicit encoding prevents platform-dependent decode errors
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]

            i = 0
            while i < len(lines) - 2:
                if lines[i+1].startswith('1 ') and lines[i+2].startswith('2 '):
                    name = lines[i]
                    l1 = lines[i+1]
                    l2 = lines[i+2]
                    try:
                        sat = EarthSatellite(l1, l2, name, self.ts)
                        satellites[sat.name] = sat
                    except Exception:
                        pass
                    i += 3
                else:
                    i += 1
            return satellites
        except Exception as e:
            logger.error(f"Error parsing TLE: {e}")
            return {}
