from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..adapters.base import AgentAdapter
from ..types import Action, AgentContext


@dataclass
class SimAgent:
    agent_id: str
    adapter: AgentAdapter
    layer_name: str
    cohort_size: int = 1
    metadata: Dict[str, object] = field(default_factory=dict)

    def act(self, observation: dict, context: AgentContext) -> Action:
        result = self.adapter.act(observation, {
            "step": context.step,
            "scenario": context.scenario,
            "world_state": context.world_state,
            "recent_events": context.recent_events,
            "budget_remaining": context.budget_remaining,
            "agent_id": self.agent_id,
            "layer_name": self.layer_name,
            "cohort_size": self.cohort_size,
            **self.metadata,
        })
        return Action(
            agent_id=self.agent_id,
            action_type=result.get("action_type", "observe"),
            details=result.get("details", {}),
            importance=float(result.get("importance", self.adapter.importance_score())),
        )

    def update_memory(self, event: dict) -> None:
        self.adapter.update_memory(event)

    def importance_score(self) -> float:
        return self.adapter.importance_score()
