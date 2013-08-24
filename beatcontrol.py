import socket, collections, logging

'''
Processes messages that are send by the gstreamer level element and sends 
an udp broadcast message that contains only the current peak to the port 6667.
'''
class BeatControl:

	socket = None
	peaks = collections.deque(maxlen=1000)

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def handle_level_message(self, message):
		current = message.structure["rms"]
		peak = reduce(lambda x, y: x + y, current) / len(current)
#		if peak > -48:
#			print peak
		self.peaks.append(peak)
		localMax = reduce(lambda x, y: x if x < y else y, self.peaks); # i.e. -24.112
		localMin = reduce(lambda x, y: x if x > y else y, self.peaks); # i.e. -3.1125
		if (localMax != localMin):
			relative = (peak - localMin) / (localMax - localMin)
			self.socket.sendto(str(relative), ("marvin", 6667))

	def notify_new_song(self):
		logging.debug('Clearing latest peaks')
		self.peaks.clear()
