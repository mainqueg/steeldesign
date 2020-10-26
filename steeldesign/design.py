'''Modulo de diseño de estructuras metalicas segun ASCE - 8 - 02

    #Tests

    ## steel
    >>> mat = steel(344.8,186200.0, 0.3, 4.58, 0.002, name = 'SA304_1_4Hard')
    >>> round(mat.Et(159.3),2)
    141952.2
    >>> round(mat.Es(159.3),2)
    174334.98
    >>> round(mat.eta(159.3),4)
    0.7624
    >>> mat.name
    'SA304_1_4Hard'
    
    ## member
    >>> m = member(100, 'Uno')
    Advertencia: El miembro Uno no tiene asignado ningun pefil.
    Advertencia: El miembro Uno no tiene asignado ningun acero.
    Advertencia: El miembro Uno no tiene asignado parametros de diseño.

    ## ASCE_8_02
    >>> p1 = c_w_lps_profile(H= 100, B= 50, D= 12, t= 1.5, r_out= 3.75)
    >>> p1.calculate()
    >>> s = steel(FY= 337, E0= 180510.0, nu= 0.3, n= 13.5, offset= 0.002, name= 'SA304_1_4Hard')
    >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    >>> m = member(L= 3200, profile= p1, steel= s, designParameters= dp)
    >>> analysis = ASCE_8_02(m)
    >>> (Pn, fiPn) = analysis.s3_FTB()
    >>> print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))
    Pn = 45313.99 | fiPn = 40782.59
    >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    >>> m = member(L= 3000, profile= p1, steel= s, designParameters= dp)
    >>> analysis = ASCE_8_02(m)
    >>> (Pn, fiPn) = analysis.s3_FTB()
    >>> print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))
    Pn = 50925.21 | fiPn = 45832.69
    >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    >>> m = member(L= 2000, profile= p1, steel= s, designParameters= dp)
    >>> analysis = ASCE_8_02(m)
    >>> (Pn, fiPn) = analysis.s3_FTB()
    >>> print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))
    Pn = 80093.79 | fiPn = 72084.41
    >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    >>> m = member(L= 1000, profile= p1, steel= s, designParameters= dp)
    >>> analysis = ASCE_8_02(m)
    >>> (Pn, fiPn) = analysis.s3_FTB()
    >>> print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))
    Pn = 95874.54 | fiPn = 86287.08
    >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
    >>> m = member(L= 100, profile= p1, steel= s, designParameters= dp)
    >>> analysis = ASCE_8_02(m)
    >>> (Pn, fiPn) = analysis.s3_FTB()
    >>> print('Pn =', round(Pn,2),'| fiPn =', round(fiPn,2))
    Pn = 137276.69 | fiPn = 123549.02

    ## sec2_1_1 aplicado a un perfil C
    >>> v_sec2_1_1 = sec2_1_1(m)
    >>> v_sec2_1_1.Cl_1('UNSTIFFNED')
    Esbeltez = 33.33 < Esbeltez admisible = 50.0
    True

'''

from math import pi
from sec_2 import sec2_1_1
from sec_3 import E3_4_2_e1, E3_4_3_e1, E3_3_1_2_e6, E3_4_3_e1
from appendix_B import B_2, B_1
from properties import c_w_lps_profile, c_profile, steel


class designParameters:
    '''Parametro de diseño asociados a un miembro.

    # Parametros
    K_i = Factor de longitud efectiva | z: direccion axial
    L_i = longitud de referencia del miembro

    '''
    def __init__(self, Kx = 1, Ky = 1, Kz = 1, Lx = 0, Ly = 0, Lz = 0):
        self.Kx = Kx
        self.Ky = Ky
        self.Kz = Kz
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz

