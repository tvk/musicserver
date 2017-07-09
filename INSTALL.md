# Prepare RaspberryPi

(Everything based on raspbian)

### Wlan

Copy this snippet into /etc/network/interfaces (Replaces the 
previous wlan0 config):

```
allow-hotplug wlan0
iface wlan0 inet dhcp
  wpa-ap-scan 1
  wpa-scan-ssid 1
  wpa-ssid "Magrathea"
  wpa-psk "xxx"
```
... and restart.

### raspi-config

* Enable i2c
* Enable SSH-Server
* Set audio to 3.5mm jack

... and restart

(SSH-Access should work now).

Set volume to 100%:
`amixer set PCM — 100%`

# Install packages

`sudo apt-get install python python-webpy python-requests python-smbus python-gst-1.0 python-gst0.10 python-serial python-apscheduler \
  git gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly screen i2c-tools`
  
# Checkout project

`git clone https://github.com/tvk/musicserver.git`

# Start!

`cd musicserver && python ./start.py`
