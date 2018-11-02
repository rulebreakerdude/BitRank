import json

numb=15000
block1=[]
for i in range(1000,numb+1,1000):
#    filepath=path.relpath(')
	with open( 'Nigu/data%i.json' %i,'r') as f:
		print 'Loading Block', i
		B=json.load(f)
		for j in range(0,1000):
			block1.append(B[j])
#print len(block1[0]['tx'])

'''
dTxIndex={}
dTxIndexHash={}
for k in range (0,numb):
	for i in range(0,len(block1[k]['tx'])):
		dTxIndex[block1[k]['tx'][i]['txid']]=block1[k]['tx'][i]['txid']
		dTxIndexHash[block1[k]['tx'][i]['txid']]=block1[k]['tx'][i]['hash']#a one-one map between tx index and tx hash

#print dTxIndexHash[131228992]
'''
print 'Making Transaction Network'

count=0
KEcount=0
dTxNet={}
for k in range (0,numb):
	for i in range(0,len(block1[k]['tx'])):
		for j in range (0,len(block1[k]['tx'][i]['vin'])):
			try:
				if block1[k]['tx'][i]['vin'][j]['txid'] not in dTxNet:
					dTxNet[block1[k]['tx'][i]['vin'][j]['txid']]=[]
				dTxNet[block1[k]['tx'][i]['vin'][j]['txid']].append(block1[k]['tx'][i]['txid'])
			except KeyError:
				'''
				try:
					if block1[k]['tx'][i]['vin'][j]['txid'] not in dTxIndex:
						count=count+1
				except KeyError:'''
				KEcount=KEcount+1
				

#print 'not caught', count
print 'key', KEcount

f=open('tx%i.txt' %numb,'w')
'''
for key in dTxNet:
	f.write(str(key)+" ")
	for value in dTxNet[key]:
		f.write(str(value)+" ")
	f.write("\n")
'''
json.dump(dTxNet,f,indent=4)

f.close()

print 'Output saved'

