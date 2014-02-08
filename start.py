import os, web, logging, shoutcast, player, beatcontrol, ConfigParser
        
urls = (
	'/', 'index',
	'/current', 'current',
	'/control/(play|pause)', 'control',
	'/level', 'level',
	'/library/local/(.*)', 'locallibrary',
	'/library/shoutcast/(.*)', 'shoutcastlibrary'
)

musicdir = '/home/thomas/music/storage/'

config = ConfigParser.ConfigParser()
config.readfp(open('config'))

beatcontrol = beatcontrol.BeatControl(config)
logging.basicConfig(level=logging.DEBUG)
player = player.Player(beatcontrol)
app = web.application(urls, globals())
render = web.template.render('templates/')
shoutcast = shoutcast.Shoutcast()

class index:
	def GET(self): return render.index()

class current:        
    def GET(self):
       	return 'Ok'
    def POST(self):
		return player.play(web.data() if web.data().startswith('http://') else musicdir + '/' + web.data());

class control:
	def POST(self, name):
		logging.debug('Control: ' + name)
		if name == 'play' and player.current is not None: player.play(player.current)
		if name == 'pause': player.pause()

class locallibrary:
	def GET(self, path):
		logging.debug('Request to local library: ' + path);
		return ('["' + reduce(lambda x, y: x + '","' + y , sorted(os.listdir(musicdir + path))) + '"]') if os.listdir(musicdir + path) else '[]';

class shoutcastlibrary:
	def GET(self, search):
		logging.debug('Request to shoutcast: ' + search);
		return shoutcast.search(search) if search else shoutcast.searchMore() 

if __name__ == "__main__":
	app.run()
