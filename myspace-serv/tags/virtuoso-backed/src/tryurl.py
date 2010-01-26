import urllib2
from time import sleep

DEBUG = False

def try_open(url, try_num=0, limit = 3):
	'''try to open a url 3 times, then fail'''
	if DEBUG:
		print url
		print "try number " + str(try_num)
	try:
		resp = urllib2.urlopen(url)
		return resp
	except:
		#logging.error("browser open error on " + url + ", retry 1")
		sleep(.5)
		try_num +=1
		if try_num < limit:
			resp = try_open(url, try_num, limit)
			return resp
		else:
			return None
		
