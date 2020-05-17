from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseEncoder(ABC):

    def __init__(self, verbose=False):
        self._verbose = verbose

    @abstractmethod
    def input_dim(self) -> int:
        pass

    @abstractmethod
    def output_dim(self) -> int:
        pass

    @abstractmethod
    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        pass
