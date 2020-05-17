from typing import Dict, Iterable, Any

import numpy as np

from encoders.base_encoder import BaseEncoder


class EncoderCache(BaseEncoder):

    def __init__(self, encoder: BaseEncoder, cache: Dict[str, np.array] = None, verbose=False) -> None:
        super().__init__(verbose)
        self.encoder = encoder
        self.cache = cache or {}

    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        result = []
        for el in data:
            vector: np.array = self.cache.get(el)
            if vector is None:
                vector = self.encoder.encode([el])
                vector = vector[0]
                self.cache[el] = vector
            result.append(vector)
        return np.array(result)

    def input_dim(self) -> int:
        return self.encoder.input_dim()

    def output_dim(self) -> int:
        return self.encoder.output_dim()
