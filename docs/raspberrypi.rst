Setting Up The Raspberry pi
===========================

This is really up to you on which one you use, you can just use any slow ones sitting around, although make sure it *dose* have an ethernet port (You can use wifi, it’s just more prone to password changes etc). I used an old raspberry pi 2 in my case.
You also need the SD card to act as the system drive.

.. note:: If you get stuck anywhere on this section, Search engines, like Google, is your friend and will have the answer if you look hard enough.

.. image:: Raspberry-Pi-2-Bare.png
    :width: 50%
    :align: center

Installing Raspbian
-------------------

Go follow this `guide <https://www.raspberrypi.org/documentation/installation/installing-images/>`_ to create a bootable raspbian sd card. Install Raspberry Pi OS Lite, (under the `Raspberry Pi OS Other` tab in there software).

Now with the operating system on the SD card, place a file name ``ssh`` with no extension into the boot partition on the SD card.

Configuring the Pi for operation
--------------------------------

First, we need to connect. Plug in the Raspberry Pi into ethernet. Next on another computer that is on the same network, open a terminal (It's called command line on windows) and try running ``ssh pi@raspberrypi`` to open a remote session to the Raspberry Pi. The default password `raspberry` which we will change soon.

.. note::  If this dose not work, then make sure the ethernet is plugged in properly and if it still dose not work, plug in a monitor and keyboard, log in, and run ''ip address'' to find the ip address, then try again on the other computer: ``ssh pi@[Ip address here]``. If all fails, run the next commands manually and enable manually in the `raspi-config -> Interfacing options` menu.

First, configure the operating system by running:

::

    sudo raspi-config

Use the arrow keys and enter to enter the network sub-menu. Change the Hostname something relevant (make sure to make a note). Wait then enter the Interfacing options and enable **I2C**. Once that is done, the last thing to do in these settings is in the ``Boot Options`` -> ``Desktop / CLI menu`` select ``B1 Console Autologin`` You can then exit raspi-config.
Next you want to change the name of the default user by executing:

::

    sudo passwd

and following the prompts.

Next clone the code into Raspberry Pi's home directory
``git clone https://github.com/Fallstop/GSheetBells.git``
Then configure permissions

::

    chmod +x GSheetBells/BellRinger.sh
    chmod +x GSheetBells/InternetStatus.sh
    chmod +x GSheetBells/StartScripts.sh

After that, install the dependencies using this command:

::

    sudo apt update && sudo apt upgrade && 
    sudo apt install python3 python3-pip screen &&
    sudo pip install -r GSheetBells/requirements.txt

.. note:: This will take ages.

Nice, time to set up the auto start.
For this, we are going to use `Screen <https://www.gnu.org/software/screen/>`_, which allows us to have sessions running in the background that can be connected to.
Edit the start processes by running

::

    sudo nano /etc/profile

and adding this to the end:

::

    cd ~
    sh /home/pi/GSheetBells/StartScripts.sh

Cool, Next up is setting up Google Sheets
