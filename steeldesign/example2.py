from design import ASCE_8_02, member, designParameters
from properties import c_w_lps_profile, steel
import matplotlib.pyplot as plt

Long =[300,500,700,1000,1200,1500,1800,2000,2200,2500,2800,3000,3500,5000]

# creo un perfil c on refuerz ode labios
p1 = c_w_lps_profile(H= 100, B= 50, D= 12, t= 1.5, r_out= 3.75)
p1.calculate()
# creo un acero
s = steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')

Fns = []
Pns = []

for L in Long:
    # defino parametros de diseño
    dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    # creo un miembro
    m = member(L= L, profile= p1, steel= s, designParameters= dp)
    # creo el analisis
    analysis = ASCE_8_02(m)
    # calculo admisibles
    (Fn, Pn) = analysis.s3_FTB()
    Fns.append(Fn)
    Pns.append(Pn)
    print('L=', L, '| Fn =', round(Fn,2),'| Pn =', round(Pn,2))

p1.section.plot_centroids()

title = 'Pn_L_C_wlps'

f = plt.figure()
plt.plot(Long, Pns)
plt.scatter(Long, Pns)
plt.title(title)
plt.xlabel('L [mm]')
plt.ylabel('Pn [N]')
#plt.legend()
f.savefig(title+'.png')
plt.show()