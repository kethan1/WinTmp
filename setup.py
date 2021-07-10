import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WinTmp",
    version="0.0.6",
    author="Kethan",
    author_email="kethan@vegunta.com",
    description="A package used to get temperature on Windows Machines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['pythonnet', 'wmi'],
    include_package_data=True,
    package_data={"OpenHardwareMonitorLib": ['OpenHardwareMonitorLib.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)