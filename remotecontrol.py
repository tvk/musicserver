import smbus, time, threading, lcddriver, json

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
		if (self.onUpdate is not None):
			self.onUpdate(relativeValue)

class RemoteControl:

	bus = None
	player = None
	
	volume = None;
	bass = None;
	treble = None;
	presets = None;
	
	lcdSecondLine = 'Welcome';
	lcdAltSecondLine = None;
	previousOffset = None;

	lcdTimeout = time.time() + 10;
	
	def __init__(self, player):
		self.player = player;
		self.bus = smbus.SMBus(1)
		self.volume = Control(self.bus, 0x41, self.player.setVolume, self.onChangeVolume)
		self.bass = Control(self.bus, 0x42, self.onUpdateBass, self.onChangeBass)
		self.treble = Control(self.bus, 0x40, self.onUpdateTreble, self.onChangeTreble)
		self.presets = Control(self.bus, 0x43, None, self.onChangePreset)
		readThread = threading.Thread(target=self.readValues)
		readThread.daemon = True
		readThread.start()
		updateLcdThread = threading.Thread(target=self.updateLcd)
		updateLcdThread.daemon = True
		updateLcdThread.start()

	def readValues(self):
		while True:
			try:
				self.volume.update()
				self.treble.update()
				self.bass.update()
				self.presets.update()
				time.sleep(0.1)
			except Exception as e:
				print e
				pass
			
	def updateLcd(self):
		lcd = lcddriver.lcd()
		while True:
			if (time.time() + 8 > self.lcdTimeout and self.lcdAltSecondLine is not None):
				self.lcdSecondLine = self.lcdAltSecondLine 
			if (time.time() < self.lcdTimeout):
				lcd.lcd_backlight("on")
				lcd.lcd_display_string(time.ctime(), 1)
				lcd.lcd_display_string(self.lcdSecondLine, 2)
			if (time.time() > self.lcdTimeout):
				lcd.lcd_backlight("off")
			time.sleep(0.25)

	def onChangeBass(self, level):
		self.lcdSecondLine = ("Bass: " + str(int(-24.0 + 36.0 * level)) + " dB").ljust(16)
		self.lcdTimeout = time.time() + 12;

	def onUpdateBass(self, level):
		self.player.setBass(-24.0 + 36.0 * level)

	def onChangeTreble(self, level):
		self.lcdSecondLine = ("Treble: " + str(int(-24.0 + 36.0 * level)) + " dB").ljust(16)
		self.lcdTimeout = time.time() + 12;

	def onUpdateTreble(self, level):
		self.player.setTreble(-24.0 + 36.0 * level)
		
	def onChangePreset(self, level):
		with open('static/radiopresets.json') as data_file:    
			data = json.load(data_file)
			offset = int(level * len(data));
			self.lcdTimeout = time.time() + 10;
			if (offset is not self.previousOffset and offset == 0):
				self.player.pause();
				self.lcdSecondLine = "Pause".ljust(16)
				self.lcdAltSecondLine = None
			elif (offset is not self.previousOffset):
				selected = data[offset - 1];
				self.play(selected["name"], selected["url"])
			else:
				self.lcdTimeout = time.time() + 10
				
			self.previousOffset = offset;	
			
	def play(self, name, url):		
		self.lcdSecondLine = name.rjust(16)
		self.lcdAltSecondLine = self.lcdSecondLine
		self.player.play(url)
		self.lcdTimeout = time.time() + 10;

	def onChangeVolume(self, level):
		self.lcdSecondLine = ("Volume: " + str(int(100.0 * level)) + "%").ljust(16)
		self.lcdTimeout = time.time() + 12;
		
