from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .types import Action, Event


@dataclass
class WorldEngine:
    scenario_name: str
    state: Dict[str, float | int | str | dict | list] = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    metrics_history: List[Dict[str, float | int | str]] = field(default_factory=list)

    def apply_action(self, step: int, action: Action, timestamp: str, routed_layer: str) -> Event:
        sentiment_delta = float(action.details.get("sentiment_delta", 0.0))
        demand_delta = float(action.details.get("demand_delta", 0.0))
        policy_delta = float(action.details.get("policy_delta", 0.0))
        macro_delta = float(action.details.get("macro_delta", 0.0))
        volatility_delta = float(action.details.get("volatility_delta", 0.0))
        confidence_delta = float(action.details.get("confidence_delta", 0.0))
        liquidity_delta = float(action.details.get("liquidity_delta", 0.0))
        stress_delta = float(action.details.get("stress_delta", 0.0))

        self.state["sentiment_index"] = float(self.state.get("sentiment_index", 0.0)) + sentiment_delta
        self.state["demand_index"] = float(self.state.get("demand_index", 0.0)) + demand_delta
        self.state["policy_signal"] = float(self.state.get("policy_signal", 0.0)) + policy_delta
        self.state["macro_pressure"] = float(self.state.get("macro_pressure", 0.0)) + macro_delta
        self.state["volatility_index"] = max(0.0, float(self.state.get("volatility_index", 0.0)) + volatility_delta)
        self.state["confidence_index"] = float(self.state.get("confidence_index", 0.0)) + confidence_delta
        self.state["liquidity_index"] = float(self.state.get("liquidity_index", 0.0)) + liquidity_delta
        self.state["stress_index"] = max(0.0, float(self.state.get("stress_index", 0.0)) + stress_delta)
        self.state["world_temperature"] = round(
            float(self.state.get("sentiment_index", 0.0)) * 0.45
            + float(self.state.get("demand_index", 0.0)) * 0.35
            - float(self.state.get("stress_index", 0.0)) * 0.2,
            4,
        )
        self.state["system_stability"] = round(
            float(self.state.get("confidence_index", 0.0))
            + float(self.state.get("liquidity_index", 0.0))
            - float(self.state.get("volatility_index", 0.0))
            - float(self.state.get("stress_index", 0.0)),
            4,
        )
        self.state["last_actor"] = action.agent_id

        event = Event(
            step=step,
            source=action.agent_id,
            event_type=action.action_type,
            payload=action.details,
            timestamp=timestamp,
            importance=action.importance,
            routed_layer=routed_layer,
        )
        self.events.append(event)
        self.metrics_history.append(
            {
                "step": step,
                "timestamp": timestamp,
                "actor": action.agent_id,
                "routed_layer": routed_layer,
                "sentiment_index": round(float(self.state.get("sentiment_index", 0.0)), 4),
                "demand_index": round(float(self.state.get("demand_index", 0.0)), 4),
                "policy_signal": round(float(self.state.get("policy_signal", 0.0)), 4),
                "macro_pressure": round(float(self.state.get("macro_pressure", 0.0)), 4),
                "volatility_index": round(float(self.state.get("volatility_index", 0.0)), 4),
                "confidence_index": round(float(self.state.get("confidence_index", 0.0)), 4),
                "liquidity_index": round(float(self.state.get("liquidity_index", 0.0)), 4),
                "stress_index": round(float(self.state.get("stress_index", 0.0)), 4),
                "world_temperature": round(float(self.state.get("world_temperature", 0.0)), 4),
                "system_stability": round(float(self.state.get("system_stability", 0.0)), 4),
            }
        )
        return event

    def snapshot(self) -> Dict[str, float | int | str | dict | list]:
        return dict(self.state)
