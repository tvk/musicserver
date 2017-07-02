import smbus, time, threading

# PCF8591
ADDRESS = 0x48

class RemoteControl:

	bus = None
	player = None;
	
	def __init__(self, player):
		self.player = player;
		self.bus = smbus.SMBus(1)
		fred = threading.Thread(target=self.loop)
		fred.daemon = True
		fred.start()

	def loop(self):
		while True:
			try:
				self.player.setVolume(self.read(0x41))
				self.player.setBass(-24.0 + 36.0 * self.read(0x42))					
				self.player.setTreble(-24.0 + 36.0 * self.read(0x40))
				time.sleep(0.1)
			except Exception as e:
				print e
				pass

	def read(self, index):
		self.bus.read_byte_data(ADDRESS, index)
		return (255.0 - self.bus.read_byte_data(ADDRESS, index)) / 255.0
