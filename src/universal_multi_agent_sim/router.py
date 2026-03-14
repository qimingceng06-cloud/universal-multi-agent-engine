from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelRouter:
    layer_thresholds: Dict[str, float]
    budget: float = 1.0

    def route(self, importance: float, event_criticality: float = 0.0, cohort_size: int = 1) -> str:
        score = max(importance, event_criticality)
        if score >= self.layer_thresholds.get("key_individual", 0.8) and self.budget >= 0.2:
            return "Layer 1 Key Individual Agents"
        if score >= self.layer_thresholds.get("templated_adaptive", 0.5) and self.budget >= 0.1:
            return "Layer 2 Templated Adaptive Agents"
        if cohort_size >= 20 or score >= self.layer_thresholds.get("archetype_group", 0.25):
            return "Layer 3 Archetype Groups"
        return "Layer 4 Macro Statistical Population"

    def consume_budget(self, routed_layer: str) -> None:
        burn = {
            "Layer 1 Key Individual Agents": 0.2,
            "Layer 2 Templated Adaptive Agents": 0.1,
            "Layer 3 Archetype Groups": 0.03,
            "Layer 4 Macro Statistical Population": 0.01,
        }[routed_layer]
        self.budget = max(0.0, self.budget - burn)
