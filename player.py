import pygst, gst, logging

class Player:
	pipeline = None
	current = None
	def play(self, url):
		logging.debug('Playing ' + url)
		self.pause()
		self.pipeline = self.createPipeline(url)
		self.current = url;
		self.pipeline.set_state(gst.STATE_PLAYING)
	def pause(self):
		logging.debug('Pausing')
		if (self.pipeline is not None):
			self.pipeline.set_state(gst.STATE_PAUSED)

	def createPipeline(self, url):
		pipeline = gst.Pipeline("pipeline_default")
		source = gst.element_factory_make("gnomevfssrc", "source")
		source.set_property("location", url)
		mad = gst.element_factory_make("mad")
		audioconvert = gst.element_factory_make("audioconvert")
		audioresample = gst.element_factory_make("audioresample")
		sink = gst.element_factory_make("alsasink")

		pipeline.add(source, mad, audioconvert, audioresample, sink)
		gst.element_link_many(source, mad, audioconvert, audioresample, sink)
		return pipeline
