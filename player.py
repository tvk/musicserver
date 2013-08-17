import pygst, gst, logging, gobject, threading

gobject.threads_init()

class Player:
	pipeline = None
	current = None

	def __init__(self):
		g_loop = threading.Thread(target=gobject.MainLoop().run)
		g_loop.daemon = True
		g_loop.start()

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

	def handle_bus_messages(self, bus, message):
		print message

	def create_pipeline(self, url):
		self.pipeline = gst.parse_launch('souphttpsrc location="' + url + '" ! mad ! volume ! level name="level" ! alsasink')

		# Connect this player to the gstreamer bus
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect('message', self.handle_bus_messages)
