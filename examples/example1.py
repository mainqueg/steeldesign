'''Combined Distortional and Overall Flexural-Torsional Buckling of Cold-Formed Stainless Steel Sections: Design
Barbara Rossi; Jean-Pierre Jaspart; and Kim J. R. Rasmussen
JOURNAL OF STRUCTURAL ENGINEERING © ASCE / APRIL 2010
DOI: 10.1061/ASCEST.1943-541X.0000147

L=1200
Fig. 1, Curva A*fn,Et 

'''

import steeldesign as sd


# creo un perfil con refuerzo de labios
p1 = sd.c_w_lps_profile(H= 100, B= 50, D= 12, t= 1.5, r_out= 3.75)

# creo un acero
s = sd.steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')

# defino parametros de diseño
dp = sd.designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
# creo un miembro
m = sd.member(L= 1000, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
# calculo admisibles #
(Fn, Pn) = analysis.s3_FTB()

print('Fn =', round(Fn,2),'| Pn =', round(Pn,2))