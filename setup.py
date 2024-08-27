import os
from setuptools import setup, find_packages

install_requires = []

if os.name == "nt":
    install_requires.append("winloop")
elif os.name == "posix":
    install_requires.append("uvloop")

setup(
    name="winuvloop",
    version="0.1.1",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
    ],
)
