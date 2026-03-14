from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List

from .types import Event


@dataclass
class MemoryManager:
    window_size: int = 5
    working_memory: Dict[str, Deque[dict]] = field(default_factory=lambda: defaultdict(deque))
    long_term_memory: Dict[str, List[dict]] = field(default_factory=lambda: defaultdict(list))

    def record(self, agent_id: str, event: Event) -> None:
        bucket = self.working_memory[agent_id]
        bucket.append({
            "step": event.step,
            "event_type": event.event_type,
            "payload": event.payload,
            "importance": event.importance,
        })
        while len(bucket) > self.window_size:
            self.long_term_memory[agent_id].append(bucket.popleft())

    def recall(self, agent_id: str) -> List[dict]:
        return list(self.long_term_memory[agent_id]) + list(self.working_memory[agent_id])
