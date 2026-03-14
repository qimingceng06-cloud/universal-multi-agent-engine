from __future__ import annotations

from abc import ABC, abstractmethod


class AgentAdapter(ABC):
    @abstractmethod
    def act(self, observation: dict, context: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_memory(self, event: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def importance_score(self) -> float:
        raise NotImplementedError
