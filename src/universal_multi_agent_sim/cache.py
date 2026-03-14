from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class SemanticCache:
    store: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any:
        return self.store.get(key)

    def put(self, key: str, value: Any) -> None:
        self.store[key] = value
