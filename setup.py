# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pineapple',
    version='0.1.0',
    description='Chinese Poker: Pineapple variant',
    long_description=readme,
    author='Kevin Carlis',
    author_email='kevcarlis@gmail.com',
    url='https://github.com/KevinCarlis/pineapple.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
