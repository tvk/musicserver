from apscheduler.scheduler import Scheduler

class WakeUp:

	sched = Scheduler()
	config = None
	player = None

	def __init__(self, config, player):
		self.config = config
		self.player = player
		self.sched.start()
		if (config.has_section('wakeup') and config.getboolean('wakeup', 'enabled')):
			self.sched.add_cron_job(self.wakeup, day_of_week=config.get('wakeup', 'days'), hour=config.get('wakeup', 'hour'), minute=config.get('wakeup', 'minute'))
			print "Wakeup initialized"

	def wakeup(self):
		self.player.play(self.config.get('wakeup', 'url'))
