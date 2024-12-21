# uPython startup tools

## Setup environment
```
sudo apt install -y python3-pip python3-venv picocom

sudo usermod -a -G dialout $USER
sudo reboot
```
From project root:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

## Flash firmware
Connect Wemos D1 mini board with USB cable.
Run `udevadm info --name /dev/ttyUSB*` to get serial port path. Verify it in the shell scripts.
Run **flash-firmware.sh** to write base uPython firmware.
