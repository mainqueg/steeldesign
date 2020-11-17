myStep= odb.steps.items()[0][1]
myFrame = myStep.frames[1]
SFs = myFrame.fieldOutputs['SF']
setE= session.openOdb(r'C:/Users/Mainque/Dropbox/CNEA/00 - Varios/00 - ABQ unifilar/Job-1.odb').rootAssembly.instances['PART-1-1'].elementSets['C2']
SFsE= SFs.getSubset(position=INTEGRATION_POINT,region=setE)
SFsE.values[0].data
SFsE.values[0].elementLabel

SF1min, SF2min, SF3min = 1e14, 1e14, 1e14
SF1max, SF2max, SF3max = -1e14, -1e14, -1e14

for value in SFsE.values:
    SF1 = value.data[0]
    SF2 = value.data[1]
    SF3 = value.data[2]
    
    if SF1 > SF1max:
        SF1max = SF1
        SF1maxE = value.elementLabel
    if SF1 < SF1min:
        SF1min = SF1
        SF1minE = value.elementLabel
    
    if SF2 > SF2max:
        SF2max = SF2
        SF2maxE = value.elementLabel
    if SF2 < SF2min:
        SF2min = SF2
        SF2minE = value.elementLabel
    
    if SF3 > SF3max:
        SF3max = SF3
        SF3maxE = value.elementLabel
    if SF3 < SF3min:
        SF3min = SF3
        SF3minE = value.elementLabel
        
print 'SF1MAX',SF1max, 'en Elemento', SF1maxE
print 'SF1Min',SF1min, 'en Elemento', SF1minE

print 'SF2MAX',SF2max, 'en Elemento', SF2maxE
print 'SF2Min',SF2min, 'en Elemento', SF2minE

print 'SF3MAX',SF3max, 'en Elemento', SF3maxE
print 'SF3Min',SF3min, 'en Elemento', SF3minE