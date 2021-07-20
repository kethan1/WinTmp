import clr
import os
import subprocess

# List for hardware types and sensor types that our DLL can open
OHM_hwtypes = [
    "Mainboard", "SuperIO", "CPU", "RAM", "GpuNvidia",
    "GpuAti", "TBalancer", "Heatmaster", "SSD"
]
OHM_sensortypes = [
    "Voltage", "Clock", "Temperature", "Load", "Fan", "Flow",
    "Control", "Level", "Factor", "Power", "Data", "SmallData"
]


clr.AddReference(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "OpenHardwareMonitorLib.dll"
))
from OpenHardwareMonitor import Hardware
hw = Hardware.Computer()
hw.MainboardEnabled, hw.CPUEnabled, hw.RAMEnabled, hw.GPUEnabled, hw.HDDEnabled = True, True, True, True, True
hw.Open()


def fetch_data():
    out = []
    for i in hw.Hardware:
        i.Update()
        for sensor in i.Sensors:
            sensor_output = parse_sensor(sensor)
            if sensor_output is not None:
                out.append(sensor_output)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                sensor_output = parse_sensor(subsensor)
                out.append(sensor_output)
    return out


def parse_sensor(snsr):
    if snsr.Value is not None:
        if snsr.SensorType == OHM_sensortypes.index("Temperature"):
            HwType = OHM_hwtypes[snsr.Hardware.HardwareType]
            return {"Type": HwType, "Name": snsr.Hardware.Name, "Sensor": snsr.Name, "Reading": u"%s\xb0C" % snsr.Value}


nvidia = False
for sensor in fetch_data():
    if sensor["Type"] == "GpuNvidia":
        nvidia = True


def get_temperatures():
    temps = {"CPU": {}}

    data = fetch_data()

    for sensor_reading in data:
        if sensor_reading["Type"] == "CPU":
            temps["CPU"][sensor_reading["Sensor"]] = sensor_reading["Reading"]
        elif "Gpu" in sensor_reading["Type"]:
            if not nvidia:
                gpu_temperatues = []
                for gpu_sensor_reading in temps["Gpu"]:
                    gpu_temperatues.append(int(gpu_sensor_reading["Reading"]))
                temps["GPU"] = gpu_temperatues

    return temps


def GPU_Temp(average=True):
    if nvidia:
        return float(list(filter(lambda x: 'GPU Current Temp' in x, subprocess.run("nvidia-smi -q -d temperature", shell=True, capture_output=True).stdout.decode().replace("\r\n", "\n").split("\n")))[0].split(":")[1].strip().strip(" C"))
    else:
        temperatures = get_temperatures()
        if "GPU" in temperatures:
            if average:
                return sum(float(temperature.strip("°C")) for temperature in get_temperatures()["GPU"]) / len(get_temperatures()["GPU"])
            else:
                return [float(temperature.strip("°C")) for temperature in get_temperatures()["GPU"]]


def CPU_Temp(average=True):
    temperatures = get_temperatures()
    if temperatures["CPU"]:  # Makes sure the CPU key is not an empty dictionary
        if average:
            return sum(float(each_cpu_temp.strip("°C")) for each_cpu_temp in temperatures["CPU"].values()) / len(temperatures["CPU"].values())
        else:
            return {key: float(value.strip("°C")) for key, value in temperatures["CPU"].items()}
