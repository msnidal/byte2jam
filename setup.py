from setuptools import setup, find_packages

setup(
    name="byte2jam",
    version="0.1",
    description="Musical sequence byte encoder",
    author="Mark Snidal",
    license="LGPL",

    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',

    packages=find_packages(),
)
