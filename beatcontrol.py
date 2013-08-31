import collections, logging, serial

'''
Processes messages that are send by the gstreamer level element and sends 
it them via the serial interface to the arduino
'''
class BeatControl:

	tty = None 
	peaks = collections.deque(maxlen=1000)

	def __init__(self):
		self.tty = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

	def handle_level_message(self, message):
		current = message.structure["peak"]
		peak = reduce(lambda x, y: x + y, current) / len(current)
#		if peak > -48:
#		print peak
		self.peaks.append(peak)
		localMax = reduce(lambda x, y: x if x < y else y, self.peaks); # i.e. -24.112
		localMin = reduce(lambda x, y: x if x > y else y, self.peaks); # i.e. -3.1125
		if (localMax != localMin):
#			relative = (peak - localMin) / (localMax - localMin)
			relative = (peak + 40.0) / 40.0

			byte1 = 0
			byte2 = 1
			for i in range(6):
				byte1 += pow(2,i+1) if (relative >= i * 0.1) else 0
				byte2 += pow(2,i+1) if (relative >= 0.5 + i * 0.1) else 0
			self.tty.write(chr(byte1))
			self.tty.write(chr(byte2))

	def notify_new_song(self):
		logging.debug('Clearing latest peaks')
		self.peaks.clear()
