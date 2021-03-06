from setuptools import setup, find_packages

setup(
    name="byte2jam",
    version="1.0",
    description="Musical sequence byte encoder",
    author="Mark Snidal",
    author_email="mark.snidal@gmail.com",
    license="LGPL",
    install_requires=['abjad'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages()
)
