'''Example 22.1 c-Section wlps (LRFD). 

Lin, Shin-Hua; Yu, Wei-wen; and Galambos, Theodore V., "Illustrative examples based on the ASCE
standard specifcation for the design of cold-formed stainless steel structural members" (1991). Center
for Cold-Formed Steel Structures Library. p257

'''
import steeldesign as sd

# creo perfil
p1 = sd.c_w_lps_profile(H= 8.0, B= 3, D= 0.80, t= 0.105, r_out= ( 0.105+3/16) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# design parameters (default)
dp = sd.designParameters(Cm_x= 1.0, Cm_y= 1.0)
# creo un miembro
m = sd.member(L= 16*12, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)

print('\n3.4 Concentrically Loaded Compression Members')
fiPn, midC_3_4 = analysis.s3_4()
print('fiPn =', round(fiPn,2),'| Pn =', round(midC_3_4['Fn']*midC_3_4['Ae'],2), '| Pno =',  round(midC_3_4['Pno'],2), '| Ae_no =',  round(midC_3_4['Ae_no'],3) )

# Valores de referencia:    fiPn = 10.97 | Pn = 12.91 | Pno = 54.80 | Ae_no = 1.096
# Valores de steeldesign:   fiPn = 10.87 | Pn = 12.79 | Pno = 54.64 | Ae_no = 1.093


print('\n3.3.1 Strength for Bending Only')
fiMn, midC_3_3_1 = analysis.s3_3_1()
print('fiMn =', round(fiMn,2),'| Mn_no =', round(midC_3_3_1['Mn_no'],2), '| Mn_LB =',  round(midC_3_3_1['Mn_LB'],2))

# Valores de referencia:    fiMn = 46.26 | Mn_no = 176.3 | Mn_LB = 54.42
# Valores de steeldesign:   fiMn = 43.30 | Mn_no = 175.8 | Mn_LB = 50.94
# NOTA: La referencia considera eta=1.0, steeldesign obtiene eta= 0.956 -> 50.94/eta = 53.28


print('\n3.3.1.1 Strength for Bending Only on y-axis')
fiMny_plus, fiMny_minus, midC_3_3_1_y = analysis.s3_3_1_1_y()
print('fiMno_y_plus =', round(fiMny_plus,2),'| Mn_no =', round(midC_3_3_1_y['Mn_no'],2))

# Valores de referencia:    fiMno_y_plus = 36.36 | Mn_no = 40.40
# Valores de steeldesign:   fiMno_y_plus = 36.33 | Mn_no = 40.37


print('\n3.5 Combined Axial Load and Bending')
Mu_x = 12.88
Mu_y = 6.44
Pu = 3.22
print('Cargas: Mu_x = ', Mu_x,  ' | Mu_y = ', Mu_y, ' | Pu = ', Pu)
ratios_3_5, states_3_5 = analysis.s3_5(Pu=Pu, fiPn=fiPn, Ae=midC_3_4['Ae_no'], Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=46.26, fiMn_y=36.36)
print('ratios = ', ratios_3_5, ' | state : ', states_3_5)

# Valores de referencia:    ratios = 0.834 | 0.524
# Valores de steeldesign:   ratios = 0.855 | 0.544

# NOTA: En ambos casos el error viene dado por el termino en x, fiMn_x (6.4% error) tiene mas error que fiMn_y