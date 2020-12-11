'''
Revised ASCE specification for the design of cold-formed stainless steel
Shin-Hua Lina, Wei-Wen Yu
Engineering Structures 2005
doi:10.1016/j.engstruct.2005.03.007

'''

import steeldesign as sd

# creo un perfil c on refuerz ode labios
p1 = sd.c_w_lps_profile(H= 88.9, B= 50.8, D=22.86, t= 2.67, r_out= (4.76+2.67) )
# creo un acero
s = sd.steel(FY= 344.8, E0= 186200, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA304_1_4_hard')
# defino parametros de diseño
dp = sd.designParameters()
# creo un miembro
m = sd.member(L= 1828.8, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
fiPn, midC = analysis.s3_4()

print('fiPn =', round(fiPn,2),'| Fn_FBy =', round(midC['Fn_FBy'],2),'| Fn_FTB =', round(midC['Fn_FTB'],2), '| Ae', round(midC['Ae'], 2) )

# Valores de referencia:    fiPn = 68500.00 | Fn_FBy = 159.4 | Fn_FTB = 128.8 | Ae 573.5
# Valores de steeldesign:   fiPn = 63296.17 | Fn_FBy = 159.52 | Fn_FTB = 129.87 | Ae 573.4

#NOTA: La diferencia esta en el valor de Fn_FTB que usa la referencia. En lugar de 128.8 usa 141.1 obtenido usando valores tabulados para eta, no la ecuación R-O.