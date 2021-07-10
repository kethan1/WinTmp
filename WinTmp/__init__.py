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


def init_OHM():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "OpenHardwareMonitorLib.dll"
    )
    clr.AddReference(path)
    from OpenHardwareMonitor import Hardware
    hw = Hardware.Computer()
    hw.MainboardEnabled, hw.CPUEnabled, hw.RAMEnabled, hw.GPUEnabled, hw.HDDEnabled = True, True, True, True, True
    hw.Open()
    return hw


def fetch_data(handle):
    out = []
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            thing = parse_sensor(sensor)
            if thing is not None:
                out.append(thing)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                thing = parse_sensor(subsensor)
                out.append(thing)
    return out


def parse_sensor(snsr):
    if snsr.Value is not None:
        if snsr.SensorType == OHM_sensortypes.index("Temperature"):
            HwType = OHM_hwtypes[snsr.Hardware.HardwareType]
            return {"Type": HwType, "Name": snsr.Hardware.Name, "Sensor": snsr.Name, "Reading": u"%s\xb0C" % snsr.Value }


nvidia = False
for sensor in fetch_data(init_OHM()):
    if sensor["Type"] == "GpuNvidia":
        nvidia = True


def get_temperatures():
    temps = {"CPU": {}, "GPU": {}}

    data = fetch_data(init_OHM())

    for sensor_reading in data:
        if sensor_reading["Type"] == "CPU":
            temps["CPU"][sensor_reading["Sensor"]] = sensor_reading["Reading"]
        elif "Gpu" in sensor_reading["Type"]:
            if not nvidia:
                tmp_avg = 0
                for gpu_sensor_reading in temps["Gpu"]:
                    tmp_avg += int(gpu_sensor_reading["Reading"])
                temps["GPU"] = tmp_avg

    return temps


def GPU_Temp():
    if nvidia:
        return list(filter(lambda x: 'GPU Current Temp' in x, subprocess.run("nvidia-smi -q -d temperature", shell=True, capture_output=True).stdout.decode().replace("\r\n", "\n").split("\n")))[0].split(":")[1].strip()
    else:
        try:
            return get_temperatures()["GPU"]
        except KeyError:
            pass


def CPU_Temp(average=True):
    temperatures = get_temperatures()
    if get_temperatures()["CPU"]:  # Makes sure the CPU key is not an empty dictionary
        if average:
            return sum(temperatures["CPU"].values()) / len(temperatures["CPU"].values())
        else:
            return temperatures["CPU"]
