from typing import List, Iterable, Any

from encoders.base_encoder import BaseEncoder


class CompositeEncoder(BaseEncoder):

    def __init__(self, encoders: List[BaseEncoder], verbose=False):
        super().__init__(verbose)
        self.__encoders = encoders

    def input_dim(self) -> int:
        first_encoder = self.__encoders[0]
        return first_encoder.input_dim()

    def output_dim(self) -> int:
        last_encoder = self.__encoders[-1]
        return last_encoder.output_dim()

    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        for encoder in self.__encoders:
            data = encoder.encode(data)
        return data
