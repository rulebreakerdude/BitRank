from snap import *
import json

name='upMIH4990'

with open('%s.txt' %name ,'r') as f:
	d1=json.load(f)

d2={}#dictionary node->count 
d3={}#dictionary count->node
G=TNEANet.New()

count=0;
for entry in d1:
	d2[entry]=count
	G.AddNode(d2[entry])
	count=count+1
	for something in d1[entry]:
		if something not in d2:
			d2[something]=count
			G.AddNode(d2[something])
			count=count+1

print count

for entry in d1:
	for something in d1[entry]:
		G.AddEdge(d2[entry],d2[something])

print 'Made the graph'
F = TFOut('%s.graph' %name)
G.Save(F)
F.Flush()
