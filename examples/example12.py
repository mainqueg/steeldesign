'''Example 9.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p122

'''

import steeldesign as sd

# creo perfil C
p1 = sd.c_profile(H= 7.0, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Ly= 2.5*12, Lz= 2.5*12, Cb= 1.685, N=6.0)
# creo un miembro
m = sd.member(L= 30*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)


print('\n3.3.1 Design Strength for Bending Only')
fiMn, midC_B = analysis.s3_3_1(localDistorsion=True)
print('fiMn =', round(fiMn,2),'| fiMn_no_LD =', round(midC_B['fiMn_no'],2), '| fiMn_LB =',  round(midC_B['fiMn_LBx'],2))

# Valores de referencia:    fiMn = 80.16 | fiMn_no = ----- | fiMn_LB = 80.16
# Valores de steeldesign:   fiMn = 78.38 | fiMn_no = 84.70 | fiMn_LB = 78.38 (k=0.5)

# NOTA: Error tiene origen en el uso de eta_iter en lugar de los valores de tabla que usa la referencia. f_ref=42.12 f_eta_iter= 41.2
# NOTA: No hay valor para comparar si se consideran distorsiones locales, pero es un valor razonable :)


# creo perfil C con labios
p1 = sd.c_w_lps_profile(H= 7.0, B= 1.5, D=0.65, t= 0.135, r_out= (0.135+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Ly= 2.5*12, Lz= 2.5*12, Cb= 1.685, N=6.0)
# creo un miembro
m = sd.member(L= 30*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)

print('\n3.3.1 Design Strength for Bending Only')
fiMn, midC_B = analysis.s3_3_1(localDistorsion=True)
print('fiMn =', round(fiMn,2),'| fiMn_no_LD =', round(midC_B['fiMn_no'],2), '| fiMn_LB =',  round(midC_B['fiMn_LBx'],2))

# Valores de referencia:    fiMn = ----- | fiMn_no = ----- | fiMn_LB = -----
# Valores de steeldesign:   fiMn = 95.27 | fiMn_no = 95.27 | fiMn_LB = 98.42 (k=0.5)

# NOTA: No hay valor para comparar si se consideran distorsiones locales, pero es un valor razonable :)


# creo perfil C con labios - aumento el ancho
p1 = sd.c_w_lps_profile(H= 7.0, B= 2.5, D=0.85, t= 0.135, r_out= (0.135+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Ly= 2.5*12, Lz= 2.5*12, Cb= 1.685, N=6.0)
# creo un miembro
m = sd.member(L= 30*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)

print('\n3.3.1 Design Strength for Bending Only')
fiMn, midC_B = analysis.s3_3_1(localDistorsion=True)
print('fiMn =', round(fiMn,2),'| fiMn_no_LD =', round(midC_B['fiMn_no'],2), '| fiMn_LB =',  round(midC_B['fiMn_LBx'],2))

# Valores de referencia:    fiMn = ------ | fiMn_no = ------ | fiMn_LB = ------
# Valores de steeldesign:   fiMn = 134.09 | fiMn_no = 134.09 | fiMn_LB = 150.57 (k=2.96)

# NOTA: No hay valor para comparar si se consideran distorsiones locales, pero es un valor razonable :)