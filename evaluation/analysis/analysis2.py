from VectorSpace import *

f = open('data/data.txt','r')


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
term_count.reverse()
#print term_count

print "Overall word count - "+str(len(vs.vectorKeywordIndex))

from matplotlib.pylab import *
from pylab import *
y = [t[0] for t in term_count]
x = [t[1] for t in term_count]
y = y[1:100]
x = x[1:100]

for z in range(0,len(y)):
	print x[z]+" - "+str(y[z])

width = 0.35
ind = arange(len(x))
#plot(range(0,len(term_count)),y,'ro')
bar(ind,y,width,color='r')
ylabel('Count')
title('Count of term in dataset')
xlabel('Term')
xticks(ind+width/2.,x)
show()


