Connecting to Google Sheets
===========================

Getting the Template
--------------------
Follow this link - https://bit.ly/GSheetBellTemplate and make a copy

.. image:: TemplateMakeACopy.png
    :width: 30%
    :align: center
    :alt: Under File, Make a Copy

You can have an explore how it works, but the time inputs are next:

Rules for time formatting
-------------------------

Must be a 4 characters long, 24 hour and be separated by a colon

:EG:

| 8:45 am: ``08:45``
| 2:30 pm: ``15:30``

Google Cloud Platform
---------------------
If you have used GCloud before, you can skip this little section.

Go to `GCloud Console <https://console.cloud.google.com/>`_, accept the terms and conditions.
Now go to the `Google Sheet Quickstart <https://developers.google.com/sheets/api/quickstart/python>`_, click enable google sheet API.
Use the desktop client. Now save the Client ID and Client Secret somewhere and download the Client Configuration.

Next we need to generate the Token and the easiest way to do this is on your computer.

Download the `Repository <https://github.com/Fallstop/GSheetBells>`_ by either Cloning or Downloading a zip.

Open a Terminal (Command Line in windows) and cd to the location of the Local Repository. Make sure you have python3/pip installed and run:

:With Windows\, use python/pip instead of python3/pip3:

::

    pip3 install -r requirements.txt

While that is installing, you can place the credentials you downloaded earlier into the Python folder in the Repository and fill out the config file in the same folder.