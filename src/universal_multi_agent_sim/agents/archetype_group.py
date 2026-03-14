from __future__ import annotations

from dataclasses import dataclass

from .base import SimAgent


@dataclass
class ArchetypeGroup(SimAgent):
    layer_name: str = "Layer 3 Archetype Groups"
