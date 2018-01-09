from setuptools import setup, find_packages

setup(
    name="byte2jam",
    version="1.0",
    description="Musical sequence byte encoder",
    author="Mark Snidal",
    author_email="mark.snidal@gmail.com",
    license="LGPL",
    install_requires=[
        'python-midi',
    ],
    test_suite='tests',
    packages=find_packages()
)
