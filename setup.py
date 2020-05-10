from setuptools import setup, find_packages

setup(
    name='encoder_lib',
    version='1.0',
    author="Denis Usachev",
    author_email="usachevdy@yandex.ru",
    url="https://github.com/NightFantom/encoder_lib",
    description='Library for creating encoders pipes',
    packages=find_packages('src/', exclude=["dev_utils"]),
    package_dir={'': 'src'},
    extras_require={
        'bert_embedded': ['bert-experimental==1.0.4'],
        'bert_client': ['bert-serving-client==1.10.0']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
