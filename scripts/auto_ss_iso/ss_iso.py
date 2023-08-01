import subprocess
from picamera import PiCamera
import os


# ss 1800-4000, 100 incr
# iso 300-1000, 100 incr
# awbgains 1.5,2.0 0.1 incr

index = 0


for ss in range(1000, 8000, 350):
    for ISO in range(100, 1000, 40):
        index += 1
        name = f"ss{ss}ISO{ISO}"
        line = f"raspistill -ss {ss} -ISO {ISO} -ex auto -fli 50hz -awb auto -o {name}.jpg"
        if os.path.exists(name + ".jpg"):
            print(f"Index: {index} already exists")
            pass
        else:
            print(f"Index: {index}, Image: ",name)
            print(f"Index: {index}, Command: {line}")
            subprocess.call(line, shell=True)

