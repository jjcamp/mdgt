from setuptools import setup, find_packages

setup(
    name="mdgt",
    version="0.1.0",
    packages=find_packages(),
    author="John Camp and Contributors",
    description="Microdata-Parsing Microservice",
    url="https://github.com/jjcamp/mdgt",
    keywords="microdata",
    long_description=open('README.md').read(),
    license="MIT",
    install_requires=[
        "lxml >= 3.5.0",
        "requests >= 2.9.1"
    ]
)
