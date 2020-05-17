import logging
from encoders.cache_encoder import EncoderCache
import pickle


def simple_dump_to_pickle(cache: EncoderCache, path: str) -> None:
    """
    Dump cache in pickle file
    :param cache: Cache
    :param path: Full file name in which you want to save cache
    """
    if isinstance(cache, EncoderCache):
        with open(path, mode="wb") as file:
            pickle.dump(cache.cache, file)
    else:
        logging.error(f"Cache {cache.__class__}. Expected: EncoderCache")
