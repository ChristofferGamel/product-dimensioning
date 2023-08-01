import subprocess
from picamera import PiCamera


# ss 1800-4000, 100 incr
# iso 300-1000, 100 incr
# awbgains 1.5,2.0 0.1 incr
fli = ["auto","off","50hz","60hz"]
awb = ["off","auto",
       "sun","cloud",
       "shade","tungsten", 
       "fluorescent", "incandescent", 
       "flash", "horizon", "greyworld"]
exp = ["auto","night","nightpreview",
       "backlight", "spotlight","sports",
       "snow", "beach", "verylong",
       "fixedfps","antishake", "fireworks"]

index = 0


for fli_i in range(len(fli)):
    for awb_i in range(len(awb)):
        for exp_i in range(len(exp)):
            index += 1
            iso = 500
            ss = 2500
            name = f"ss{ss}ISO{iso}ex{exp[exp_i]}fli{fli[fli_i]}awb{awb[awb_i]}"
            line = f"raspistill -ss {ss} -ISO {iso} -ex {exp[exp_i]} -fli {fli[fli_i]} -awb {awb[awb_i]} -o {name}.jpg"
            print(f"Index: {index}, Image: ",name)
            print(f"Index: {index}, Command: {line}")
            subprocess.call(line, shell=True)

