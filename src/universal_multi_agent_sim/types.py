from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class Event:
    step: int
    source: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: str
    target: Optional[str] = None
    importance: float = 0.0
    routed_layer: Optional[str] = None


@dataclass(slots=True)
class Action:
    agent_id: str
    action_type: str
    details: Dict[str, Any]
    importance: float = 0.0


@dataclass(slots=True)
class AgentContext:
    step: int
    scenario: str
    world_state: Dict[str, Any]
    recent_events: List[Dict[str, Any]] = field(default_factory=list)
    memory: List[Dict[str, Any]] = field(default_factory=list)
    budget_remaining: float = 1.0


@dataclass(slots=True)
class SimulationConfig:
    scenario_name: str
    steps: int
    output_dir: str
    budget: float = 1.0
    seed: int = 0
    world: Dict[str, Any] = field(default_factory=dict)
    scheduler: Dict[str, Any] = field(default_factory=dict)
    router: Dict[str, Any] = field(default_factory=dict)
    agents: List[Dict[str, Any]] = field(default_factory=list)
    macro_population: Dict[str, Any] = field(default_factory=dict)
