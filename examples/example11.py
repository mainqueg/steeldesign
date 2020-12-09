'''Example 22.1 c-Section wlps (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p257

'''
import steeldesign as sd
from steeldesign.modules.functions import adjustNeutralAxis

# creo perfil
p1 = sd.c_w_lps_profile(H= 8.0, B= 3, D= 0.80, t= 0.105, r_out= ( 0.105+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters()
# creo un miembro
m = sd.member(L= 16*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# solicito analisis segun 3.4
fiPn, midC = analysis.s3_4()
print('fiPn =', round(fiPn,2),'| Pn =', round(midC['Fn']*midC['Ae'],2), '| Pno =',  round(midC['Pno'],2), '| Ae_no =',  round(midC['Ae_no'],3) )

# Valores de referencia:    fiPn = 10.97 | Pn = 12.91 | Pno = 54.80 | Ae_no = 1.096
# Valores de steeldesign:   fiPn = 10.87 | Pn = 12.79 | Pno = 54.64 | Ae_no = 1.093
