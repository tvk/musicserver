import os, web, logging, shoutcast, player, beatcontrol, wakeup, ConfigParser
        
urls = (
	'/', 'index',
	'/current', 'current',
	'/control/(play|pause)', 'control',
	'/level', 'level',
	'/library/local/(.*)', 'locallibrary',
	'/library/shoutcast/(.*)', 'shoutcastlibrary'
)

logging.basicConfig(level=logging.DEBUG)
musicdir = '/home/thomas/music/storage/'

class index:
	def GET(self): return web.theRenderer.index()

class current:        
    def GET(self):
       	return 'Ok'
    def POST(self):
		return web.thePlayer.play(web.data() if web.data().startswith('http://') else musicdir + '/' + web.data());

class control:
	def POST(self, name):
		logging.debug('Control: ' + name)
		if name == 'play' and web.thePlayer.current is not None: web.thePlayer.play(web.thePlayer.current)
		if name == 'pause': web.thePlayer.pause()

class locallibrary:
	def GET(self, path):
		logging.debug('Request to local library: ' + path);
		return ('["' + reduce(lambda x, y: x + '","' + y , sorted(os.listdir(musicdir + path))) + '"]') if os.listdir(musicdir + path) else '[]';

class shoutcastlibrary:
	def GET(self, search):
		logging.debug('Request to shoutcast: ' + search);
		return web.theShoutcast.search(search) if search else web.theShoutcast.searchMore() 

if __name__ == "__main__":

	config = ConfigParser.ConfigParser()
	if (os.path.exists('config')):
		config.readfp(open('config'))
	app = web.application(urls, globals())
	web.theRenderer = web.template.render('templates/')
	web.theShoutcast = shoutcast.Shoutcast()
	beatcontrol = beatcontrol.BeatControl(config, None)
	web.thePlayer = player.Player(beatcontrol)
	beatcontrol.player = web.thePlayer
	wakeup = wakeup.WakeUp(config, web.thePlayer)

	app.run()
