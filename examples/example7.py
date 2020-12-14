'''Example 9.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p122

'''

import steeldesign as sd

# creo perfil
p1 = sd.c_profile(H= 7.0, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Ly= 2.5*12, Lz= 2.5*12, Cb= 1.685)
# creo un miembro
m = sd.member(L= 30*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
fiMn, midC= analysis.s3_3_1()
print('fiMn =', round(fiMn,2),'| Mn_no =', round(midC['Mn_no'],2), '| Mn_LB =',  round(midC['Mn_LB'],2))

# Valores de referencia:    fiMn = 80.16 | Mn_no = 111.95 | Mn_LB = 94.30
# Valores de steeldesign:   fiMn = 78.38 | Mn_no = 111.90 | Mn_LB = 92.21

# NOTA: Error tiene origen en el uso de eta_iter en lugar de los valores de tabla que usa la referencia. f_ref=42.12 f_eta_iter= 41.2

print('\n3.3.2 Design Strength for Shear Only')
fiVn, midC= analysis.s3_3_2()
print('fiVn =', round(fiVn,2),'| vn =', round(midC['tau'],2))

# Valores de referencia:    fiVn = 27.88 | vn = 38.24
# Valores de steeldesign:   fiVn = 27.91 | vn = 38.27

# NOTA: Error tiene origen en el uso de eta_iter en lugar de los valores de tabla que usa la referencia. f_ref=38.30 f_eta_iter= 38.27.
# NOTA: Si se usa Es/E0 (B-4) en lugar de Gs/G0 sd da fiVn = 29.06 | vn = 39.86 (error no conservativo).
# NOTA: Si se usa Et/E0 (B-5) en lugar de Gs/G0 sd da fiVn = 22.65 | vn = 31.06 (mayor error pero es conservativo).

print('\n3.3.3 Strength for Combined Bending and Shear')
Mu = 44.16
Vu = 2.21
print('Cargas: Mu = ', Mu, ' | Vu = ', Vu)
ratio, state = analysis.s3_3_3(fiMn=fiMn, fiVn=fiVn, Mu=Mu, Vu=Vu)
print('ratio = ', round(ratio,2), '| state : ', state)

# Valores de referencia:    ratio = 0.31
# Valores de steeldesign:   ratio = 0.32