class member():
    ''' Crea un miembro estructural.

    # Parametros
    L:                  Longitud
    profile:            Clase profile con dimensiones y metodos de la seccion estructural 
    steel:              Clase steel con las propiedades mecanicas y metodos
    designParameters:   Clase con los parametros de diseño a considerar en el miembro

    '''

    def __init__(self, L, name = 'none', profile = '', steel = '', designParameters = ''):

        self.name = name
        self.L = L
        if not profile:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado ningun pefil.')
        else:
            self.profile = profile

        if not steel:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado ningun acero.')
        else:
            self.steel = steel

        if not designParameters:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado parametros de diseño.')
        else:
            self.dP = designParameters
            if designParameters.Lx == 0:
                designParameters.Lx = L
            if designParameters.Ly == 0:
                designParameters.Ly = L
            if designParameters.Lz == 0:
                designParameters.Lz = L

class ASCE_8_02:
    ''' Verificaciones segun ASCE 8

    # Parametros
    member: <member Class>
    
    '''

    def __init__(self, member):
        self.member = member
        if not member.profile:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun pefil.')
        if not member.steel:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun acero.')
        if not member.dP:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado parametros de diseño.')

    def s3_FTB(self):
        '''Devuelve la carga critica nominal y de diseño de pandeo flexo-torsional.

        Basado en Ec. 3.4.3-1. Itera sobre Et(s) segun un esquema de Newton-Rapson.
        
        Retorna el par (Pn, fiPn)
        ''' 
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel
        fi_n = 0.9 # chequear valor
        FF = E3_4_3_e1(E0 = steel.E0, G0 = steel.G0,
                        Kx = dP.Kx, Kt = dP.Kz, Lx = dP.Lx, Lt = dP.Lz,
                        rx = profile.rx, ry = profile.ry, c_x = profile.c_x, sc_x = profile.sc_x,
                        A = profile.A, Cw = profile.Cw, J = profile.J,
                        eta = 1)
        Fn = eta_iter(FF,steel)
        if Fn > steel.FY:
            Fn = steel.FY

        Pn = Fn* profile.A
        return Pn, fi_n*Pn

    def s3_FB(self):
        '''Devuelve la carga critica nominal y de diseño para pandeo a flexion en x e y.

        Basado en Ec. 3.4.3-1. Itera sobre Et(s) segun un esquema de Newton-Rapson.

        Retorna el par ([Pnx, fiPnx], [Pny, fiPny])
        '''
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel
        fi_n = 0.9 # chequear valor
        
        FFx = E3_3_1_2_e6(E0= steel.E0, K = dP.Kx, L = dP.Lx, r = profile.rx, eta= 1)
        Fnx = eta_iter(FFx,steel)
        if Fnx > steel.FY:
            Fnx = steel.FY
        Pnx = Fnx* profile.A

        FFy = E3_3_1_2_e6(E0= steel.E0, K = dP.Ky, L = dP.Ly, r = profile.ry, eta= 1)
        Fny = eta_iter(FFy,steel)
        if Fny > steel.FY:
            Fny = steel.FY
        Pny = Fny* profile.A

        return [Pnx, fi_n*Pnx], [Pny, fi_n*Pny]

    def s3_TB(self):
        '''Devuelve la carga critica nominal y de diseño para pandeo a flexion en x e y.

        Basado en Ec. 3.4.3-1. Itera sobre Et(s) segun un esquema de Newton-Rapson.

        Retorna ([Pnx, fiPnx], [Pny, fiPny])
        '''
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel
        fi_n = 0.9 # chequear valor
        
        FF = E3_4_2_e1(E0= steel.E0, Kt= dP.Kz, Lt= dP.Lz, rx= profile.rx, ry= profile.ry,
                    c_x= profile.c_x, sc_x= profile.sc_x, A= profile.A, Cw= profile.Cw, G0= steel.G0, J= profile.J,
                    eta= 1)
        Fn = eta_iter(FF,steel)
        if Fn > steel.FY:
            Fn = steel.FY
        Pn = Fn* profile.A

        return Pn, fi_n*Pn

