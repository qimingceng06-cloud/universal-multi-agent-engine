from universal_multi_agent_sim.memory import MemoryManager
from universal_multi_agent_sim.types import Event


def test_memory_manager_rolls_to_long_term_memory():
    manager = MemoryManager(window_size=2)
    for step in range(3):
        manager.record(
            "agent-1",
            Event(
                step=step,
                source="agent-1",
                event_type="observe",
                payload={"value": step},
                timestamp=f"2026-03-12T09:0{step}:00",
            ),
        )
    recall = manager.recall("agent-1")
    assert len(recall) == 3
    assert recall[0]["payload"] == {"value": 0}
