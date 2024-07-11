import clr
import os

clr.AddReference(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "LibreHardwareMonitorLib.dll"
    )
)
from LibreHardwareMonitor import Hardware

hw = Hardware.Computer()
hw.IsCpuEnabled = hw.IsGpuEnabled = hw.IsMemoryEnabled = \
    hw.IsMotherboardEnabled = hw.IsStorageEnabled = True
hw.Open()


def GPU_Temp():
    for h in hw.Hardware:
        h.Update()

        if h.HardwareType in (Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
            for sensor in h.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature and "GPU Core" in sensor.Name:
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

        if h.HardwareType in (Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
            for sensor in h.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature and "GPU Core" in sensor.Name:
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
