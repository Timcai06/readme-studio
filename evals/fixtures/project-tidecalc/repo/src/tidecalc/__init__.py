"""Tide predictions from harmonic constituents."""
import math
from dataclasses import dataclass

__version__ = "0.4.1"
SPEEDS = {"M2": 28.9841042, "S2": 30.0, "N2": 28.4397295, "K1": 15.0410686, "O1": 13.9430356}


@dataclass
class Constituent:
    name: str
    amplitude: float  # metres
    phase: float      # degrees


def predict(constituents, hours, datum=0.0):
    """Water level (m) at each hour offset: datum + sum(A*cos(speed*t - phase))."""
    out = []
    for t in hours:
        h = datum
        for c in constituents:
            h += c.amplitude * math.cos(math.radians(SPEEDS[c.name] * t - c.phase))
        out.append(round(h, 3))
    return out


def load_csv(path):
    rows = [line.strip().split(",") for line in open(path) if line.strip() and not line.startswith("#")]
    return [Constituent(n, float(a), float(p)) for n, a, p in rows[1:]]
