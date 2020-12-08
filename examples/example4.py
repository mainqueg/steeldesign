'''Example 17.1 I-Section (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. 174

'''

import steeldesign as sd

# creo un perfil c on refuerz ode labios
p1 = sd.I_builtup_c_profile(H= 6, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
p2 = sd.c_profile(H= 6, B= 1.5, t= 0.135, r_out= (0.135+3/16) )

#p1.calculate()
p2.calculate()
p1.J = 2*p2.J 

# creo un acero
s = sd.steel(FY= 30, E0= 27000, nu= 0.3, n= 9.7, offset= 0.002, name= 'SA409_long')

# defino parametros de diseño
dp = sd.designParameters(Lx= 14*12, Ly= 7*12, Lz= 7*12)
# creo un miembro
m = sd.member(L= 14*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
fiPn, midC = analysis.s3_4()

print('fiPn =', round(fiPn,2),'| Pn =', round(midC['Fn_FBy']*midC['Ae'],2))
print('Esbeltez de', m.profile.elements[1]['name'],'=', round(m.profile.elements[1]['esbeltez'],2))
print('Esbeltez de', m.profile.elements[2]['name'],'=', round(m.profile.elements[2]['esbeltez'],2))

#NOTA: La referencia da Pn 22.98 contra los 23.27 de steeldesign. Tado el error proviene de la diferencia en el ry calculado respecto del usado en la referencia.