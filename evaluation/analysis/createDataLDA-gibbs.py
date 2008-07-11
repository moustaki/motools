from Parser import Parser
import util

f = open('data/gq.txt','r')

parser = Parser()

otp = open('data-lda-gibbs.txt','w')
while True:
	line = f.readline()
	if line == '':
		break
	line = parser.tokenise(line)
	line = parser.removeStopWords(line)
	for word in line:
		otp.write(word+' ')


otp.close()
		
f.close()
