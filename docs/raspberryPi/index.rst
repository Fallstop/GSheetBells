The Raspberry pi
================

This is really up to you on which one you use, you can just use any slow ones sitting around, although make sure it *dose* have an ethernet port (You can use wifi, it’s just more prone to password changes etc). I used an old raspberry pi 2 in my case.
You also need the SD card to act as the system drive.

Raspberry pi photo here

Installing Raspbian
-------------------

Go follow this guide to create a bootable raspbian sd card, you want to install Raspberry Pi OS Lite, under the Raspberry Pi OS (Other) tab.
https://www.raspberrypi.org/documentation/installation/installing-images/

Now with the operating system on the SD card, place a file name ``ssh`` with no extension into the boot partition on the SD card.

Configuring the Pi for operation
--------------------------------

First, we need to connect. Plug in the Raspberry Pi into ethernet. Next on another computer that is on the same network, open a terminal (It's called command line on windows) and try running ``ssh pi@raspberrypi`` to open a remote session to the Raspberry Pi. Enter the default password ``raspberry``.

.. note::  If this dose not work, then make sure the ethernet is plugged in properly and if it still dose not work, plug in a monitor and keyboard, log in, and run ''ip address'' to find the ip address, then try again on the other computer: ``ssh pi@[Ip address here]``. If all fails, run the next commands manually and enable manually in the `raspi-config -> Interfacing options` menu.

First, change the password and hostname
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Enter ``sudo raspi-config``, use the arrow keys and enter to enter the network sub-menu. Change the Hostname something relevant (make sure to make a note). Wait then enter the Interfacing options and enable **I2C**

First just make sure the dependencies are installed
``sudo apt update && sudo apt install python3 python3-pip screen``

Next clone the code into Raspberry Pi's home directory
``git clone https://github.com/Fallstop/GSheetBells.git``

