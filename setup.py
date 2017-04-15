from setuptools import setup, find_packages

setup(
    name="LIA",
    version="0.9",
    author="Ryan Himmelwright",
    author_email="ryan.himmelwright@gmail.com",
    url='http://github.com/himmAllRight/LIA',
    description="An assistant to help convert/import data to ledger-cli",
    license="GPL-3.0",
    keywords="ledger",
    packages=['lia'],
    scripts=['lia2']
)
