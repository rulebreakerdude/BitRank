import json

block1=[]

start=200000
end=205000
step=10
numb=end-start-10

for i in range(start+step,end,10):
#    filepath=path.relpath(')
	with open( 'JSONFiles/data%i.json' %i,'r') as f:
		print 'Loading Block', i
		B=json.load(f)
		for j in range(0,10):
			block1.append(B[j])

#print len(block1[0]['tx'])



dOutTxid={}
for k in range (0,numb):
	for i in range(0,len(block1[k]['tx'])):
		for j in range (0,len(block1[k]['tx'][i]['vout'])):
			try:
				if block1[k]['tx'][i]['txid'] not in dOutTxid:
					dOutTxid[block1[k]['tx'][i]['txid']]=[]
				dOutTxid[block1[k]['tx'][i]['txid']].append(block1[k]['tx'][i]['vout'][j]['scriptPubKey']['addresses'][0])
				if len(block1[k]['tx'][i]['vout'][j]['scriptPubKey']['addresses'])>1:
					print 'Possible Escrow' + block1[k]['tx'][i]['txid']
			except KeyError:
				continue




dInpTxid={}
count=0;
for k in range (0,numb): 
	dInpTxid[block1[k]['tx'][0]['txid']]=[]
	dInpTxid[block1[k]['tx'][0]['txid']].append('coinbase')#dummy input for miner
	for i in range(0,len(block1[k]['tx'])):
		for j in range (0,len(block1[k]['tx'][i]['vin'])):
			try:
				if block1[k]['tx'][i]['txid'] not in dInpTxid:
					dInpTxid[block1[k]['tx'][i]['txid']]=[]
				txid=block1[k]['tx'][i]['vin'][j]['txid']#the transaction id of the transaction this input is taken from
				vout=block1[k]['tx'][i]['vin'][j]['vout']#the index of the output used for this input
				dInpTxid[block1[k]['tx'][i]['txid']].append(dOutTxid[txid][vout])
			except KeyError:
				continue


dPkNet={}
for txid in dInpTxid:
	try:
		pks_in_txid=dOutTxid[txid]
		for in_addr in dInpTxid[txid]:
			for out_pk in pks_in_txid:
				if in_addr not in dPkNet:
					dPkNet[in_addr]=[]
				dPkNet[in_addr].append(out_pk)
	except KeyError:
		pass



f=open('pk_%i_%i.txt' %(start,numb),'w')
json.dump(dPkNet,f,indent=4)
f.close()

print 'Done'

