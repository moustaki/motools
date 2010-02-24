import urllib2
from time import sleep


def try_open(url, try_num=0, limit = 3):
    '''try to open a url 3 times, then fail'''
    req = urllib2.Request(url,data=None,headers={'User-Agent':'dbtune.org/myspace v0.3.02b'})
    try:
		resp = urllib2.urlopen(req)
		return resp
    except:
		sleep(.5)
		try_num +=1
		if try_num < limit:
			resp = try_open(url, try_num, limit)
			return resp
		else:
			return None
		
