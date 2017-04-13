from setuptools import setup, find_packages

setup(
        name="LIA",
        version="0.9",
        author="Ryan Himmelwright",
        author_email="ryan.himmelwright@gmail.com",
        description="An assistant to help convert/import data to ledger-cli",
        url='ryan.himmelwright.net',
        license="GPL-3.0",
        
        packages=['lia'],
        scripts=['lia.py'],
        keywords="ledger",        
)
