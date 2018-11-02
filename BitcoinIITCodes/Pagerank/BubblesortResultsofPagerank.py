import json
def BSR(name):	
	f1=open('simple_pagerank_scores_%s' %name,'r')
	f2=open('weighted_pagerank_scores_%s' %name,'r')
	
	l1=[]
	l2=[]
	
	d1=json.load(f1)
	d2=json.load(f2)
	
	for key in d1:
		l1.append(key)
	
	print len(l1)
	
	for j in range(0,len(l1)):
		for i in range(0,len(l1)-1-j):
			if d1[l1[i]]<d1[l1[i+1]]:
				temp=l1[i+1]
				l1[i+1]=l1[i]
				l1[i]=temp
	
	print l1[0]		
	
	for key in d2:
		l2.append(key)
	
	print len(l2)
	
	for j in range(0,len(l2)):
		for i in range(0,len(l2)-1-j):
			if d2[l2[i]]<d2[l2[i+1]]:
				temp=l2[i+1]
				l2[i+1]=l2[i]
				l2[i]=temp
	
	print l2[0]	
	
	f1.close()
	f2.close()
	
	f3=open('compare_rank_%s' %name,'w')
	
	for i in range(0,len(l1)):
		f3.write(l1[i]+' '+l2[i]+' '+str(d1[l1[i]])+' '+str(d2[l2[i]])+'\n')
		
