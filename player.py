import pygst, gst, logging, time

class Player:
	pipeline = None
	current = None

	def play(self, url):
		logging.debug('Playing ' + url)
		self.pause()
		if (self.pipeline is not None):	self.pipeline.set_state(gst.STATE_NULL)
		self.pipeline = self.createPipeline(url)
		self.current = url;
		self.pipeline.set_state(gst.STATE_READY)
		self.pipeline.set_state(gst.STATE_PAUSED)
		time.sleep(1)
		self.pipeline.set_state(gst.STATE_PLAYING)

	def pause(self):
		logging.debug('Pausing')
		if (self.pipeline is not None):
			self.pipeline.set_state(gst.STATE_PAUSED)

	def createPipeline(self, url):
		return gst.parse_launch('playbin2 uri="' + url + '"')

