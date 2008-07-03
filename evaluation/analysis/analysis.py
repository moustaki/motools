from VectorSpace import *

f = open('data/description_ga.txt','r')


descs = []
while True:
	line = f.readline()
	if line == '':
		break
	descs.append(line)

vs = VectorSpace(descs)
print vs.related(0)
s = vs.search(["upbeat"])
print s

for k in range(0,len(s)):
	if k > 0.1:
		print descs[k]

