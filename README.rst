PyRelayCtl
==========

PyRelayCtl is a library to control FTDI FT245R based relay boards.
This includes the SainSmart 4-channel 5V USB relay board.
The outlets can be switched on and off via USB.

The library depends on PyUSB (https://github.com/walac/pyusb).

On Debian PyUSB can be installed using::

    apt-get install python3-usb

Examples
--------

relctl.py is a command line tool to control attached relay boards.

printenv.py shows how to use the library to switch on a computer, read the
U-Boot environment variables and then switch it off again.

Permissions
-----------

Per default, only root is allowed to use devices directly, therefore the
library also only works as root.

To allow group relayctl access create file /lib/udev/rules.d/60-relayctl.rules
with the following content::

    SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="relayctl", MODE="660", ENV{MODALIAS}="ignore"

Then reload the udev rules with::

    udevadm control --reload-rules

License
-------

Copyright (c) 2016, Heinrich Schuchardt <xypron.glpk@gmx.de>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
