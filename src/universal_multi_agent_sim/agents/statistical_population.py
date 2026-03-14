from __future__ import annotations

from dataclasses import dataclass

from .base import SimAgent


@dataclass
class MacroStatisticalPopulation(SimAgent):
    layer_name: str = "Layer 4 Macro Statistical Population"
