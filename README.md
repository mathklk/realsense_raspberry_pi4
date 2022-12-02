# librealsense on a Raspberry Pi 4

A step by step instruction for installing [librealsense](https://github.com/IntelRealSense/librealsense/) on a Raspberry Pi 4, or more specifically pyrealsense.

Credit goes to [datasith](https://github.com/datasith), who also made a [tutorial](https://github.com/datasith/Ai_Demos_RPi/wiki/Raspberry-Pi-4-and-Intel-RealSense-D435) about this. 

This repository can be understood as a fork from his wiki entry.

## Hardware

||
---
|Raspberry Pi 4 Model B 8GB Rev 1.4 B|
|64 GB SanDisk SD card|
|Intel Realsense D435 |

## Operating System

- Install Raspberry Pi OS 32-bit installed via the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- If you're doing this in headless mode, the Imager program allows you to conviniently set up WiFi and SSH access.

## Prerequisites

- Start with updating, upgrading, and installing dependencies and tools:
```
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install -y automake libtool cmake libusb-1.0-0-dev libx11-dev xorg-dev libglu1-mesa-dev libssl-dev clang llvm libatlas-base-dev python3-opencv
```

- Expand the filesystem by selecting `Advanced Options > Expand Filesystem`, and select yes to rebooting:
```
sudo raspi-config
```

- (not necessary on the 8 GB Raspberry) Increase swap to 2GB by changing the file below to `CONF_SWAPSIZE=2048`:
```
sudo nano /etc/dphys-swapfile
```
- (not necessary on the 8 GB Raspberry) Apply the change: 
```
sudo /etc/init.d/dphys-swapfile restart swapon -s
```

- Clone the realsense repo and create a new `udev` rule:
```
cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/ 
```

- Apply the change (needs to be run by root):
```
sudo su
udevadm control --reload-rules && udevadm trigger
exit
```

- Add the following lines to the end of your `.bashrc` file (some of these are first needed at later steps):
```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3

export PYTHONPATH=$PYTHONPATH:/usr/local/lib:/home/pi/librealsense/build/wrappers/python
```

- Apply the change:
```
source ~/.bashrc
```

## Installation

- Install `protobuf` — Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data:
```
cd ~
git clone --depth=1 -b v3.10.0 https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j4
sudo make install
cd python
export LD_LIBRARY_PATH=../src/.libs
python3 setup.py build --cpp_implementation 
python3 setup.py test --cpp_implementation
sudo python3 setup.py install --cpp_implementation
sudo ldconfig
protoc --version # libprotoc 3.10.0
```
(Running the python tests might throw errors, but the installation still worked fine for me in the end.)

- Install `libtbb-dev` parallelism library for C++:
```
cd ~
wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
sudo ldconfig
rm libtbb-dev_2018U2_armhf.deb
```

- Change default C/C++ compiler to clang ([#9962](https://github.com/IntelRealSense/librealsense/issues/9962))
```
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
```

- Install RealSense SDK `librealsense`:
```
cd ~/librealsense
mkdir  build  && cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DFORCE_LIBUVC=true -DOTHER_LIBS="-latomic"
make -j4
sudo make install
```
(The DOTHER_LIBS flag might not be required, but I had it from previous attempts to fixing this and it worked so I'm leaving it)

- Install RealSense SDK `pyrealsense2` Python bindings for `librealsense`:
```
cd ~/librealsense/build
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)
make -j4
sudo make install
```

- Change the default compiler back to gcc
```
unset CC
unset CXX
```

## Testing

I've included an example script for using the pyrealsense2 library. Tested with a D435. 

- Download the example python script from this repo
```
cd ~
wget https://raw.githubusercontent.com/mathklk/realsense_raspberry_pi4/master/example.py
chmod +x example.py
```
- Run the script (requires a desktop environment to show the image)
```
./example.py
```
