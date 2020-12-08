'''Example 3.1 c-Section wlps (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 31

'''
import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis

p1 = sd.c_w_lps_profile(H= 6.0, B= 1.625, D= 0.60, t= 0.06, r_out= (0.06+3/32) )
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
