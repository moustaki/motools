from VectorSpace import VectorSpace
import util

f = open('data/gq.txt','r')


documentList = []
while True:
	line = f.readline()
	if line == '':
		break
	documentList.append(line)

vectorSpace= VectorSpace(documentList)
dv = vectorSpace.documentVectors

def countUniqueTerm(i):
	count = 0
	for j in range(0,len(dv[i])):
		if dv[i][j]>0:
			count += 1
	return count

vocab = open('vocab-lda-c.txt','w')
keys = dict([[v,k] for k,v in vectorSpace.vectorKeywordIndex.items()])
for i in range(0,len(dv[0])):
	vocab.write(keys[i]+'\n')
vocab.close()

otp = open('data-lda-c.txt','w')
for i in range(0,len(dv)):
	otp.write(str(countUniqueTerm(i))+' ')
	for j in range(1,len(dv[i])):
		if dv[i][j]!=0:
			otp.write(str(j)+':'+str(dv[i][j])+' ')
	otp.write('\n')



otp.close()
		

#print vectorIndex
f.close()

