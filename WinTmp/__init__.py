import clr
import os

if os.path.exists(os.path.join(os.path.abspath(__file__), "_version.py")):
    from WinTmp._version import __version__
else:
    __version__ = "0.0.0"

clr.AddReference(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "LibreHardwareMonitorLib.dll"
    )
)
from LibreHardwareMonitor import Hardware

hw = Hardware.Computer()
hw.IsCpuEnabled = hw.IsGpuEnabled = hw.IsMemoryEnabled = hw.IsMotherboardEnabled = (
    hw.IsStorageEnabled
) = True
hw.Open()

GPU_SENSORS = (
    Hardware.HardwareType.GpuNvidia,
    Hardware.HardwareType.GpuAmd,
    Hardware.HardwareType.GpuIntel,
)


def GPU_Temp():
    for h in hw.Hardware:
        h.Update()

        if h.HardwareType in GPU_SENSORS:
            for sensor in h.Sensors:
                if (
                    sensor.SensorType == Hardware.SensorType.Temperature
                    and "GPU Core" in sensor.Name
                ):
                    return sensor.Value


def CPU_Temp():
    for h in hw.Hardware:
        h.Update()

        if h.HardwareType == Hardware.HardwareType.Cpu:
            for sensor in h.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature:
                    return sensor.Value


def GPU_Temps():
    temps = []
    for h in hw.Hardware:
        h.Update()

        if h.HardwareType in GPU_SENSORS:
            for sensor in h.Sensors:
                if (
                    sensor.SensorType == Hardware.SensorType.Temperature
                    and "GPU Core" in sensor.Name
                ):
                    temps.append(sensor.Value)
    return temps


def CPU_Temps():
    temps = []
    for h in hw.Hardware:
        h.Update()

        if h.HardwareType == Hardware.HardwareType.Cpu:
            for sensor in h.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature:
                    temps.append(sensor.Value)
    return temps


def _all_temps():
    temps = {}
    for h in hw.Hardware:
        h.Update()
        for sensor in h.Sensors:
            if sensor.SensorType == Hardware.SensorType.Temperature:
                key = f"{h.HardwareType}_{sensor.SensorType}"
                if key in temps.keys():
                    temps[key].append(sensor.Value)
                else:
                    temps[key] = [sensor.Value]
    return temps


def _all_sensor_data():
    temps = {}
    for h in hw.Hardware:
        h.Update()
        for sensor in h.Sensors:
            key = f"{h.HardwareType}_{sensor.SensorType}"
            if key in temps.keys():
                temps[key].append(sensor.Value)
            else:
                temps[key] = [sensor.Value]
    return temps
