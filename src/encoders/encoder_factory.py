import os
import pickle
from typing import Dict, Any

from encoders.adapters.bert_embedded_adapter import BertEmbeddedAdapter
from encoders.adapters.tf_idf_encoder_adapter import TFIDFAdapter
from encoders.base_encoder import BaseEncoder
from encoders.cache_encoder import EncoderCache
from encoders.adapters.bert_thin_client_encoder_adapter import BertClientAdapter
from encoders.composite_encoder import CompositeEncoder
from encoders.encoders_constants import *


class EncoderFactory:

    def __init__(self, config: Dict[str, Any]) -> None:
        self.__config = config
        self.__cache = {}

    def get_encoder(self, key: str) -> BaseEncoder:
        encoder = self.__cache.get(key)
        if encoder is None:
            encoder = self.build_encoder(key)
        return encoder

    def build_encoder(self, key):
        config = self.__config[key]
        encoder_type = config[ENCODER_TYPE]
        verbose = config.get(ENCODER_VERBOSE, False)
        if encoder_type == ENCODER_TYPE_BERT_CLIENT:
            try:
                from bert_serving.client import BertClient
            except ImportError:
                raise ImportError('Bert Embedded is not fully installed, '
                                  'Please use "pip install -U encoder_utils_lib[bert_client]" to install it.')
            encoder = BertClient(**config[ENCODER_PARAMS])
            encoder = BertClientAdapter(encoder, config[ENCODER_INPUT_DIM], config[ENCODER_OUTPUT_DIM], verbose=verbose)
        elif encoder_type == ENCODER_TYPE_TFIDF:
            path = self.__get_path(config[PATH_DESC])
            with open(path, mode="rb") as file:
                tf_idf = pickle.load(file)
            encoder = TFIDFAdapter(tf_idf, verbose=verbose)
        elif encoder_type == ENCODER_TYPE_COMPOSITE:
            params_dict = config[ENCODER_PARAMS]
            encoder_key_list = params_dict[ENCODER_COMPOSITE_ENCODER_LIST]
            encoder_list = []
            for key in encoder_key_list:
                encoder = self.get_encoder(key)
                encoder_list.append(encoder)
            encoder = CompositeEncoder(encoder_list, verbose=verbose)
        elif encoder_type == ENCODER_TYPE_BERT_EMBEDDED:
            try:
                from bert_experimental.feature_extraction.bert_feature_extractor import BERTFeatureExtractor
            except ImportError:
                raise ImportError('Bert Embedded is not fully installed, '
                                  'Please use "pip install -U encoder_utils_lib[bert_embedded]" to install it.')
            params_dict = config[ENCODER_PARAMS]
            graph_path = self.__get_path(params_dict[BERT_EMBEDDED_GRAPH][PATH_DESC])
            vocab_path = self.__get_path(params_dict[BERT_EMBEDDED_VOCAB][PATH_DESC])
            seq_len = params_dict.get(BERT_EMBEDDED_MAX_SEQ_LEN, 25)

            encoder = BERTFeatureExtractor(graph_path, vocab_path, seq_len=seq_len)
            encoder = BertEmbeddedAdapter(encoder, config[ENCODER_INPUT_DIM], config[ENCODER_OUTPUT_DIM], verbose=verbose)
        else:
            raise ValueError(f"Not support encoder type {encoder_type}")

        encoder = self.wrap_in_cache(config, encoder)
        self.__cache[key] = encoder
        return encoder

    def wrap_in_cache(self, config, encoder):
        cache_description = config.get(CACHE_DESC)
        if cache_description:
            cache = None
            if cache_description[CACHE_TYPE] == CACHE_TYPE_SIMPLE:
                params = cache_description.get(CACHE_PARAMS)
                if params:
                    path_desc = params[PATH_DESC]
                    if path_desc:
                        path = self.__get_path(path_desc)
                        if os.path.exists(path):
                            with open(path, mode="rb") as file:
                                cache = pickle.load(file)
                if cache is None:
                    cache = {}
                encoder = EncoderCache(encoder, cache)
        return encoder

    def __get_path(self, config: Dict[str, Any]) -> str:
        path_type = config[PATH_TYPE]
        if path_type == PATH_TYPE_RELATIVE:
            base_path = os.environ[config[PATH_OS_ENV]]
            relative_path = config[PATH_FILE_NAME]
            path = os.path.join(base_path, relative_path)
        elif path_type == PATH_TYPE_ABSOLUTE:
            path = config[PATH_FILE_NAME]
        else:
            raise ValueError(f"Not support path type {path_type}")
        return path
