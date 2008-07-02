import urllib
from BeautifulSoup import BeautifulSoup

filename="google_questions.n3"
max = 500
file = open(filename,'a')


def getThread(link,title) :
	id = link.split('/id/')[1].split('.html')[0]
	thread = urllib.urlopen("http://answers.google.com/"+link)
	st = BeautifulSoup(thread)
	description = st('pre')[0].contents[0]
	file.write('<#'+id+'> a ga:Question.\n')
	file.write('<#'+id+'> dc:title """'+title+'""".\n')
	file.write('<#'+id+'> dc:description """'+description+'""".\n\n')
	thread.close()



def crawl(inc,browse_page) :
	bp = urllib.urlopen("http://answers.google.com/"+browse_page)
	soup = BeautifulSoup(bp)
	for ahref in soup('a'):
        	print ahref
		link = ahref.get('href')
		title = ahref.contents[0]
		if link.find('threadview') > -1:
			getThread(link,title)
			inc = inc+1
			print inc
			if(inc>max) :
				file.close()
				exit()
		if link.find('browse/1005') > -1:
			crawl(inc,ahref.get('href'))
	bp.close()


page = crawl(0,"answers/browse/1005.html")

