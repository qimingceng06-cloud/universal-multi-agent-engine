"""Universal Multi-Agent Simulation Engine MVP package."""

__version__ = "0.1.0"

from .engine import SimulationEngine, run_from_config
from .types import Action, AgentContext, Event, SimulationConfig

__all__ = [
    "__version__",
    "Action",
    "AgentContext",
    "Event",
    "SimulationConfig",
    "SimulationEngine",
    "run_from_config",
]
