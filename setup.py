import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="ads-cli",
    version="0.1.0",
    url="https://github.com/smoh/ads_cli",
    license="MIT",
    author="Semyeong Oh",
    author_email="semyeong.oh@gmail.com",
    description="Command-line interface to ADS",
    long_description=read("README.md"),
    # packages=find_packages(exclude=("tests",)),
    py_modules=["ads_cli", "ads_variables", "adsapp"],
    install_requires=["click", "prompt_toolkit"],
    entry_points="""
        [console_scripts]
        ads=ads_cli:cli
        adscli=adsapp:run
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
