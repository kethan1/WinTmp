# WinTmp

WinTmp, short for Windows Temperature, is a Python module that enables easy access to the temperatures of the CPU and GPU in Windows. 

This module requires administrator privilages to access the sensor data. Please ensure that your code is run with admin privilages.

Install using `pip`:
`pip install WinTmp`

WinTmp exposes two functions:
 - `CPU_Temp()`
   - Returns the temperature of the CPU as a float.
 - `GPU_Temp()`
   - Returns the temperature of the first GPU found as a float. 

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
