import urllib2
from time import sleep
import logging

def try_open(url):
	'''try to open a url 3 times, then fail'''
	try:
		resp = urllib2.urlopen(url)
		return resp
	except:
		#logging.error("browser open error on " + url + ", retry 1")
		sleep(.5)
		try:
			resp = urllib2.urlopen(url)
			return resp
		except:
			#logging.error("browser open error, retry 2")
			sleep(.5)
			try:
				resp = urllib2.urlopen(url)
				return resp
			except:
				#logging.error("browser open error after 3 tries, failing...")
				return None

def try_get(url, path):
	'''try to get a file from url 3 times, then fail'''
	try:
		resp = urllib2.urlretrieve(url,path)
		return resp
	except:
		logging.error("urlretrieve error on " + url + "\nreason:"  +  "\nretry 1")
		sleep(.5)
		try:
			resp = urllib2.urlretrieve(url,path)
			return resp
		except:
			logging.error("urlretrieve error, retry 2")
			sleep(.5)
			try:
				resp = urllib2.urlretrieve(url,path)
				return resp
			except:
				logging.error("urlretrieve error after 3 tries, failing...")
				return None
