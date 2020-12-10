'''Example 3.1 c-Section wlps (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p44

'''
import steeldesign as sd

# creo perfil
p1 = sd.c_w_lps_profile(H= 6.0, B= 1.625, D= 0.60, t= 0.06, r_out= (0.06+3/32) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# parametros de diseño
dp = sd.designParameters()
# creo un miembro
m = sd.member(L= 100, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)

fiMn, midC= analysis.s3_3_1()
print('Mn_no =', round(midC['Mn_no'],2), '| fiMn_no =', round(midC['fiMn_no'],2))

# Valores de referencia:    Mn_no = 51.45 | fiMn_no = 46.31
# Valores de steeldesign:   Mn_no = 51.38 | fiMn_no = 46.24