from VectorSpace import *
import util

f = open('data/data.txt','r')


descs = []
descs.append(f.read())
f.close()
f = open('data/ontology.txt','r')
descs.append(f.read())
f.close()

vs = VectorSpace(descs)

print util.cosine(vs.documentVectors[0],vs.documentVectors[1])
print util.cosine(vs.documentVectors[1],vs.documentVectors[0])



