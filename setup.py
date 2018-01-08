from setuptools import setup, find_packages

setup(
    name="byte2jam",
    version="0.1",
    description="Musical sequence byte encoder",
    author="Mark Snidal",
    author_email="mark.snidal@gmail.com",
    url="https://snd.al",
    license="LGPL",

    setup_requires=[
        'setuptools-markdown',
    ],
    long_description_markdown_filename='README.md',

    install_requires=[
        'python3-midi',
    ],

    packages=find_packages(),
)
