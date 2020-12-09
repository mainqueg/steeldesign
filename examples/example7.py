'''Example 9.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p122

'''

import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis

# creo perfil
p1 = sd.c_profile(H= 7.0, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Ly= 2.5*12, Lz= 2.5*12, Cb=1.685)
# creo un miembro
m = sd.member(L= 30*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
Se, nEffAreas= analysis.s3_Se_effective(50)
print(Se)
