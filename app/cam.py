import time
from picamera2 import Picamera2
import os
import cv2
import numpy as np

class Picture():       
    def picture(cam):
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
        
        
        picam.start()
        time.sleep(1)

        org_image = picam.capture_image()
        picam.close()
        #open_cv_image = np.array(array)
        #open_cv_image = open_cv_image[:, :, ::-1].copy() 
        

#        image_data = array.astype(np.uint8)
#        print(org_image)
#        image = cv2.imdecode(image_data,1)
        opencv_image = cv2.cvtColor(np.array(org_image), cv2.COLOR_RGBA2BGR)
        print(opencv_image)

        return opencv_image
