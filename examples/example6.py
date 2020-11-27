'''Example 8.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 174

'''

import steeldesign as sd

# creo un perfil con refuerzo de labios
p1 = sd.I_builtup_c_profile(H= 6.0, B= 3.25, t= 0.06, r_out= (0.06+3/32) )
p2 = sd.c_profile(H= 6.0, B= 3.25, t= 0.06, r_out= (0.06+3/32) )

p1.calculate()
p2.calculate()
p1.J = 2*p2.J

print('Area:', round(p1.A,3))
print('Area ref:', 1.083)

# creo un acero
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')

# defino parametros de diseño
dp = sd.designParameters(Lx= 8*12, Ly= 8*12, Lz= 4*12)
# creo un miembro
m = sd.member(L= 8*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
fiMn, midC = analysis.s3_3_1()

print('Mn_Nominal =', round(midC['Nominal_Mn']*midC['Ae'],2),'| Mn_LB =', round(midC['LB_Mn']*midC['Ae'],2))
# print('Esbeltez de', m.profile.elements[1]['name'],'=', m.profile.elements[1]['esbeltez'])
# print('Esbeltez de', m.profile.elements[2]['name'],'=', round(m.profile.elements[2]['esbeltez'],3))
# print('Esbeltez de', m.profile.elements[3]['name'],'=', round(m.profile.elements[3]['esbeltez'],3))

#NOTA: La referencia da Mn_Nominal 71.10 contra los xxx de steeldesign.
#NOTA: La referencia da Mn_LB 56.55 contra los xxx de steeldesign.
