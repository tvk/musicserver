import pygst, gst, logging, gobject, threading, beatcontrol, requests, re
gobject.threads_init()

class Player:
	pipeline = None
	current = None
	beatcontrol = beatcontrol.BeatControl()

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

	def handle_level_messages(self, bus, message):
		if (message.structure is not None and message.structure.get_name() == 'level'):
			self.beatcontrol.handle_level_message(message)

	def create_pipeline(self, url):
		if (self.pipeline is not None):
			self.pipeline.set_state(gst.STATE_NULL)
		
		source = 'souphttpsrc' if url.startswith('http') else 'filesrc';
		url = self.parse_playlist(url) if source == 'souphttpsrc' and '.pls' in url else url;
		thePipeline = source + ' location="' + url + '" ! mad ! tee name=t ! queue ! audioconvert ! audiocheblimit mode=low-pass cutoff=40 type=1 ! level interval=16000000 ! fakesink t. ! queue ! volume ! alsasink'
		logging.debug(thePipeline)

		self.pipeline = gst.parse_launch(thePipeline)

		# Connect this player to the gstreamer bus
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect('message', self.handle_level_messages)

	def parse_playlist(self, url):
		return re.search('File.=(.*)', requests.get(url).text).group(1)


