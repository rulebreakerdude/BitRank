import json

block1=[]


def pkWN(start,end,step,numb,name):
	for i in range(start+step,end+step,step):
	#    filepath=path.relpath(')
		with open( 'JSONFiles/data%i.json' %i,'r') as f:
			print 'Loading Block', i
			B=json.load(f)
			for j in range(0,10):
				block1.append(B[j])

	dOutTxid={}
	for k in range (0,numb):
		for i in range(0,len(block1[k]['tx'])):
			for j in range (0,len(block1[k]['tx'][i]['vout'])):
				try:
					if block1[k]['tx'][i]['txid'] not in dOutTxid:
						dOutTxid[block1[k]['tx'][i]['txid']]=[]
					dOutTxid[block1[k]['tx'][i]['txid']].append([block1[k]['tx'][i]['vout'][j]['scriptPubKey']['addresses'][0],block1[k]['tx'][i]['vout'][j]['value']])
					if len(block1[k]['tx'][i]['vout'][j]['scriptPubKey']['addresses'])>1:
						print 'Possible Escrow' + block1[k]['tx'][i]['txid']
				except KeyError:
					continue

	'''
	f=open('testDOUT.txt','w')
	json.dump(dOutTxid,f,indent=4)
	f.close()
	'''

	dInpTxid={}
	count=0;
	for k in range (0,numb): 
		dInpTxid[block1[k]['tx'][0]['txid']]=[]
		dInpTxid[block1[k]['tx'][0]['txid']].append(['coinbase',25])#dummy input for miner
		for i in range(0,len(block1[k]['tx'])):
			for j in range (0,len(block1[k]['tx'][i]['vin'])):
				try:
					if block1[k]['tx'][i]['txid'] not in dInpTxid:
						dInpTxid[block1[k]['tx'][i]['txid']]=[]
					txid=block1[k]['tx'][i]['vin'][j]['txid']#the transaction id of the transaction this input is taken from
					vout=block1[k]['tx'][i]['vin'][j]['vout']#the index of the output used for this input
					dInpTxid[block1[k]['tx'][i]['txid']].append([dOutTxid[txid][vout][0],dOutTxid[txid][vout][1]])
				except KeyError:
					continue
				except IndexError:
					continue


	'''
	f=open('testDIN','w')
	json.dump(dInpTxid,f,indent=4)
	f.close()
	'''
	dPkNet={}
	for txid in dInpTxid:
		try:
			#Total_data_out_txid=dOutTxid[txid]
			s=0
	
			for data_out_txid in dOutTxid[txid]:
				s=s+data_out_txid[1]				#base weight for distribution of edge weight
	
			for data_in_txid in dInpTxid[txid]:
				in_addr = data_in_txid[0]
				in_value= data_in_txid[1]
				if in_addr not in dPkNet:
					dPkNet[in_addr]=[]
				for data_out_txid in dOutTxid[txid]:
					out_addr=  data_out_txid[0]
					out_value= data_out_txid[1]
					edge_weight= in_value*out_value/s
					dPkNet[in_addr].append([out_addr,edge_weight])
		except KeyError:
			continue



	f=open(name,'w')
	json.dump(dPkNet,f,indent=4)
	f.close()

	print 'Done'
