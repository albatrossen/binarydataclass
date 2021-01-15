import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binary-dataclass",
    version="0.1",
    author="Jes Andersen",
    author_email="sindal@gmail.com",
    description="Binary Conversion for dataclass classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albatrossen/binarydataclass",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
