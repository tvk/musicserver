import smbus, time, threading, lcddriver

# PCF8591
ADDRESS = 0x48

class Control:
	
	currentValue = None
	bus = None
	address = None;
	onUpdate = None
	onChange = None

	def __init__(self, bus, address, onUpdate, onChange):
		self.bus = bus
		self.address = address
		self.onUpdate = onUpdate
		self.onChange = onChange
		
	def update(self):
		self.bus.read_byte_data(ADDRESS, self.address)
		newValue = self.bus.read_byte_data(ADDRESS, self.address)
		normalizedNewValue = 0 if newValue <= 2 else (255 if newValue >= 253 else newValue)
		relativeValue = (255.0 - normalizedNewValue) / 255.0
		if (self.currentValue is not None and abs(newValue - self.currentValue) > 5):
			self.onChange(relativeValue)
			self.currentValue = newValue	
		if (self.currentValue is None):
			self.currentValue = newValue	
		self.onUpdate(relativeValue)

class RemoteControl:

	bus = None
	lcd = None
	player = None
	
	volume = None;
	bass = None;
	treble = None;
	
	lcdSecondLine = None;
	lcdPreviousSecondLine = None;
	
	def __init__(self, player):
		self.player = player;
		self.bus = smbus.SMBus(1)
		self.lcd = lcddriver.lcd()
		self.volume = Control(self.bus, 0x41, self.player.setVolume, self.onChangeVolume)
		self.bass = Control(self.bus, 0x42, self.onUpdateBass, self.onChangeBass)
		self.treble = Control(self.bus, 0x40, self.onUpdateTreble, self.onChangeTreble)
		readThread = threading.Thread(target=self.readValues)
		readThread.daemon = True
		readThread.start()
		updateLcdThread = threading.Thread(target=self.updateLcd)
		updateLcdThread.daemon = True
		updateLcdThread.start()
		self.lcd.lcd_clear()
		self.lcd.lcd_backlight("on");

	def readValues(self):
		while True:
			try:
				self.volume.update()
				self.treble.update()
				self.bass.update()
				time.sleep(0.1)
			except Exception as e:
				print e
				pass
			
	def updateLcd(self):
		while True:
			if (self.lcdSecondLine != self.lcdPreviousSecondLine):
				self.lcd.lcd_display_string(self.lcdSecondLine, 2)
			self.lcdPreviousSecondLine = self.lcdSecondLine
			time.sleep(0.25)

	def onChangeBass(self, level):
		self.lcdSecondLine = ("Bass: " + str(int(-24.0 + 36.0 * level)) + " dB").ljust(16)

	def onUpdateBass(self, level):
		self.player.setBass(-24.0 + 36.0 * level)

	def onChangeTreble(self, level):
		self.lcdSecondLine = ("Treble: " + str(int(-24.0 + 36.0 * level)) + " dB").ljust(16)

	def onUpdateTreble(self, level):
		self.player.setTreble(-24.0 + 36.0 * level)

	def onChangeVolume(self, level):
		self.lcdSecondLine = ("Volume: " + str(int(100.0 * level)) + "%").ljust(16)

	#def setLcd(self, line2):		
		#self.lcd.lcd_clear()
		#self.lcd.lcd_backlight("on");
		#self.lcd.lcd_display_string(time.strftime(""), 1)
		
