# product-dimensioning
# SSH and VNC
To enable SSH and VNC connections on the Raspberry pi, enter the following command:

`sudo raspi-config`

Navigate to "Interface options", and enable SSH and VNC
Once done, perform a reboot

`sudo reboot`

## IP adress
To retrieve the Raspberry's IP adress, the following command, will return the Pi's IP adress:
`hostname -I`

## SSH connection
To connect to the pi, using SSH, enter the following command on your device:

`ssh user@ip-adress`

## VNC connection
On your device, enter the Pi's IP adress, and then the given password for the user


