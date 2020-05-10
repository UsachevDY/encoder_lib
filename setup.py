from setuptools import setup, find_packages

setup(
    name='encoder_utils_lib',
    version='1.0',
    description='Library for creating encoders pipes',
    packages=find_packages('src/', exclude=["dev_utils"]),
    package_dir={'': 'src'},
    extras_require={
        'bert_embedded': ['bert-experimental==1.0.4'],
        'bert_client': ['bert-serving-client==1.10.0']
    }
)
