import requests, logging
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
	json = ''
	def handle_starttag(self, tag, attrs):
		if (tag == 'a'):
			for name, value in attrs:
				if (name == 'class' and 'clickabletitle' in value):
					self.handle_entry(attrs)

	def handle_entry(self, attrs):
		self.json += '{' if len(self.json) == 0 else ',{';
		for name, value in attrs:
			if (name == 'title'): self.json += '"title": "' + value + '",';
			if (name == 'href'): self.json += '"url": "' + value + '",';
		self.json += '"u":"u"}'
				
class Shoutcast:

	lastSearchQuery = ''
	lastSearchIndex = 0
  
	def search(self, search):
	  
		if (search is not self.lastSearchQuery):
			self.lastSearchIndex = 0
			self.lastSearchQuery = search
		
		logging.debug("Requesting " + self.lastSearchQuery + ", index: " + str(self.lastSearchIndex));
		response = requests.post(r'http://www.shoutcast.com/search-ajax/' + self.lastSearchQuery, data='strIndex=' + str(self.lastSearchIndex) + '&count=10&ajax=true')
		parser = MyHTMLParser()
		parser.feed(response.text)
		return '[' + parser.json + ']'

	def searchMore(self):
		self.lastSearchIndex += 10
		return self.search(self.lastSearchQuery)

