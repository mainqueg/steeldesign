'''Example 1.1 c-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 174

'''
import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis
H= 6.0
B= 1.625
t= 0.06
r_out= (0.06+3/32)

p1 = sd.c_profile(H= 6.0, B= 1.625, t= 0.06, r_out= (0.06+3/32) )
p1.calculate()

s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')

b = 0.806
w = B - r_out
cy_ = (H-t)/2.0

cy, Ix = adjustNeutralAxis(Ix=p1.Ix, A= p1.A, t= p1.t, b_= w - b, cy_= cy_)
print(cy, Ix)
