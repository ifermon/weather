# weather
RaspberryPi weather station. Temp/Humid, light sensor, camera

This doesn't have everything, and I have not recently tested it, but below is a set of directions for setting up yur weather station.

Create raspberry sd card from image (on mac)
Get image from rasberrypi.org
Download and extract it to local computer
Now image the sd card using:
sudo dd bs=1m if=path_of_your_image.img of=/dev/diskn

Now put the card into the raspberry pi plug it in. Connect your Pi into a WIRED connection. It doesn’t matter where, go to your home router and plug it in right there. You will setup WIFI later.

Go to a terminal on another computer
I’m assuming a mac here
On a PC try Putty
On a chromebook just go to a terminal using ctrl+alt+t

You need to find out the IP address of the pi (hint, use fing on your phone, look for the entry with RaspberrPi as the vendor)
Log in:
ssh pi@IP ADDRESS
Default password is “raspberry"

Congratulations, you are now logged into your pi !


Configure the setup using the built in config tool:
run raspi-config
sudo raspi-config
You are now in the config program. Using arrows on your keyboard, change the following:
Select “Expand Filesystem"
Select “Enable Boot to Desktop / Scratch"
Select “Console Text console …"
Select “Advanced Options” (you have to go back to Advanced menu each time)
Select “Update"
Select “Hostname” - enter the name for your computer
Select “Memory Split” - change to 16 since there is no monitor
Select “SPI” - enable
Select “I2C” - enable
Select Device Tree - disable
Select “Internationalization Options"
Set you timezone
Set overclock to Turbo (or Pi2)
Select “Finish"

Update and configure you local environment 
Now we are back at the command line.

Let’s upgrade / update our software:

sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get update
sudo rpi-update
sudo apt-get install bootlogd

I prefer to use vi as my editor, only do this if you  use vi. If you don’t know what vi is then ignore this.
sudo apt-get install vim
git config --global core.editor "vi"
git config --global user.email "github-ifermon@sneakemail.com"
git config --global user.name "Ivan"
git clone https://github.com/ifermon/config.git
sudo update-alternatives --config editor

Security
We are going the simple route, everything we do will be under the same account.
This is not a best practice from a security standpoint, If you want tighter security there are lots of sites that can give you advice on what to do to make things more secure.

We are going to stick with the basics - a new username and change the default password.

First, create a new user so you can make changes to pi account
In the terminal, type the following:

Add a new user  - remember the password:
sudo adduser <new user name> —ingroup pi

Now give the new user sudo permissions, this allows the user to act as a system administrator
sudo visudo
** Change the line starting with “pi”: change pi to your new username **
** save and exit **

in the command line we are going to exit out and log back in:
exit
ssh <new user name>@IP ADDRESS

Now add your new user to some security groups - will make it easier to view log files and such
sudo usermod -a -G root,adm <new username>

Now we need to delete pi
sudo deluser pi

Make sure to note your username and password. You believe you will always remember, you won’t.

Done! You’ve now just taken the biggest step you can to increase the security of your pi.

Use your new username to log in from now on:
ssh <new username>@IP ADDRESS
You will have to do this every time you reboot the pi

** You'll have to figoure out networking on your own **

Load Modules at Boot
Edit the /etc/modules file and add the following:
sudo nano /etc/modules
i2c-dev
i2c-bcm2708

Install Watchdog
Watchdog is a hardware module that should automatically reboot your pi if it hangs. This is *very* convienent if it is somewhere that is difficult to get to. It was installed above, now you need to make sure it starts:
sudo apt-get install watchdog
sudo update-rc.d watchdog defaults

Install Motion
CHECK OUT sudo apt-get install uv4l-webrtc (here)
Only needed if you have a camera:
sudo apt-get install motion
sudo mkdir /var/run/motion
sudo chmod 777 /var/run/motion

Install Python 3.3+ (latest version of python)
I need this for the google authentication. 
First install some needed libraries:
sudo apt-get install libssl-dev
Go to www.python.org -> Downloads -> (latest version) -> copy link of gzipped tarball
From home directory
mkdir tmp
cd tmp
wget <link of tarball>
tar -xvf <name of tarball>
cd <dir created by tar>
vi README
Read and follow instructions

Install pigpio 
Instructions here
wget abyz.co.uk/rpi/pigpio/pigpio.zip

For Weather Station:
sudo pip3 install gspread oauth2client
For smbus go here
sudo pip3 install requests

More info here.
sudo apt-get install python-pip git python-dev python-dateutil python-smbus i2c-tools build-essential python-rpi.gpio 

sudo pip install pyephem pytz plivo virtualenv flask

Enable i2c (remove from blacklist / uncomment out)
sudo  nano /etc/modprobe.d/raspi-blacklist.conf

Headless Setup:
For headless access (only ssh), you can remove the following:
alsa-base alsa-utils cups-bsd cups-client cups-common debian-reference-common debian-reference-en desktop-base desktop-file-utils dillo galculator gconf-service gconf2 gconf2-common gnome-icon-theme gnome-themes-standard gnome-themes-standard gpicview gsettings-desktop-schemas gtk2-engines:armhf hicolor-icon-theme idle idle idle3 leafpad leafpad libcups2:armhf libcupsimage2:armhf libgail-3-0:armhf libgail18:armhf libgconf-2-4:armhf libgnome-keyring0:armhf lightdm lxappearance lxde lxde-common lxde-core lxde-icon-theme lxinput lxmenu-data lxpanel lxpolkit lxrandr lxsession lxsession-edit lxshortcut lxshortcut lxtask lxterminal menu-xdg midori netsurf-common netsurf-gtk obconf omxplayer openbox penguinspuzzle pistore plymouth raspberrypi-artwork smartsim tk8.5 whiptail wpagui x11-common x11-utils x11-xserver-utils xarchiver xarchiver xauth xdg-utils xfonts-encodings xfonts-utils xinit xpdf xserver-common xserver-xorg xserver-xorg-core xserver-xorg-video-fbdev xterm zenity

Then run apt-get autoremove and apt-get purge


