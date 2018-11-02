from snap import *
import json

name='pk_200000_4990'

F = TFIn('%s.graph' %name)
G = TNEANet.Load(F)
print 'Loaded Graph'

PlotInDegDistr(G, "Bitcoin","Bitcoin In Degree")
PlotOutDegDistr(G, "Bitcoin","Bitcoin Out Degree")	

print 'done'
