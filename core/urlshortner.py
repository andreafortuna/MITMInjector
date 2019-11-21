from urllib.request import urlopen

def tinyUrl(nurl):
	url = 'http://tinyurl.com/api-create.php?url=' + nurl
	r = urlopen(url).read() 
	return str(r.decode())