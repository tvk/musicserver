import collections, logging, serial, threading, time

'''
Processes messages that are send by the gstreamer level element and sends 
it them via the serial interface to the arduino
'''
class BeatControl:

	tty = None 
	peak = None
	player = None
	running = True

	# A command which is sent when play/pause is pressed
	CMD__PLAY_PAUSE = 1;

	def __init__(self, config, player):
		self.player = player
		if (config.has_option('beatcontrol', 'port')):		
			self.tty = serial.Serial(config.get('beatcontrol', 'port'), 9600, timeout=None)
			writeThread = threading.Thread(target=self.send_bytes)
			writeThread.daemon = True
			writeThread.start()
			readThread = threading.Thread(target=self.read_bytes)
			readThread.daemon = True
			readThread.start()

	def handle_level_message(self, message):
		current = message.structure["peak"]
		self.peak = reduce(lambda x, y: x + y, current) / len(current)

	def read_bytes(self):
		while True:
			try:
				value=int(self.tty.readline())
				print value
				if (value == self.CMD__PLAY_PAUSE):
					self.player.togglePlayPause()
			except ValueError as e:
				pass
			except OSError as e:
				print e
				

	def send_bytes(self):
		while True:
			byte1 = 0
			byte2 = 1
			if (self.peak is not None):
				relative = (self.peak + 40.0) / 30.0
				self.peak = None;
				byte1, byte2 = self.calculate_bytes_vertical_bar(relative);
			threading.Timer(1.2, self.send_bytes_async, [byte1, byte2]).start()
			time.sleep(0.05)

	def send_bytes_async(self, byte1, byte2):		
		if (self.running and self.tty is not None):
			self.tty.write(chr(byte1))
			self.tty.write(chr(byte2))
		
	def stop(self):
		self.running = False	
		if self.tty is not None:
			self.tty.write(chr(0))
			self.tty.write(chr(1))

	def start(self):
		self.running = True		

	def calculate_bytes_rotating_clock(self, relative):
		byte1 = 0
		byte2 = 1			
		for i in range(6):
			byte1 += pow(2,i+1) if (relative >= i * 0.1) else 0
			byte2 += pow(2,i+1) if (relative >= 0.5 + i * 0.1) else 0
		return byte1, byte2


	def calculate_bytes_horizontally_pulsing_clock(self, relative):
		value = 0
		if (relative >= 0.2): value += pow(2,1)
		if (relative >= 0.4): value += pow(2,2) + pow(2,6)
		if (relative >= 0.6): value += pow(2,3) + pow(2,5)
		if (relative >= 0.8): value += pow(2,4)
		return value, 1 + value



	def calculate_bytes_vertical_bar(self, relative):
		byte1 = 0
		byte2 = 1			
		if (relative >= 1.0/7.0): 
			byte2 += pow(2,1)
		if (relative >= 2.0/7.0): 
			byte1 += pow(2,6)
			byte2 += pow(2,2)
		if (relative >= 3.0/7.0): 
			byte1 += pow(2,5)
			byte2 += pow(2,3)
		if (relative >= 4.0/7.0): 
			byte1 += pow(2,4)
			byte2 += pow(2,4)
		if (relative >= 5.0/7.0): 
			byte1 += pow(2,3)
			byte2 += pow(2,5)
		if (relative >= 6.0/7.0): 
			byte1 += pow(2,2)
			byte2 += pow(2,6)
		if (relative >= 7.0/7.0): 
			byte1 += pow(2,1)

		return byte1, byte2

