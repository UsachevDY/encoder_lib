from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseEncoder(ABC):

    @abstractmethod
    def input_dim(self) -> int:
        pass

    @abstractmethod
    def output_dim(self) -> int:
        pass

    @abstractmethod
    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        pass
