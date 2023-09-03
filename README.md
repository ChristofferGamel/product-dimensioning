# product-dimensioning
# Preparing the Pi
For installing raspbian on the pi, the easiest tool for this, would be Raspberry pi's official imaging tool: https://www.raspberrypi.com/software/
Specifically for this program to run, the OS "Raspberry Pi OS (64-bit), is required, in order for the python packages to run

## SSH and VNC
To enable SSH and VNC connections on the Raspberry pi, enter the following command:

`sudo raspi-config`

Navigate to "Interface options", and enable SSH and VNC
Once done, perform a reboot

`sudo reboot`

### IP adress
To retrieve the Raspberry's IP adress, the following command, will return the Pi's IP adress:
`hostname -I`

### SSH connection
To connect to the pi, using SSH, enter the following command on your device:

`ssh user@ip-adress`

### VNC connection
On your device, enter the Pi's IP adress, and then the given password for the user

## Setting up SSH with GIT
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

## Packages
To install the packages required to run this program, start by updating the system

`sudo apt-get update && sudo apt-get upgrade`

First create a new virtual environment

`python -m venv venv`

And activate it by entering the command:

`source venv/bin/activate`

And install the required packages with the following command:

`pip install -r requirements.txt`

## Camera setup
Firstly make sure the cameras are connected securely with the ArduCam Adapter board

Then disable Legacy camera, and enable I2C

`sudo raspi-config`

Navigate to "Interface options"

Firstly disable Legacy camera
Then enable I2C
When done, reboot the pi
`sudo reboot`

## Boot config setup
To enable the adapter board enter the pi's boot configuration by:

`sudo nano /boot/config.txt`

Find the `camera_auto_detect` And make sure it says `camera_auto_detect=1`
Next, find the `dtoverlay=vc4-kms-v3`, and change it to:
`dtoverlay=camera-mux-4port,cam0-imx708,cam1-imx708`

A working copy of the config file is placed in the /pi directory

## Dual Camera test
To test if the cameras are working properly, a test script is located in the /pi directory named: "cam_test.py", and returns two images named: "cam0.jpg" and "cam1.jpg"

If any issues occur, perform a reboot, and try again
