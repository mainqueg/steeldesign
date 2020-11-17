'''Combined Distortional and Overall Flexural-Torsional Buckling of Cold-Formed Stainless Steel Sections: Design
Barbara Rossi; Jean-Pierre Jaspart; and Kim J. R. Rasmussen
JOURNAL OF STRUCTURAL ENGINEERING © ASCE / APRIL 2010
DOI: 10.1061/ASCEST.1943-541X.0000147

Fig. 1, Curva Al*fn,Et y A*fn,Et

'''

import steeldesign as sd
import matplotlib.pyplot as plt

Long =[300,500,700,1000,1200,1500,1800,2000,2200,2500,2800,3000,3500,5000]

# creo un perfil c on refuerz ode labios
p1 = sd.c_w_lps_profile(H= 100, B= 50, D= 12, t= 1.5, r_out= 3.75)
p1.calculate()
# creo un acero
s = sd.steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')

Pn_As = []
Pn_Aes = []

for L in Long:
    # defino parametros de diseño
    dp = sd.designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    # creo un miembro
    m = sd.member(L= L, profile= p1, steel= s, designParameters= dp)
    # creo el analisis
    analysis = sd.ASCE_8_02(m)
    # calculo admisibles
    #(Fn, Pn_A) = analysis.s3_FTB()
    fiPn, midC = analysis.s3_4()
    Pn_As.append(midC['Fn']*p1.A)
    Pn_Aes.append(midC['Fn']*p1.Ae)
    Pn_A = midC['Fn']*p1.A
    print('L=', L, '| Fn =', round(midC['Fn'],2),'| Pn_A =', round(Pn_A,2), '| Ae =', round(midC['Ae'],2), '| Pn_Ae =', round(midC['Fn']*midC['Ae'],2) )

#p1.section.plot_centroids()

title = 'Fn_A y Fn_Ae'

f = plt.figure()
plt.plot(Long, Pn_As, label = 'Fn*A')
plt.scatter(Long, Pn_As)
plt.plot(Long, Pn_Aes, label = 'Fn*Ae')
plt.scatter(Long, Pn_Aes)
plt.title(title)
plt.xlabel('L [mm]')
plt.ylabel('Pn [N]')
plt.legend()
f.savefig(title+'.png')
plt.show()