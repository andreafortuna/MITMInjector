import sys
import os, platform
import subprocess
import socket
import os.path as path
from multiprocessing import Process
#from urllib.request import urlopen
import urllib.request
import zipfile
import json 

class ngrok(object):
    PORT = 8080
    def __init__(self, authtoken, port):
        if authtoken:
            self.token = authtoken
        else:
            print ("Can't use Ngrok without a valid token")
        self.PORT = port
        system_type = os.name
        system_name = platform.system()
        system_architecture = platform.architecture()[0]

        str_ngrok = './ngrok'
        if "nt" in system_type:
            str_ngrok = './ngrok.exe'
        
        if path.exists(str_ngrok):
            pass
        else:            
            if "posix" in system_type:
                if "arwin" in system_name:
                    if "64" in system_architecture:
                        download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
                    else:
                        download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-386.zip"
                else:
                    if "64" in system_architecture:
                        download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
                    else:
                        download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip"
            elif "nt" in system_type:
                if "64" in system_architecture:
                    download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip"
                else:
                    download_link = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-386.zip"
            else:
                sys.exit(0)
            
            filename = "ngrok.zip"
            urllib.request.urlretrieve(download_link, filename)
                        
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(".")
            if "posix" in system_type:
                os.chmod("ngrok", 0o755)            
            os.remove(filename)
        subprocess.check_output([str_ngrok, "authtoken", authtoken])                 

    def start(self):
        pNg = Process(target=self.start_ngrok,)
        pNg.start()	
        NgrokURL = self.getNgrokStats()
        return NgrokURL

    def start_ngrok(self):
	    subprocess.check_output(["./ngrok", "http", self.PORT])
	
    def getNgrokStats(self):
        output=""
        while output == "":
            try:
                raw_output = urllib.request.urlopen("http://localhost:4040/api/tunnels").read().decode()
                data = json.loads(raw_output)
                output = data['tunnels'][0]['public_url']
            except Exception as e:
                #print (str(e))
                continue
            break
        return output