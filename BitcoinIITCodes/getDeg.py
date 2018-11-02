from snap import *
import json

name='pk_200000_4990'

F = TFIn('%s.graph' %name)
G = TNEANet.Load(F)
print 'Loaded Graph'

idcv=TIntPrV()#in-deg count vector
odcv=TIntPrV()#out-deg count vector
GetInDegCnt(G,idcv)
GetOutDegCnt(G,odcv)

with open('DegreeCount_%s.txt' %name,'w') as f:
	f.write('In-deg\tCount\n')
	for item in idcv:
		f.write('%d\t\t%d\n' %(item.GetVal1(),item.GetVal2()))
	f.write('\n\n')
	f.write('Out-deg\tCount\n')	
	for item in odcv:
		f.write('%d\t\t%d\n' %(item.GetVal1(),item.GetVal2()))

print 'Done'
