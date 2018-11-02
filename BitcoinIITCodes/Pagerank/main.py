#Input start and end values here
from pkWeightedNet import *
from NWeightedSparse import *
from PageRankWeighted import *
from BubblesortResultsofPagerank import *
start=400000
end  =400010
step=10
numb=end-start
#Strict Naming Convention, modify these at your own risk.
name='pk_weighted_%i_%i.txt' %(start,numb)
print '1. Create 2. Sparsify 3. Compute rank 4. Sort results'
a=int(raw_input())
while a!=0:
	if a==1:
		pkWN(start,end,step,numb,name)#Makes the Weighted Public Key Network
	if a==2:
		NWS(name)#Makes the sparse Money network
	if a==3:
		PRW(name)
	if a==4:
		BSR(name)
	print 'Enter again'
	a=int(raw_input())
print 'chill'

