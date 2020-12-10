'''Example 8.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p114

'''

import steeldesign as sd

# creo un perfil con refuerzo de labios
p1 = sd.I_builtup_c_profile(H= 6.0, B= 1.625, t= 0.06, r_out= (0.06+3/32) )
p2 = sd.c_profile(H= 6.0, B= 1.625, t= 0.06, r_out= (0.06+3/32) )
p2.calculate(loadProfileFromDB=True)
# creo un acero
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# defino parametros de diseño
dp = sd.designParameters(Lx= 4*12, Ly= 4*12, Lz= 4*12, Cb= 1.75)
# creo un miembro
m = sd.member(L= 4*12, profile= p1, steel= s, designParameters= dp)
p1.J = 2*p2.J
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles
fiMn, midC = analysis.s3_3_1()

print('fiMn =', round(fiMn,2),'| Mn_no =', round(midC['Mn_no'],2), '| Mn_LB =',  round(midC['Mn_LB'],2))

# Valores de referencia:    fiMn = 48.07 | Mn_no = 71.10 | Mn_LB = 56.55
# Valores de steeldesign:   fiMn = 48.52 | Mn_no = 70.99 | Mn_LB = 57.08

# NOTA: Error tiene origen en el uso de eta_iter en lugar de los valores de tabla que usa la referencia. f_ref=38.47 f_eta_iter= 38.88