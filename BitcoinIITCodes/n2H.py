import json



numb=10
block1=[]
for i in range(1,numb+1):

    with open( 'JSONfiles/data%i.json' %i,'r') as f:
        print 'Loading Block', i
        block1.append(json.load(f))
#print len(block1[0]['tx'])
'''User Naming Convention: A pk which is encountered for the first time is allocated to the username "Hash of the transaction" in which it was found first, subsequent occurences and the associated public keys are mapped to that same user'''



dPkUser={}#dictionary to store the Pk->user relationship



#start of the multi Input heuristic
for k in range(0,numb):
	for i in range (0,len(block1[k]['tx'])):
		match=0
		for j in range (0,len(block1[k]['tx'][i]['inputs'])):
			try:
				if block1[k]['tx'][i]['inputs'][j]['prev_out']['addr'] in dPkUser:
					match=1
					user=dPkUser[block1[k]['tx'][i]['inputs'][j]['prev_out']['addr']]
					break
			except KeyError:
				continue
		if match==1:
			for j in range (0,len(block1[k]['tx'][i]['inputs'])):
				try:
					dPkUser[block1[k]['tx'][i]['inputs'][j]['prev_out']['addr']]=user
				except KeyError:
					continue
		if match==0:
			for j in range (0,len(block1[k]['tx'][i]['inputs'])):
				try:
					dPkUser[block1[k]['tx'][i]['inputs'][j]['prev_out']['addr']]=block1[k]['tx'][i]['hash']
				except KeyError:
					continue
#end of the multi input heuristic



dClusterInfo={}#dictionary to store the user->PK cluster information /\/\ Made using dPkUser
for key in dPkUser:
	if dPkUser[key] not in dClusterInfo:
		dClusterInfo[dPkUser[key]]=[]
	dClusterInfo[dPkUser[key]].append(key)



#start of the N-In-2-Out heuristic				
ferr=open('upN2H%iSmart.txt' %numb,'w')
for k in range(0,numb):
	for i in range (0,len(block1[k]['tx'])):
		try:
			if len(block1[k]['tx'][i]['inputs']) >=2 and len(block1[k]['tx'][i]['out']) == 2 :
				if block1[k]['tx'][i]['out'][0]['value'] < block1[k]['tx'][i]['out'][1]['value']:
					payment=block1[k]['tx'][i]['out'][1]['value']
					pkChange=block1[k]['tx'][i]['out'][0]['addr']
				else:
					payment=block1[k]['tx'][i]['out'][0]['value']
					pkChange=block1[k]['tx'][i]['out'][1]['addr']
			
				su=0
				for j in range(0,len(block1[k]['tx'][i]['inputs'])):
					try:
						su=su+block1[k]['tx'][i]['inputs'][j]['prev_out']['value']#calculating sum of the inputs
					except KeyError:
						continue

				casual=1#assume the user is casual

				for j in range(0,len(block1[k]['tx'][i]['inputs'])):
					try:
						if payment <= su-block1[k]['tx'][i]['inputs'][j]['prev_out']['value']:#checking if the payment is less than any n-1 summation of n inputs
							casual=0#Encountered a smart user
					except KeyError:
						continue
				

				if casual == 1:
					if pkChange not in dPkUser:#assuming smaller value is the change
						for j in range(0,len(block1[k]['tx'][i]['inputs'])):#the input heuristic has already been taken care of
							try:
								user=dPkUser[block1[k]['tx'][i]['inputs'][j]['prev_out']['addr']]
							except KeyError:
								continue		
				#else:
				#	print 'Smart User', block1[k]['tx'][i]['hash']

					if pkChange not in dPkUser:#that is, if it has not been caught in Multi Input Heuristic we make it go to the input cluster
						dPkUser[pkChange]=user
						ferr.write(str(block1[k]['tx'][i]['hash']))
						ferr.write("\n")
					else:#that is, if it has been caught in the Multi Input heuristic
						try:
							pkCluster=dClusterInfo[dPkUser[pkChange]]
							for pk in pkCluster:
								dPkUser[pk]=user
						except KeyError:
							continue
		except KeyError:
			continue
ferr.close()
#end of the N-In-2-Out heuristic



dClusterInfo={}#re-making this dictionary after the N-in-2-out Heuristic
for key in dPkUser:
	if dPkUser[key] not in dClusterInfo:
		dClusterInfo[dPkUser[key]]=[]
	dClusterInfo[dPkUser[key]].append(key)



dInpHash={}#dictionary to store the txHash->inputPk relationship
count=0;
for k in range (0,numb):
    dInpHash[block1[k]['tx'][0]['hash']]=[]
    dInpHash[block1[k]['tx'][0]['hash']].append(block1[k]['tx'][0]['hash'])#dummy input for miner
    for i in range(0,len(block1[k]['tx'])):
        for j in range (0,len(block1[k]['tx'][i]['inputs'])):
            try:
                if block1[k]['tx'][i]['hash'] not in dInpHash:
                    dInpHash[block1[k]['tx'][i]['hash']]=[]
                dInpHash[block1[k]['tx'][i]['hash']].append(block1[k]['tx'][i]['inputs'][j]['prev_out']['addr'])
            except KeyError:
                continue



dOutHash={}#dictionary to store the txHash->outPk relationship

for k in range (0,numb):
    for i in range(0,len(block1[k]['tx'])):
        for j in range (0,len(block1[k]['tx'][i]['out'])):
            try:
                if block1[k]['tx'][i]['hash'] not in dOutHash:
                    dOutHash[block1[k]['tx'][i]['hash']]=[]
                dOutHash[block1[k]['tx'][i]['hash']].append(block1[k]['tx'][i]['out'][j]['addr'])
            except KeyError:
                continue




dPkNet={}#dictionary to store the PK/user Network
count=0;

for tx_hash in dInpHash:
	try:
		pk_hash=dOutHash[tx_hash]
		for in_addr in dInpHash[tx_hash]:
			if in_addr in dPkUser:
				in_addr=dPkUser[in_addr]#converting input pk to user
			for out_pk in pk_hash:
				if out_pk in dPkUser:
					out_pk=dPkUser[out_pk]#converting output pk to user
				if in_addr not in dPkNet:
					dPkNet[in_addr]=[]
				dPkNet[in_addr].append(out_pk)

	except KeyError:
		continue





'''
count = 1
for key in dPkUser:
	f.write(str(key)+" "+str(dPkUser[key]))
	f.write("\n")
for k in range (0,numb):
    for i in range(0,len(block1[k]['tx'])):
        for j in range (0,len(block1[k]['tx'][i]['out'])):
			try:
				if block1[k]['tx'][i]['out'][j]['addr'] not in dPkUser:
					f.write(block1[k]['tx'][i]['out'][j]['addr']+" "+str(count))
					count=count+1
					f.write("\n")
			except KeyError:
				continue
'''


fe=open('upN2H%idClusterInfo.txt' %numb,'w')
json.dump(dClusterInfo,fe,indent=4)
fe.close()


fin=open('upN2H%sdPkUser.txt' %numb,'w')
json.dump(dPkUser,fin,indent=4)
fin.close()


f=open('upN2H%i.txt' %numb,'w')
json.dump(dPkNet,f,indent=4)
f.close()

print 'Done'
