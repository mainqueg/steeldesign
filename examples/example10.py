'''Example 4.5 c-Section wlps (LRFD). 

Wei-wen Yu; Chen, Helen "Cold-formed steel design" (2020). WILEY. p137

'''
import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis

p1 = sd.c_w_lps_profile(H= 10.0, B= 3.5, D= 0.720, t= 0.075, r_out= (0.075+3/32) )
#p1.calculate()

s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')

#b = 0.806
#w = B - r_out
#cy_ = (H-t)/2.0
dp = sd.designParameters()
# creo un miembro
m = sd.member(L= 100, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
Se, nEffAreas= analysis.s3_Se_effective(50)
print(Se)
#cy, Ix = adjustNeutralAxis(Ix=p1.Ix, A= p1.A, t= p1.t, b_= w - b, cy_= cy_)
#print(cy, Ix)
