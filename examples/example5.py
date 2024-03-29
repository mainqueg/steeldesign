'''Example 18.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p230

'''

import steeldesign as sd

# creo un perfil con refuerzo de labios
p1 = sd.I_builtup_c_w_lps_profile(H= 6.0, B= 2.50, D= 0.82, t= 0.135, r_out= (0.135+3/16) )
p2 = sd.c_w_lps_profile(H= 6.0, B= 2.5, D= 0.82, t= 0.135, r_out= (0.135+3/16) )
p2.calculate(loadProfileFromDB=True)
# creo un acero
s = sd.steel(FY= 30, E0= 27000, nu= 0.3, n= 9.7, offset= 0.002, name= 'SA409_long')
# defino parametros de diseño
dp = sd.designParameters(Lx= 12*12, Ly= 6*12, Lz= 6*12)
# creo un miembro
m = sd.member(L= 6*12, profile= p1, steel= s, designParameters= dp)
p1.J = 2*p2.J
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
fiPn, midC = analysis.s3_4()

print('fiPn =', round(fiPn,2),'| Pn =', round(midC['Fn']*midC['Ae'],2))
print('Esbeltez de', m.profile.elements[1]['name'],'=', m.profile.elements[1]['sec 3.4-fiPn']['esbeltez'])
print('Esbeltez de', m.profile.elements[2]['name'],'=', round(m.profile.elements[2]['sec 3.4-fiPn']['esbeltez'],3))
print('Esbeltez de', m.profile.elements[3]['name'],'=', round(m.profile.elements[3]['sec 3.4-fiPn']['esbeltez'],3))

# Valores de referencia:    fiPn = 62.93 | Pn = 74.04
# Valores de steeldesign:   fiPn = 62.5 | Pn = 73.53

# NOTA: Error tiene origen en el uso de eta_iter en lugar de los valores de tabla que usa la referencia. f_ref=23.52 f_eta_iter= 23.40