'''
steel(344.8,186200.0, 0.3, 4.58, 0.002, name = 'SA304_1_4Hard').eta(159.3)

members = []
p = C_profile(4,2,50)
s = steel(344,186200)
dP = designParameters(1.5,'stiffned')
m = member(100,'1', p, s, dP)
members.append(m)
p = C_profile(4,2,50)
s = steel(344,186200)
dP = designParameters(1.5,'unstiffned')
m = member(200,'2', p, s, dP)
members.append(m)


for member in members:
    analysis = ASCE_8_02(member)
    print ('Miembro:',member.name,'| Ala:', member.dP.tipoAla, '| Pcr:',round(analysis.Cl_5_5(),2))
    print ('Miembro:',member.name,'| LTB:',round(analysis.Cl_2_5(),2))
    '''

def Fn(L, eta):
    Fn = E3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = L, Kt = 0.5, Lt = L, rx = 40.272, ry = 18.2673,
                    eta = eta, c_x = 15.59, sc_x = 23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239)
    return Fn

def eta_iter(FF, mat, s = 0):
    ''' A partir de la constante FF, se itera con un esquema de newton-rapson para 
    satisfacer la ecuacion f(s): s- FF*eta(s) = 0

    # Parametros:
    FF: Valor de la ecuacion para eta = 1
    mat: <steel Class> Material del miembro
    s: Tension incial de la iteracion. Por default s = 0.75*FY


    #Test
    #>>> round( F_FTB(100), 2)
    430.27
    #>>> round( F_FTB(1000), 2)
    300.5
    #>>> round( F_FTB(2000), 2)
    251.03
    #>>> round( F_FTB(3000), 2)
    159.59
    '''

    # tension inicial para iterar
    if not s:
        s = mat.FY*0.75
    ds = 0.1
    # error tolerado porcentual
    err = 1
    #inicializo el contador de iteraciones
    iterr = 0
    #inicializo eta
    eta = mat.eta(s)
    F = FF*eta

    # funcion para encontrar raices
    fn = s - F
    
    # newton-rapson para encontrar raiz de fn
    while abs((F-s)/s*100) > err and iterr < 100:
        # diferencial de eta
        eta_2 = mat.eta(s+ds)
        # diferencial de F
        F_2 = FF*eta_2
        # diferencial de fn
        fn_2 = s+ds - F_2
        # derivada  dfn/ds
        dfn = (fn_2 - fn)/ds
        # nuevo valor de s
        s = s - fn/dfn

        # actualizo valores, itero
        eta = mat.eta(s)
        F = FF*eta
        fn = s - F
        iterr += 1
        #print(iterr, s, F, 100-(F-s)/s*100)
    if abs((F-s)/s*100) > err:
        print('Se excedieron las 100 iteraciones')
    return F

def F_FTB(L, s = 0):
    '''

    #Test
    #>>> round( F_FTB(100), 2)
    430.27
    #>>> round( F_FTB(1000), 2)
    300.5
    #>>> round( F_FTB(2000), 2)
    251.03
    #>>> round( F_FTB(3000), 2)
    159.59

    '''
    mat = steel(FY= 337, E0 = 180510, nu = 0.3, n = 13.5, offset = 0.002)
    
    # tension inicial para iterar
    if not s:
        s = mat.FY*0.75
    ds = 0.1
    # error tolerado porcentual
    err = 1
    #inicializo el contador de iteraciones
    iterr = 0
    #inicializo eta
    eta = mat.eta(s)
    #calculo el primer valor de Fn para eta = 1
    FF =Fn(L, 1)
    F = FF*eta

    # funcion para encontrar raices
    fn = s - F
    
    # newton-rapson para encontrar raiz de fn
    while abs((F-s)/s*100) > err and iterr < 100:
        eta_2 = mat.eta(s+ds)
        F_2 = FF*eta_2
        fn_2 = s+ds - F_2
        dfn = (fn_2 - fn)/ds
        s = s - fn/dfn

        eta = mat.eta(s)
        F = FF*eta
        fn = s - F
        iterr += 1
        #print(iterr, s, F, 100-(F-s)/s*100)
    if abs((F-s)/s*100) > err:
        print('Se excedieron las 100 iteraciones')
    print(s)
    return F

#for L in range(100,4000,100):
#print(F_FTB(3200))