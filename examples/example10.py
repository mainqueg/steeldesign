'''Example 4.5 c-Section wlps (LRFD). 

Wei-wen Yu; Chen, Helen "Cold-formed steel design" (2020). WILEY. p137

'''
import steeldesign as sd

# creo perfil
p1 = sd.c_w_lps_profile(H= 10.0, B= 3.5, D= 0.720, t= 0.075, r_out= (0.075+3/32) )
# creo material
s = sd.steel(FY= 50, E0= 27000, nu= 0.3, n= 4.58, offset= 0.002, name= 'SA301_1_4Hard')
# parametros de diseño
dp = sd.designParameters()
# creo un miembro
m = sd.member(L= 100, profile= p1, steel= s, designParameters= dp)
# creo el analisis
analysis = sd.ASCE_8_02(m)
Se, nEffAreas= analysis.s3_Se_effective(50)
print(Se)

# Valor de referencia 3.211
# Valor de steeldesign 3.196

# NOTA: La referencia usa el AISI S100, que tiene algunas variaciones respecto de ASCE 8
