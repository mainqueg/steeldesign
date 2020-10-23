from design import ASCE_8_02, member, designParameters
from properties import c_w_lps_profile, steel

# creo un perfil c on refuerz ode labios
p1 = c_w_lps_profile(H= 100, B= 50, D= 12, t= 1.5, r_out= 3.75)
#p2 = c_w_lps_profile(H= 200, B= 50, D= 12, t= 1.5, r_out= 3.75)
p1.calculate()

# creo un acero
s = steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')

# defino parametros de diseño
dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
# creo un miembro
m = member(L= 3200, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = ASCE_8_02(m)
# calculo admisibles
(Pn, fiPn) = analysis.s3_FTB()

print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))