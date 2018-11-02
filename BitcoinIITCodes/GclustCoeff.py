from snap import *
import json

NIdV = TIntV()

name='pk_200000_4990MaximalConnectedComponent'

F = TFIn('%s.graph' %name)
G = TUNGraph.Load(F)
print 'Loaded Graph'

Components = TCnComV()
GetSccs(G, Components)

for i in Components[0]:
	NIdV.Add(i)

print 'Got Components'

SG=GetSubGraph(G,NIdV)

print 'Made subgraph using the maximal connected component' 

PlotClustCf(SG, "Bitcoin_Graph_PK", "Bitcoin")

print 'Plotted the coefficients'

F = TFOut('%sMaximalConnectedComponent.graph' %name)
SG.Save(F)
F.Flush()

#print SG.len()
print 'Done'
