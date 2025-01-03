from setuptools import setup, find_packages

setup(
    name="TALDCommands",
    version="0.1.0",
    author="Mohamed Rayan Ettaldi",
    author_email="taldtool06@gmail.com",
    description="This module contains suspicious patterns.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="TALDCommands/TALDCommands/TALDCommands.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
