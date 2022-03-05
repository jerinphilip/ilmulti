from abc import ABC, abstractmethod
from typing import Any, List


class Filter(ABC):
    def __call__(self, data: List[Any]) -> List[Any]:
        return self.filter(data)

    @abstractmethod
    def condition(self, datum: Any) -> bool:
        return True

    def filter(self, data: List[Any]) -> List[Any]:
        return [datum for datum in data if self.condition(datum)]
