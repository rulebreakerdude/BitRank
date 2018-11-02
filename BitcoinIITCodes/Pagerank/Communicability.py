import json
import csv
import numpy as np
import math as mt
from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
#name = 'pk_weighted_400000_1.txt'#default name. For use as an independent module.
name = 'test.txt'#default name. For use as an independent module.
def PRW(name):
	f=open('Sparse_%s' %name, 'r')
	sw = csv.reader(f, delimiter=' ')

	maxIter=20
	s=0.8
	maxerr=0.01
	r=[]
	c=[]
	d=[]
	sd=[]
	flag=0
	for line in sw:
		if flag==0:
			n=int(line[0])
			flag=1
			continue
		else:
			r.append(int(line[0])-1)#subtracting 1 in convention with numpy format whose index starts with 0.
			c.append(int(line[1])-1)#subtracting 1 in convention with numpy format whose index starts with 0.
			d.append(float(line[2]))#Weighted Pagerank
			sd.append(1.0)#simple Pagerank
	#print r,c,d
	f.close()

	row = np.array(r)
	col = np.array(c)
	data = np.array(d)
	simpleData=np.array(sd)
	R=csr_matrix((data, (row, col)), shape=(n, n))#making a sparse scipy matrix
	C=csc_matrix((data, (row, col)), shape=(n, n))#making a sparse scipy matrix
	print R.toarray()
	rsums = np.array(R.sum(1))[:,0]
	csums = np.array(C.sum(0))[0,:]#computing row-column sum
	print rsums
	print csums
	for item in range(0,R.nnz):
		data[item]=data[item]/(rsums[row[item]]+csums[row[item]]-data[item])#normalizing, note how data[item] has been counted twice and is hence being subtracted one time
	
	G=csr_matrix((data, (row, col)), shape=(n, n))
	S=0

	for k in range(1,maxIter):
		P=G**k
		P=P/mt.factorial(k)
		S=S+P

	print S.toarray()
PRW(name)
