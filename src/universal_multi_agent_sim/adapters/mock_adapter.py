from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Dict, List

from .base import AgentAdapter


@dataclass
class MockAgentAdapter(AgentAdapter):
    name: str
    base_importance: float = 0.5
    profile: Dict[str, float] = field(default_factory=dict)
    memory: List[dict] = field(default_factory=list)

    def _memory_signal(self) -> float:
        if not self.memory:
            return 0.0
        deltas = [float(item.get("payload", {}).get("sentiment_delta", 0.0)) for item in self.memory[-3:]]
        return mean(deltas) if deltas else 0.0

    def act(self, observation: dict, context: dict) -> dict:
        pressure = float(observation.get("pressure", 0.0))
        world_state = context.get("world_state", {})
        policy_signal = float(world_state.get("policy_signal", 0.0))
        macro_pressure = float(world_state.get("macro_pressure", 0.0))
        world_temperature = float(world_state.get("world_temperature", 0.0))
        memory_signal = self._memory_signal()

        sensitivity = float(self.profile.get("sensitivity", 1.0))
        resilience = float(self.profile.get("resilience", 0.2))
        layer_multiplier = float(self.profile.get("layer_multiplier", 1.0))
        policy_exposure = float(self.profile.get("policy_exposure", 0.4))
        macro_exposure = float(self.profile.get("macro_exposure", 0.3))
        volatility_bias = float(self.profile.get("volatility_bias", 0.0))
        liquidity_bias = float(self.profile.get("liquidity_bias", 0.0))
        confidence_bias = float(self.profile.get("confidence_bias", 0.0))

        sentiment_delta = (
            self.profile.get("sentiment_bias", 0.0)
            + (pressure * sensitivity)
            + (memory_signal * 0.35)
            - (policy_signal * policy_exposure)
            - (macro_pressure * macro_exposure)
            + confidence_bias
        ) * layer_multiplier
        demand_delta = (
            self.profile.get("demand_bias", 0.0)
            + max(0.0, sentiment_delta * (0.55 + resilience))
            - (macro_pressure * 0.1)
            + liquidity_bias
        )
        policy_delta = self.profile.get("policy_bias", 0.0) + (pressure * float(self.profile.get("policy_reflex", 0.0)))
        macro_delta = self.profile.get("macro_bias", 0.0) + (pressure * float(self.profile.get("macro_reflex", 0.0)))
        volatility_delta = abs(sentiment_delta) * 0.4 + pressure * 0.3 + volatility_bias - resilience * 0.15
        confidence_delta = sentiment_delta * 0.25 - abs(policy_signal) * 0.08 + confidence_bias * 0.5
        liquidity_delta = demand_delta * 0.12 - abs(world_temperature) * 0.04 + liquidity_bias * 0.6
        stress_delta = max(0.0, pressure + macro_pressure - resilience - confidence_bias)

        details = {
            "note": f"{self.name} reacted at step {context.get('step')}",
            "sentiment_delta": round(sentiment_delta, 4),
            "demand_delta": round(demand_delta, 4),
            "policy_delta": round(policy_delta, 4),
            "macro_delta": round(macro_delta, 4),
            "volatility_delta": round(volatility_delta, 4),
            "confidence_delta": round(confidence_delta, 4),
            "liquidity_delta": round(liquidity_delta, 4),
            "stress_delta": round(stress_delta, 4),
            "memory_signal": round(memory_signal, 4),
        }
        return {
            "action_type": self.profile.get("action_type", "respond"),
            "details": details,
            "importance": self.importance_score(),
        }

    def update_memory(self, event: dict) -> None:
        self.memory.append(event)

    def importance_score(self) -> float:
        memory_boost = min(0.15, len(self.memory) * 0.01)
        return round(min(1.0, self.base_importance + memory_boost), 4)
