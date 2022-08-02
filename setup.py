import pathlib

from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = list(map(str.strip, f.read().split("\n")))[:-1]

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="badger-voter-sdk",
    install_requires=requirements,
    author="SHAKOTN",
    author_email="andrii@badger.com",
    description="Shared code for badger autovoters",
    long_description=README,
    keywords=["badger-voter-sdk"],
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    version="0.0.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    url="https://github.com/Badger-Finance/badger-voter-sdk",
    python_requires=">=3.7,<4",
)
