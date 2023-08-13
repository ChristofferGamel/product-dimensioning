import time
from picamera2 import Picamera2
import os

class Picture():       
    def picture(filename, cam):
        # Path configuration
        #root_absolute_path = os.path.join("/ram/", filename)

        picam = Picamera2(camera_num=cam)
        controls = {"ExposureTime": 1600, 
                    "AnalogueGain": 1.2, 
                    "Brightness": 0.08,
                    "Sharpness":3,
                    "AwbMode":5
                    }
        config = picam.create_preview_configuration(main={"size": (2304, 1296)}, controls=controls)
        picam.configure(config)
        
        time.sleep(2)
        picam.start()
        time.sleep(2)

        picam.capture_file(filename)

        picam.close()
        return filename