import web, pygst, gst, logging
        
urls = (
	'/', 'index',
    '/current', 'current',
	'/control/(play|pause)', 'control'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
logging.basicConfig(level=logging.DEBUG)

class index:
	def GET(self):
		return render.index()

class current:        
    def GET(self):
       	return 'Ok'
    def POST(self):
		return player.play(web.data())

class control:
	def POST(self, name):
		logging.debug('Control: ' + name)
		if name == 'play' and player.current is not None: player.play(player.current)
		if name == 'pause': player.pause()

class player:
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
		
player = player()


if __name__ == "__main__":
    app.run()
