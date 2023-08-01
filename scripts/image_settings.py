import subprocess
from picamera import PiCamera


# ss 1800-4000, 100 incr
# iso 300-1000, 100 incr
# awbgains 1.5,2.0 0.1 incr
fli = ["auto","off","50hz","60hz"]
awb = ["off","auto",
       "sun","cloud",
       "shade","tungtsten", 
       "fluorescent", "incandescent", 
       "flash", "horizon", "greyworld"]
exp = ["auto","night","nightpreview",
       "backlight", "spotlight","sports"
       "snow", "beach", "verylong",
       "fixedfps","antishake", "fireworks"]


for ss in range(1800,4000, 100):
    for iso in range(300,1000,100):
        for awbgains in range(15,20): #/10
            for fli_i in range(len(fli)):
                for awb_i in range(len(awb)):
                    for exp_i in range(len(exp)):
                        name = f"ss{ss}ISO{iso}ex{exp[exp_i]}fli{fli[fli_i]}awb{awb[awb_i]}awbgains{awbgains}"
                        line = f"raspistill -ss {ss} -ISO {iso} -ex {exp[exp_i]} -fli {fli[fli_i]} -awb {awb[awb_i]} --awbgains {awbgains} -o {name}.jpg"
                        subprocess.call(line, shell=True)

