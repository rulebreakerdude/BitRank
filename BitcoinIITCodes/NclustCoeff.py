from snap import *
import json

NIdV = TIntV()

name='upMIH4990'

F = TFIn('%s.graph' %name)
G = TNEANet.Load(F)
print 'Loaded Graph'

Components = TCnComV()
GetSccs(G, Components)

print 'Loaded Graph'

for i in Components[0]:
	NIdV.Add(i)

SG=GetSubGraph(G,NIdV)

print 'Got the maximum maximal connected component' 

PlotClustCf(SG, "%s_directed" %name, "Bitcoin")
F = TFOut('%sMaximalConnectedComponent.graph' %name)
SG.Save(F)
F.Flush()

#print SG.len()
''''''
