from gpiozero import CPUTemperature, DiskUsage
import shutil
import psutil

cpu = CPUTemperature()

while True:
    print(f'CPU Temp: {cpu.temperature} \t CPU {psutil.cpu_percent(4)}% \t Memory used: {psutil.virtual_memory().percent}%')
