import pygst, gst, logging, gobject, threading, socket, collections
gobject.threads_init()

class Player:
	pipeline = None
	current = None
	peaks = collections.deque(maxlen=100)
	socket = None

	def __init__(self):
		g_loop = threading.Thread(target=gobject.MainLoop().run)
		g_loop.daemon = True
		g_loop.start()

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def play(self, url):
		logging.debug('Playing ' + url)
		self.pause()
		self.create_pipeline(url)
		self.current = url;
		self.pipeline.set_state(gst.STATE_PLAYING)

	def pause(self):
		logging.debug('Pausing')
		if (self.pipeline is not None):
			self.pipeline.set_state(gst.STATE_PAUSED)

	def handle_level_messages(self, bus, message):
		if (message.structure is not None and message.structure.get_name() == 'level'):
			peak = (message.structure["peak"][0] + message.structure["peak"][1]) / 2.0; # i.e. -12.123
			self.peaks.append(peak)
			localMax = reduce(lambda x, y: x if x < y else y, self.peaks); # i.e. -24.112
			localMin = reduce(lambda x, y: x if x > y else y, self.peaks); # i.e. -3.1125
			if (localMax != localMin):
				relative = (peak - localMin) / (localMax - localMin)
				self.socket.sendto(str(relative), ("marvin", 6667))

	def get_level(self):
		return self.peak

	def create_pipeline(self, url):
		if (self.pipeline is not None):
			self.pipeline.set_state(gst.STATE_NULL)
		
		source = 'souphttpsrc' if url.startswith('http') else 'filesrc';
		thePipeline = source + ' location="' + url + '" ! mad ! tee name=t ! queue ! audioconvert ! audiocheblimit mode=low-pass cutoff=40 type=1 ! level interval=5000000 ! fakesink t. ! queue ! volume ! alsasink'
		logging.debug(thePipeline)

		self.pipeline = gst.parse_launch(thePipeline)

		# Connect this player to the gstreamer bus
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect('message', self.handle_level_messages)

		self.peaks.clear()
