from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

from .types import Event


class JsonlEventLogger:
    def __init__(self, output_dir: str) -> None:
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.events_file = self.output_path / "events.jsonl"
        self.summary_file = self.output_path / "summary.json"
        self.metrics_file = self.output_path / "metrics.json"

    def write_events(self, events: Iterable[Event]) -> None:
        with self.events_file.open("w", encoding="utf-8") as handle:
            for event in events:
                handle.write(json.dumps({
                    "step": event.step,
                    "source": event.source,
                    "event_type": event.event_type,
                    "payload": event.payload,
                    "timestamp": event.timestamp,
                    "importance": event.importance,
                    "routed_layer": event.routed_layer,
                }) + "\n")

    def write_summary(self, summary: dict) -> None:
        with self.summary_file.open("w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)

    def write_metrics(self, metrics: Sequence[dict]) -> None:
        with self.metrics_file.open("w", encoding="utf-8") as handle:
            json.dump(list(metrics), handle, indent=2)
