# Fresh install, connected to wifi
echo "-- Setting up! --"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y wget
#sudo apt-get dist-upgrade -y # Might not need this one

# Make sure pip is gucci
sudo apt-get install python3-distutils -y
sudo apt-get install python3-pip -y

# Installing RTL_fm
cd
sudo apt update
sudo apt install git cmake pkg-config libusb-1.0-0-dev sox -y
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo make install
sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
sudo ldconfig
sudo touch /etc/modprobe.d/blacklist-rtl.conf
sudo echo -e "blacklist dvb_usb_rtl28xxu\nblacklist rtl2832\nblacklist rtl2830"  > /etc/modprobe.d/blacklist-rtl.conf

# Setting up other dependencies
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
sudo apt-get install python3-smbus -y
sudo apt-get install python3-opencv -y
sudo apt-get install -y python3-matplotlib
sudo apt install -y python3-picamera2
sudo pip3 install mpu6050-raspberrypi

# Adding NASAcode folder
cd
sudo mkdir NASAcode

# Prompt a reboot
sudo echo -e "\nSetup script complete! Make sure to do a reboot soon\n"

















# old depricated 

# Installing camera support
#echo "-- Installing Arducam Camera Support --"
#sudo wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
#sudo chmod +x install_pivariety_pkgs.sh
#sudo ./install_pivariety_pkgs.sh -p libcamera_dev
#sudo ./install_pivariety_pkgs.sh -p libcamera_apps

# We are gonna be sticking with the stock version of Python for ease of use and compile time, using 3.9.X

# Removing any old installations of python          < Might break other things, not a good idea
#echo "-- Removing old python installations --"
#sudo rm -rf /usr/bin/python2.x as well as python3.x
#sudo rm -rf /usr/lib/python2.x as well as python3.x
#sudo rm -rf /usr/local/lib/python2.x as well as python 3.x  
#sudo apt-get update

# Installing python3.10
#echo "-- Installing Python 3.10 --"
#sudo apt install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev 
#sudo wget https://www.python.org/ftp/python/3.10.10/Python-3.10.10.tar.xz
#sudo tar -xvf Python-3.10.10.tar.xz
#cd Python-3.10.10
#sudo ./configure --enable-optimizations
#sudo make -j 4
#sudo make altinstall

# Make python3.10 default           < Dont do this, just run as python3.10 and pip3.10
#echo "-- Making Python 3.10 Default --"
#cd /usr/bin
#sudo rm python3
#sudo ln -s /usr/local/bin/python3.10 python3
#sudo ln -s /usr/local/bin/python3.10 python