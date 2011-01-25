# -*- coding: utf-8 -*-

import usb
from time import sleep

def find_device():
	busses = usb.busses()
	for bus in busses:
		for dev in bus.devices:
			if dev.idVendor == 0x2123 and dev.idProduct == 0x1010:
				return dev

class Missile(object):
	_dev = None
	handle = None

	COMMANDS = {
		'STOP': 0x20,
		'DOWN': 0x01,
		'UP': 0x02,
		'LEFT': 0x04,
		'RIGHT': 0x08,
		'SHOOT': 0x10,
	}

	def __init__(self):
		self._dev = find_device()
		self.handle = self.init_usb_connection()

	def init_usb_connection(self):
		handle = self._dev.open()
		try:
			handle.detachKernelDriver(0) # Should this be iface.interfaceNumber?
		except usb.USBError:
			print "Already detached"
		return handle
	
	def send_message(self, message):
		msg_buffer = [0x02] + [message] + [0] * 6
		print msg_buffer
		print self.handle.controlMsg(usb.TYPE_CLASS | usb.RECIP_INTERFACE | usb.ENDPOINT_OUT, usb.REQ_SET_CONFIGURATION, msg_buffer, usb.DT_CONFIG, 0)

	def stop(self):
		self.send_message(Missile.COMMANDS['STOP'])

	def move(self, direction, s = 0):
		self.send_message(Missile.COMMANDS[direction])
		s = max(s, 0.005) # minimum pause to see some movement
		sleep(s)
		self.stop()

	def up(self, s = 0):
		# experience shows that full up<->down is around 0.76s
		self.move('UP', s)

	def down(self, s = 0):
		# experience shows that full up<->down is around 0.76s
		self.move('DOWN', s)

	def left(self, s = 0):
		# experience shows that full left<->right is around 5s
		# experience shows something like 90° ~ 1.7s
		self.move('LEFT', s)

	def right(self, s = 0):
		# experience shows that full left<->right is around 5s
		# experience shows something like 90° ~ 1.7s
		self.move('RIGHT', s)

	def shoot(self):
		self.send_message(Missile.COMMANDS['SHOOT'])
