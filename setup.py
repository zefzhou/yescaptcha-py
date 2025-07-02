from setuptools import setup, find_packages

setup(
    name="yescaptcha-py",
    version="0.0.3",
    author="zefzhou44",
    author_email="zefzhou44@gmail.com",
    description="yescaptcha python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zefzhou/yescaptcha-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
    install_requires=[
        "loguru>=0.7.2",
        "Requests>=2.32.3",
        "aiohttp>=3.12.13",
    ],
)
