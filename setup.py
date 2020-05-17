from setuptools import setup, find_packages
import encoders

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='encoder_lib',
    version=encoders.__version__,
    author="Denis Usachev",
    author_email="usachevdy@yandex.ru",
    url="https://github.com/NightFantom/encoder_lib",
    description='Library for creating encoders pipes',
    long_description=long_description,
    long_description_content_type="text/markdown",
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
