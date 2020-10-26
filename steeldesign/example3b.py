from design import ASCE_8_02, member, designParameters
from properties import c_w_lps_profile, c_profile, steel
import matplotlib.pyplot as plt

Long =[300,500,700,1000,1200,1500,1800,2000,2200,2500,2800,3000,3500,5000]

# creo un perfil c on refuerz ode labios
p1 = c_profile(H= 50, B= 50, t= 4, r_out= 3.75)
p1.calculate()
# creo un acero
s = steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')

FTB = []
FBx = []
FBy = []
TB = []

for L in Long:
    # defino parametros de diseño
    dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    # creo un miembro
    m = member(L= L, profile= p1, steel= s, designParameters= dp)
    # creo el analisis
    analysis = ASCE_8_02(m)
    # calculo admisibles
    (Pn_FTB, _) = analysis.s3_FTB()
    (Pn_TB, _) = analysis.s3_TB()
    (x_dir, y_dir) = analysis.s3_FB()
    (Pn, _) = analysis.s3_FTB()
    FTB.append(Pn_FTB)
    TB.append(Pn_TB)
    FBx.append(x_dir[0])
    FBy.append(y_dir[0])

    print('L=',L,'| FTB =', round(Pn_FTB,2),'| TB =', round(Pn_TB,2),'| FBx =', round(x_dir[0],2),'| FBy =', round(y_dir[0],2))
p1.section.plot_centroids()

title = 'Cee'

f = plt.figure()
plt.plot(Long, FTB, label = 'FTB')
plt.scatter(Long, FTB)
plt.plot(Long, TB, label = 'TB')
plt.scatter(Long, TB)
plt.plot(Long, FBx, label= 'FBx')
plt.scatter(Long, FBx)
plt.plot(Long, FBy, label= 'FBy')
plt.scatter(Long, FBy)
plt.title(title)
plt.xlabel('L [mm]')
plt.ylabel('Pn [N]')
plt.legend()
f.savefig(title+'.png')
plt.show()