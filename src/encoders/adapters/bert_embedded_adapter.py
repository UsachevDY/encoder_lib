from typing import Iterable, Any
from encoders.base_encoder import BaseEncoder


class BertEmbeddedAdapter(BaseEncoder):

    def __init__(self, encoder: "BERTFeatureExtractor", input_dim: int, output_dim: int, verbose=False) -> None:
        super().__init__(verbose)
        self.__encoder = encoder
        self.__input_dim = input_dim
        self.__output_dim = output_dim

    def input_dim(self) -> int:
        return self.__input_dim

    def output_dim(self) -> int:
        return self.__output_dim

    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        return self.__encoder(data, verbose=self._verbose)



