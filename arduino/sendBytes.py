#!/usr/bin/python

import serial

tty=serial.Serial("/dev/ttyACM1", 9600, timeout=None)

value=int(tty.readline())
if (value == 1):
	print "pp"

tty.write(chr(1));
tty.write(chr(0));
tty.write(chr(73));

