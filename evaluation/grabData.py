#!/usr/bin/python
import urllib
import sys
from xml.dom.ext.reader import Sax2


appid="XpbUTg7V34G0UhjATJnBGTmxGa4Rkr0fjtfx6fWwq2td30MiiNTiGFTFXe2ZcHJx9X4-"
category=396545139
filename="questions.n3"

iterations=20

def getUrl(appid,category,start) :
	return "http://answers.yahooapis.com/AnswersService/V1/getByCategory?appid="+appid+"&category_id="+str(category)+"&start="+str(start)+"&results=50"


def appendNewQuestions(url):
	stream = urllib.urlopen(url)
	reader = Sax2.Reader()
	doc_node = reader.fromStream(stream)
	result_set = doc_node.documentElement

	file = open(filename,'a')
	for question in result_set.childNodes:
		if question.nodeType==1:
			subject = question.childNodes[1].firstChild.data.encode('utf-8')
			content = question.childNodes[3].firstChild.data.encode('utf-8')
			timestamp = question.childNodes[7].firstChild.data.encode('utf-8')
			file.write("\n<#"+timestamp+">"+" a ya:Question.\n")
			file.write("<#"+timestamp+">"+" dc:title "+"\"\"\""+subject+"\"\"\".\n")
			file.write("<#"+timestamp+">"+" dc:description "+"\"\"\""+content+"\"\"\".\n")

	file.close()
	stream.close()


k=0
while k<=iterations:
	k = k+1
	start = 50*k
	url = getUrl(appid,category,start)
	print "Fetching and parsing "+url
	appendNewQuestions(url)


