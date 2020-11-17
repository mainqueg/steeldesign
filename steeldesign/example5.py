'''Example 18.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 174

'''

from design import ASCE_8_02, member, designParameters
from properties import I_builtup_c_w_lps_profile, c_w_lps_profile, steel

# creo un perfil con refuerzo de labios
p1 = I_builtup_c_w_lps_profile(H= 8.0, B= 2.50, D= 0.498, t= 0.135, r_out= (0.135+3/16) )
p2 = c_w_lps_profile(H= 8.0, B= 2.5, D= 0.498, t= 0.135, r_out= (0.135+3/16) )

p1.calculate()
p2.calculate()
p1.J = 2*p2.J

# creo un acero
s = steel(FY= 30, E0= 27000, nu= 0.3, n= 9.7, offset= 0.002, name= 'SA409_long')

# defino parametros de diseño
dp = designParameters(Lx= 12*12, Ly= 6*12, Lz= 6*12)
# creo un miembro
m = member(L= 6*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = ASCE_8_02(m)
# calculo admisibles #
fiPn, midC = analysis.s3_4()

print('fiPn =', round(fiPn,2),'| Pn =', round(midC['Fn_FBy']*midC['Ae'],2))
print('Esbeltez de', m.profile.elements[1]['name'],'=', round(m.profile.elements[1]['esbeltez'],2))
print('Esbeltez de', m.profile.elements[2]['name'],'=', round(m.profile.elements[2]['esbeltez'],2))

#NOTA: La referencia da Pn 74.04 contra los 76.12 de steeldesign. 
# Ae de ref es 3.148 y steeldesign da 3.401.
# el area calculada segun steeldesign es 3.511, mientras que la referencia es 3.148 (error del 12%!!! con sectionproperties)
# 