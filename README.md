# WinTmp

WinTmp, short for Windows Temperature, is a Python module that provides easy access to the temperatures of the CPU and GPU in Windows.

This module requires administrator privilages to access the sensor data as it uses LibreHardwareMonitor internally. Please ensure that your code is run with admin privilages.

Install using `pip`:
`pip install WinTmp`

WinTmp exposes two functions:

- `CPU_Temp()`
  - Returns the temperature of the first CPU as a float.
- `GPU_Temp()`
  - Returns the temperature of the first GPU found as a float.
- `CPU_Temps()`
  - Returns the temperatures of all the CPUs as a list of floats.
- `GPU_Temps()`
  - Returns the temperature of all the GPUs as a list of floats.

In admin command prompt type `python`.
Demo:

```python
>>> import WinTmp
>>> print(WinTmp.CPU_Temp())
38.0
>>> print(WinTmp.GPU_Temp())
35.0
>>>
```

PyPI: https://pypi.org/project/WinTmp/

Github: https://github.com/kethan1/WinTmp/

If you experience any issues, bugs, or shortcomings with this module, please don't hesitate to open an issue!
