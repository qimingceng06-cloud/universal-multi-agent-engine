from __future__ import annotations

from dataclasses import dataclass

from .base import SimAgent


@dataclass
class TemplatedAdaptiveAgent(SimAgent):
    layer_name: str = "Layer 2 Templated Adaptive Agents"
