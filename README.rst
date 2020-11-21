solarium
===============================================================================

**RaspberryPi based LED controller for artificial sunlight.**

Setup
-----

Install and enable PiGPIO::

    sudo apt install python3-pip python3-gpiozero python3-pigpio
    sudo systemctl enable pigpiod
    sudo systemctl start pigpiod

Install the package via pip::

    python3 -m pip install solarium


Create launch script::

    sudo nano /etc/systemd/system/solarium.service

Add the following lines::

    [Unit]
    Description=LED controller for artificial sunlight.
    After=pigpiod.service

    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /usr/local/bin/solarium -v -- 35 13  ### Add correct coordinates
    Restart=always

    [Install]
    WantedBy=multi-user.target

Launch script::

    sudo systemctl enable solarium.service
    sudo systemctl start solarium.service

Remote access
-------------

If you have pigpiod's remote access enabled, you can also lauch the script from your
local machine and specify the correct host::

    solarium --host=10.0.0.1 -- 52 13


Sound support
-------------

If you want to play a background sound using the ``--sound`` option,
you will need to install `ffplay`_::

    sudo apt install ffmpeg -y

.. _ffplay: https://ffmpeg.org/ffplay.html

Should you be using an Inter-IC Sound (I2S) board, make sure to run pigpiod's clock
in PMW mode, to ensure PCM is available for audio::

    sudo pygpiod -t 0
