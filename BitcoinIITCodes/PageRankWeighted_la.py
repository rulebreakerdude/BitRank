import json
import csv
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix

name='Sparsepk_weighted_400000_1'
#name='test'

f=open('%s.txt' %name, 'r')
sw = csv.reader(f, delimiter=' ')

s=0.85
n=948
maxerr=0.01
r=[]
c=[]
d=[]
sd=[]
for line in sw:
	r.append(int(line[0])-1)#subtracting 1 in convention with numpy format whose index starts with 0 instead of 1.
	c.append(int(line[1])-1)#subtracting 1 in convention with numpy format whose index starts with 0 instead of 1.
	d.append(float(line[2]))#Weighted Pagerank
	sd.append(1.0)#simple Pagerank
#print r,c,d


f.close()

row = np.array(r)
col = np.array(c)
data = np.array(d)
simpleData=np.array(sd)

G=csr_matrix((data, (row, col)), shape=(n, n))#making a sparse scipy matrix
SG=csr_matrix((simpleData, (row, col)), shape=(n, n))#making a sparse scipy matrix

#print SG.toarray()

#*********************------Weighted--Pagerank--computation------*******************

rsums = np.array(G.sum(1))[:,0]#computing row sum
for item in range(0,G.nnz):
	data[item]=data[item]/rsums[row[item]]#normalizing to make markov matrix
	
G=csc_matrix((data, (row, col)), shape=(n, n))
#print G[946,:]

sink=(rsums==0)#recognizing sinks



# Compute pagerank r until we converge
ro, r = np.zeros(n), np.ones(n)/n
while np.sum(np.abs(r-ro)) > maxerr:
	ro = r.copy()
# calculate each pagerank at a time
	for i in xrange(0,n):
		# inlinks of state i
		Ii = np.array(G[:,i].todense())[:,0]
		# account for sink states
		Si = sink / float(n)
		# account for teleportation to state i
		Ti = np.ones(n) / float(n)
		r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )

	# return normalized pagerank

d1={}
normFactor=sum(r)

for i in range(0,len(r)):
	d1[i]=r[i]#/normFactor

with open('weighted_pagerank_scores','w') as f:
	json.dump(d1,f,indent=4)
#*********************------Weighted--Pagerank--computation--Over------*******************

print 'Computed weighted pagerank'

#*********************------Simple--Pagerank--computation------*******************

rsums = np.array(SG.sum(1))[:,0]#computing row sum
for item in range(0,SG.nnz):
	simpleData[item]=simpleData[item]/rsums[row[item]]#normalizing to make markov matrix
	
SG=csc_matrix((simpleData, (row, col)), shape=(n, n))
sink=(rsums==0)#recognizing sinks



# Compute pagerank r until we converge
ro, r = np.zeros(n), np.ones(n)/n
while np.sum(np.abs(r-ro)) > maxerr:
	ro = r.copy()
# calculate each pagerank at a time
	for i in xrange(0,n):
		# inlinks of state i
		Ii = np.array(SG[:,i].todense())[:,0]
		# account for sink states
		Si = sink / float(n)
		# account for teleportation to state i
		Ti = np.ones(n) / float(n)
		r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )

	# return normalized pagerank

d2={}
normFactor=sum(r)

for i in range(0,len(r)):
	d2[i]=r[i]#/normFactor

with open('simple_pagerank_scores','w') as f:
	json.dump(d2,f,indent=4)

#*********************------Simple--Pagerank--computation--Over------*******************

print 'Computed simple pagerank'

