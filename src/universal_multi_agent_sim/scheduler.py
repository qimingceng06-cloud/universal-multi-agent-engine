from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List


@dataclass
class EventScheduler:
    start_time: datetime
    step_minutes: int = 5
    scheduled: Dict[int, List[dict]] = field(default_factory=dict)

    def schedule(self, step: int, event: dict) -> None:
        self.scheduled.setdefault(step, []).append(event)

    def pop_step_events(self, step: int) -> List[dict]:
        return list(self.scheduled.pop(step, []))

    def timestamp_for_step(self, step: int) -> str:
        return (self.start_time + timedelta(minutes=self.step_minutes * step)).isoformat()
