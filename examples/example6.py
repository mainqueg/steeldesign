'''Example 8.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 174

'''

import steeldesign as sd

# creo un perfil con refuerzo de labios
p1 = sd.I_builtup_c_profile(H= 6.0, B= 1.625, t= 0.06, r_out= (0.06+3/32) )
p2 = sd.c_profile(H= 6.0, B= 1.625, t= 0.06, r_out= (0.06+3/32) )

# p1.calculate()
p2.calculate()
p1.J = 2*p2.J

# creo un acero
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')

# defino parametros de diseño
dp = sd.designParameters(Lx= 4*12, Ly= 4*12, Lz= 4*12, Cb=1.75)
# creo un miembro
m = sd.member(L= 4*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
fiMn, midC = analysis.s3_3_1()

print('Mn_Nominal =', round(midC['Nominal_Mn'],2),'| Mn_LB =', round(midC['LB_Mn'],2))

#NOTA: La referencia da Mn_Nominal 71.10 contra los 71.10 de steeldesign.
#NOTA: La referencia da Mn_LB 56.55 contra los 57.28 de steeldesign.
