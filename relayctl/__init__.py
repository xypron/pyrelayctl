#!/usr/bin/env python
#
# Copyright (c) 2016, Heinrich Schuchardt <xypron.glpk@gmx.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#	notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#	notice, this list of conditions and the following disclaimer in the
#	documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""PyRelayCtl
PyRelayCtl is a library to control FTDI FT245R based relay boards.
This includes the SainSmart 4-channel 5V USB relay board.
The outlets can be switched on and off via USB.

The library depends on PyUSB (https://github.com/walac/pyusb).

On Debian PyUSB can be installed using

apt-get install python3-usb

Per default, only root is allowed to use devices directly, therefore the
library also only works as root.

To allow group relayctl access create file /lib/udev/rules.d/60-relayctl.rules
with the following content

SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="relayctl", MODE="660", ENV{MODALIAS}="ignore"

Then reload the udev rules with

udevadm control --reload-rules

PyRelayCtl is licensed under a modified BSD license.
"""

import usb.core
import usb.util

def connect():
	"""
	Returns the list of compatible devices.
	@return: device list
	"""
	ret = list()
	ret += list(usb.core.find(find_all=True,
		idVendor=0x0403, idProduct=0x6001))
	return ret

def disable(dev):
	"""
	Disables output to the device.
	Attaches the kernel driver if available.

	@param dev: device
	"""

	if dev.is_kernel_driver_active(0):
		return
	# Disable bitbang mode
	ret = dev.ctrl_transfer(0x40, 0x0b, 0x0000, 0x01, None, 500)
	if ret < 0:
		raise RuntimeError("relayctl: failure to disable bitbang mode")
	try:
		dev.attach_kernel_driver(0)
	except:
		print ("relayctl: could not attach kernel driver")


def enable(dev):
	"""
	Enables output to the device.

	@param dev: device
	"""

	# Detach kernel driver	
	if dev.is_kernel_driver_active(0):
		try:
			dev.detach_kernel_driver(0)
		except:
			raise RuntimeError(
				"relayctl: failure to detach kernel driver")
	# Enable bitbang mode
	ret = dev.ctrl_transfer(0x40, 0x0b, 0x01ff, 0x01, None, 500)
	if ret < 0:
		raise RuntimeError("relayctl: failure to enable bitbang mode")

def getid(dev):
	""" 
	Gets the id of a device.

	@param dev: device
	@return: id
	"""

	if 0 == len(dev.langids):
		langid = 0
	else:
		langid = dev.langids[0]

	return usb.util.get_string(dev, 3, langid)

def getmaxport(dev):
	""" 
	Gets the maximum outlet number of a device.

	@param dev: device
	@return: maximum outlet number
	"""

	return 8

def getminport(dev):
	""" 
	Gets the minimum outlet number of a device.

	@param dev: device
	@return: minimum outlet number
	"""

	return 1

def getstatus(dev, i):
	"""
	Gets the status of outlet i of the device.

	@param dev: device
	@param i: outlet
	@return: status
	"""

	assert i >= getminport(dev) and i <= getmaxport(dev)

	enable(dev)

	buf = bytes([0x00]);

	# Read status
	buf = dev.ctrl_transfer(0xC0, 0x0c, 0x0000, 0x01, buf, 500)
	if len(buf) == 0:
		raise RuntimeError("relayctl: failure to read status")
	
	if (1 << (i - 1)) & buf[0]:
		ret = 1
	else:
		ret = 0

	return ret

def switchoff(dev, i):
	"""
	Switches outlet i of the device off.

	@param dev: device
	@param i: outlet
	"""

	assert i >= getminport(dev) and i <= getmaxport(dev)

	enable(dev)

	buf = bytes([0x00]);

	# Read status
	buf = dev.ctrl_transfer(0xC0, 0x0c, 0x0000, 0x01, buf, 500)
	if len(buf) == 0:
		raise RuntimeError("relayctl: failure to read status")
	
	buf[0] &= ~(1 << (i - 1))

	# Write status
	ret = dev.write(0x02, buf, 500)
	if ret < 0:
		raise RuntimeError("relayctl: failure to write status")

	return

def switchon(dev, i):
	"""
	Switches outlet i of the device on.

	@param dev: device
	@param i: outlet
	"""

	assert i >= getminport(dev) and i <= getmaxport(dev)

	enable(dev)

	buf = bytes([0x00]);

	# Read status
	buf = dev.ctrl_transfer(0xC0, 0x0c, 0x0000, 0x01, buf, 500)
	if len(buf) == 0:
		raise RuntimeError("relayctl: failure to read status")
	
	buf[0] |= (1 << (i - 1))

	# Write status
	ret = dev.write(0x02, buf, 500)
	if ret < 0:
		raise RuntimeError("relayctl: failure to write status")

	return
