import requests
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
            if (name == 'title'): self.json += "'title': '" + value + "',";
            if (name == 'href'): self.json += "'url': '" + value + "',";
        self.json += "'u':'u'}"

def search(search):
	response = requests.get(r'http://www.shoutcast.com/search-ajax/' + search, data='strIndex=0&count=10&ajax=true')

	parser = MyHTMLParser()
	parser.feed(response.text)
	return parser.json

