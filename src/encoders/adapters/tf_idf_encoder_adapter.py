from typing import Iterable, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from encoders.base_encoder import BaseEncoder


class TFIDFAdapter(BaseEncoder):

    def __init__(self, tf_idf: TfidfVectorizer, verbose=False) -> None:
        super().__init__(verbose)
        self.__encoder = tf_idf

    def input_dim(self) -> int:
        return 1

    def output_dim(self) -> int:
        return len(self.__encoder.vocabulary_)

    def encode(self, data: Iterable[Any]) -> Iterable[Any]:
        return self.__encoder.transform(data)
