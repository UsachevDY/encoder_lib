# Introduction
Modern encoders have more than one stage of encoding. Developers manually create pipes for converting their text in vector.
But some steps are atomic bricks and can be reuseful.
Beside it some encoding takes a lot of time and we reinvent caches.
Encoder library provide simple way initialization and pipeline construction.   

# Install
```bash
pip install encoder-lib[bert_embedded,bert_client]
```

# Get started
Let's create bert thin client for bert-as-service
```python
from encoders.encoder_factory import EncoderFactory

encoder_conf_dict = {
    "default": {
        "type": "bert_client",
        "input_dim": 1,
        "output_dim": 768,
        "params": {
            "port": 5555,
            "port_out": 5556,
            "ip": "localhost",
            "timeout": 5000, 
        }
   }
}
encoder_factory = EncoderFactory(encoder_conf_dict)

encoder = encoder_factory.get_encoder("default")
documents_list = ["Hello World!"]
vectors = encoder.encode(documents_list)
```
Coll, we have encoder, but each request over network takes time. Let's enhance the encoder and add simple in-memory in cache
```python
from encoders.encoder_factory import EncoderFactory

encoder_conf_dict = {
    "default": {
        "type": "bert_client",
        "input_dim": 1,
        "output_dim": 768,
        "params": {
            "port": 5555,
            "port_out": 5556,
            "ip": "localhost",
            "timeout": 5000, 
        },
        "cache": {
            "type": "simple"
        }
   }
}
encoder_factory = EncoderFactory(encoder_conf_dict)

encoder = encoder_factory.get_encoder("default")
documents_list = ["Hello World!"]
# Encoder sends request over network
vectors = encoder.encode(documents_list)
# This call takes vector from cache 
vectors = encoder.encode(documents_list)
```
Simple cache stores data in memory without any memory restriction.
Beside it we can keep time on warming up and load pre-computed vectors from file:
```python
encoder_conf_dict = {
    "default": {
        "type": "bert_client",
        "input_dim": 1,
        "output_dim": 768,
        "params": {
            "port": 5555,
            "port_out": 5556,
            "ip": "localhost",
            "timeout": 5000, 
        },
        "cache": {
            "type": "simple",
            "params": {
                "path_desc": {
                    "type": "absolute",
                    "file": "/cache/bert_cache.pkl"
                }
            }
        }
   }
}
```

# Path object
Path object is flexible description of file location. Current path object version supports:
1. Absolute path - allow to specify full path to file
     ```yaml
     path_desc:
       type: absolute
       file: full_file_path
    ```

1. Relative path - allow to specify relative path to file. 
    We separate full file name on two parts relative and base. Relative part is stored in param "file".
    Base part is stored in OS environment variable and make you config transferable to other computers.
     ```yaml
     path_desc:
       type: relative
       file: relative_file_name
       os_env: ENV_VAR
    ```
    
    Examples
    ```yaml
    path_desc:
      type: relative
      os_env: BERT_HOME
      file: "cache/bert_cache.pkl"
    ```
   
# Supported vectorisers

1. Bert-as-Service client
1. Bert embedded
1. TF-IDF
1. Composite vectoriser

```yaml
example_bert_client:
  type: bert_client
  input_dim: 1
  output_dim: 768
  params:
    port: 5555
    port_out: 5556
    ip: localhost
    timeout: 5000

example_bert_embedded:
  type: bert_embedded
  verbose: True
  input_dim: 1
  output_dim: 768
  params:
    graph:
      path_desc:
        type: relative
        os_env: BERT_HOME
        file: model_for_inference.pbtxt
    vocab:
      path_desc:
        type: relative
        os_env: BERT_HOME
        file: vocab.txt

example_composite:
  type: composite
  params:
    encoders:
      - example_bert_client

example_tf_idf:
    type: tfidf
    params:
      path_desc:
        type: absolute
        file: /dumped_tf_idf/model.pkl
     
```

# Release notes

## 1.2
1. Added parameter verbose for BaseEncoder and all child classes
1. Added method simple_dump_to_pickle for dumping EncoderCache.

## 1.0
1. Added base functionality for Bert and TF-IDF encoders