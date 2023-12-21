import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

setuptools.setup(
    name="WinTmp",
    version="1.0.0",
    author="Kethan",
    author_email="kethan@vegunta.com",
    description="A package used to get temperature on Windows Machines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=reqs,
    packages=["WinTmp"],
    package_dir={"WinTmp": "WinTmp"},
    package_data={"WinTmp": ["*.dll"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
