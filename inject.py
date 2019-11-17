#!/usr/bin/python

# https://ngrok.com/docs#client-api


from bs4 import BeautifulSoup
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080
url = "https://www.repubblica.it"


#This class will handles any incoming request from
#the browser 
class injectionHandler(BaseHTTPRequestHandler):
	
	def inject(self,content):
		html = BeautifulSoup(content)
		if html.body:
			script = html.new_tag(
				"script",				
				type='application/javascript')
			script.string="alert(0);"
			html.body.insert(0, script)
			return str(html)
		
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(self.inject(urllib.urlopen(url).read()))
		return


def startServer():
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('', PORT_NUMBER), injectionHandler)
		print 'Started httpserver on port ' , PORT_NUMBER
		
		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()


startServer()












