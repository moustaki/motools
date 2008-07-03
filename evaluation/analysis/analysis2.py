from VectorSpace import *

f = open('data/description_ga.txt','r')


descs = []
descs.append(f.read())

vs = VectorSpace(descs)

stats = vs.documentVectors[0]

def swap_dictionary(original_dict):
	return dict([(v, k) for (k, v) in original_dict.iteritems()])

term_count = []
for k in range(0,len(stats)):
	index = swap_dictionary(vs.vectorKeywordIndex)
	term = index[k]
	count = stats[k]
	term_count.append((count,term))

#print vs.documentVectors
#print vs.vectorKeywordIndex
term_count.sort()
print term_count

