import json
import csv

def NWS(name):

	with open(name,'r') as f:
		d1=json.load(f)

	d2={}#dictionary node->count 
	d3={}#dictionary count->node

	count=0
	for entry in d1:
		if entry not in d2:
			count=count+1
			d2[entry]=count
			d3[count]=entry
			#G.AddNode(d2[entry])
		for something in d1[entry]:
			if something[0] not in d2:
				count=count+1
				d2[something[0]]=count
				d3[count]=something[0]
				#G.AddNode(d2[something[0]])


	print 'nodes ' + str(count)
	NumberOfNodes=count

	f=open('Sparse_%s' %name, 'w')
	sw = csv.writer(f, delimiter=' ')

	sw.writerow([NumberOfNodes])#printing the shape of our sparse matrix


	d4={}#pair->unique id->money (to keep a list of the pairs we have used)
	for entry in d1:
		for something in d1[entry]:
			uniqueId=d2[entry]*count+d2[something[0]]#see how this becomes the unique id for this 2-d array
			money=0
			if uniqueId not in d4:
				d4[uniqueId]=something[1]
			else:
				d4[uniqueId]=something[1]+d4[uniqueId]

	d5={}#to keep a list of pairs we have outputted
	for entry in d1:
		for something in d1[entry]:
			uniqueId=d2[entry]*count+d2[something[0]]
			if uniqueId not in d5:
				sw.writerow([d2[entry],d2[something[0]],d4[uniqueId]])
				d5[uniqueId]=""
	f.close()

	f=open('indexing_Pagerank_%s' %name,'w')
	json.dump(d3,f,indent=4)
	f.close()

