
'''Modulo de diseño de estructuras metalicas segun ASCE - 8 - 02

    Classes and functions
    ---------------------
        designParameters : class
            Parametros de diseño asociados a un miembro.

        member : class
            Miembro estructural.

        ASCE_8_02 : class
            Verificaciones segun ASCE 8.

        eta_iter : function
            Se itera con un esquema de newton-rapson para satisfacer la ecuacion f(s): s- FF*eta(s) = 0

    Tests
    -----
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
        >>> (Fn, Pn) = analysis.s3_FTB()
        >>> print('Fn =', round(Fn,2),'| Pn =', round(Pn,2))
        Fn = 142.03 | Pn = 45313.99

        >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
        >>> m = member(L= 1000, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> (Fn, Pn) = analysis.s3_FTB()
        >>> print('Fn =', round(Fn,2),'| Pn =', round(Pn,2))
        Fn = 300.51 | Pn = 95874.54

        >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
        >>> m = member(L= 100, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> (Fn, Pn) = analysis.s3_FTB()
        >>> print('Fn =', round(Fn,2),'| Pn =', round(Pn,2))
        Fn = 337 | Pn = 107515.68

        >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
        >>> m = member(L= 3000, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> (_, Pn_FTB) = analysis.s3_FTB()
        >>> (_, Pn_TB) = analysis.s3_TB()
        >>> (x_dir, y_dir) = analysis.s3_FB()
        >>> print('L=',3000,'| FTB =', round(Pn_FTB,2),'| TB =', round(Pn_TB,2),'| FBx =', round(x_dir[1],2),'| FBy =', round(y_dir[1],2))
        L= 3000 | FTB = 50925.21 | TB = 53988.92 | FBx = 95567.92 | FBy = 74057.88

        >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
        >>> m = member(L= 2000, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> (Fn, Pn) = analysis.s3_FTB()
        >>> print('Fn =', round(Fn,2),'| Pn =', round(Pn,2))
        Fn = 251.05 | Pn = 80093.79

        >>> dp = designParameters(Kx= 0.5, Ky= 0.5, Kz = 0.5)
        >>> m = member(L= 1500, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> (_, Pn_FTB) = analysis.s3_FTB()
        >>> (_, Pn_TB) = analysis.s3_TB()
        >>> (x_dir, y_dir) = analysis.s3_FB()
        >>> print('L=',1500,'| FTB =', round(Pn_FTB,2),'| TB =', round(Pn_TB,2),'| FBx =', round(x_dir[1],2),'| FBy =', round(y_dir[1],2))
        L= 1500 | FTB = 87988.48 | TB = 88632.78 | FBx = 107398.91 | FBy = 93891.32

        ## Sec3
        >>> (fiPn, _) = analysis.s3_4()
        >>> print('fiPc=', round(fiPn, 2) )
        fiPc= 61907.6

        ## sec2_1_1 aplicado a un perfil C
        #>>> v_sec2_1_1 = sec2_1_1(m)
        #>>> v_sec2_1_1.Cl_1('UNSTIFFNED')
        #Esbeltez = 33.33 < Esbeltez admisible = 50.0
        #True

        ## Example 17.1 I-Section (LRFD) (Ver example4.py)
        >>> p1 = I_builtup_c_profile(H= 6, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
        >>> p2 = c_profile(H= 6, B= 1.5, t= 0.135, r_out= (0.135+3/16) )
        >>> p1.calculate()
        >>> p2.calculate()
        >>> p1.J = 2*p2.J 
        >>> s = steel(FY= 30, E0= 27000, nu= 0.3, n= 9.7, offset= 0.002, name= 'SA409_long')
        >>> dp = designParameters(Lx= 14*12, Ly= 7*12, Lz= 7*12)
        >>> m = member(L= 14*12, profile= p1, steel= s, designParameters= dp)
        >>> analysis = ASCE_8_02(m)
        >>> fiPn, midC = analysis.s3_4()
        >>> print('fiPn =', round(fiPn,2),'| Pn =', round(midC['Fn_FBy']*midC['Ae'],2))
        fiPn = 19.78 | Pn = 23.27
        >>> print('Esbeltez de', m.profile.elements[1]['name'],'=', round(m.profile.elements[1]['esbeltez'],2))
        Esbeltez de web = 0.4
        >>> print('Esbeltez de', m.profile.elements[2]['name'],'=', round(m.profile.elements[2]['esbeltez'],2))
        Esbeltez de flange = 0.25
        


'''

from math import pi
from .sec_2 import sec2_1_1, sec2_2_1, sec2_3_1, sec2_4_2
from .sec_3 import E3_4_e1,E3_4_2_e1, E3_4_3_e1, E3_3_1_2_e6, E3_4_3_e1
from .appendix_B import B_2, B_1
from .properties import c_w_lps_profile, c_profile, steel, I_builtup_c_profile


class designParameters:
    '''Parametros de diseño asociados a un miembro.

    Parameters
    ----------
        Kx, Ky, Kz : float
            Factor de longitud efectiva | def : 1.0 | z: direccion axial
        Lx, Ly, Lz : float
            longitud de referencia del miembro | def : 0.0

    Attributes
    ----------
        Kx, Ky, Kz : float
            Factor de longitud efectiva | z: direccion axial
        Lx, Ly, Lz : float
            longitud de referencia del miembro

    Methods
    -------
        none

    Raises
    ------
        none

    Tests
    ------
        En archivo
    '''
    def __init__(self, Kx = 1.0, Ky = 1.0, Kz = 1.0, Lx = 0.0, Ly = 0.0, Lz = 0.0):
        self.Kx = Kx
        self.Ky = Ky
        self.Kz = Kz
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz

class member():
    '''Miembro estructural.

    Parameters
    ----------
        L : float
            Longitud del miembro
        name : string
            Label o nombre del miembro
        profile : class profile
            Clase profile con dimensiones y propiedades de seccion
        steel : class steel
            Clase steel con las propiedades mecanicas y metodos del material
        designParameters : class designParameters
            Clase con los parametros de diseño a considerar en el miembro

    Attributes
    ----------
        name : string
            Label o nombre del miembro
        L : float
            longitud de referencia del miembro
        profile : class profile
            Clase profile con dimensiones y propiedades de seccion
        steel : class steel
            Clase steel con las propiedades mecanicas y metodos del material
        dP : class designParameters
            Clase con los parametros de diseño a considerar en el miembro. Si Li = 0 -> Li = L

    Methods
    -------
        none

    Raises
    ------
        none

    Tests
    -----
        En archivo

    '''

    def __init__(self, L, name = 'none', profile = '', steel = '', designParameters = '', loads = '', reports = ''):

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
            if self.dP.Lx == 0:
                self.dP.Lx = L
            if self.dP.Ly == 0:
                self.dP.Ly = L
            if self.dP.Lz == 0:
                self.dP.Lz = L

class ASCE_8_02:
    ''' Verificaciones segun ASCE 8

    Parameters
    ----------
        member : class member
            Miembro estructural configurado con profile, steel y dP

    Attributes
    ----------
        member : class member
            Miembro estructural configurado con profile, steel y dP
        
    Methods
    -------
        s3_4() : 
            Design axial strength

        s3_FTB() : 
            Tension y Carga críticas de pandeo flexo-torsional

        s3_FB() : 
            Tension y Carga críticas de pandeo flexional

        s3_TB() : 
            Tension y Carga críticas de pandeo torsional
        s2_Ae_compMemb(f) :
            Area efectiva para miembros a compresion calculado para una tension f

    '''

    def __init__(self, member):
        self.member = member
        if not member.profile:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun pefil.')
        if not member.steel:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun acero.')
        if not member.dP:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado parametros de diseño.')

    def s3_4(self):
        '''Design axial strength. 
            
            Ec 3.4-1: Tension menor de estados limites FB, TB, FTB multiplicada por factor de resistencia y area efectiva.
        
        Parameters
        ----------
            none

        Returns
        -------
            fiPn : float
                Resistencia axial de diseño
            [Fn_FB, Fn_TB, Fn_FTB, Ae] : list of float
                Fn_FB: Tension de pandeo flexional
                Fn_TB: Tension de pandeo torsional
                Fn_FTB: Tension de pandeo flexo-torsional
                Ae: Area efectiva calculada a Fn

        Raises
        ------
            none

        Tests
        -----
            En archivo
        '''
        
        ([Fn_FBx, _], [Fn_FBy, _]) = self.s3_FB()
        (Fn_TB, _) = self.s3_TB()
        (Fn_FTB, _) = self.s3_FTB()

        Fn = min(Fn_FBx, Fn_FBy, Fn_TB, Fn_FTB)

        self.s2_Ae_compMemb(Fn)
        Ae = self.member.profile.Ae

        fiPn = E3_4_e1(Fn, Ae)

        midC = {'Fn_FBx': Fn_FBx, 'Fn_FBy': Fn_FBy, 'Fn_TB': Fn_TB, 'Fn_FTB':Fn_FTB, 'Fn': Fn, 'Ae': Ae} # convertir en diccionario

        return fiPn, midC
        
    def s2_Ae_compMemb(self, f):
        '''Area efectiva para miembros a compresion, segun 2.2.1 (stiffned), 2.3.1 (unstiffned) y 2.4.2 (stiffned_w_slps)
        
        Parameters
        ----------
            f : float
                Valor de la tension a compresion uniforme del elemento
        Returns
        -------
            None
        Raises
        ------
            none
        Tests
        -----
            En archivo
        '''
        profile= self.member.profile
        # inicio con el area neta
        profile.Ae = profile.A
        elements = profile.elements
        t= profile.t
        E0= self.member.steel.E0

        for key in elements.keys():
            element = elements[key]
            if element['type'] == 'stiffned':
                b, midC = sec2_2_1(w= element['w'], t= t, f= f, E= E0)
                element['b']= b
                element['rho']= midC['rho']
                element['esbeltez']= midC['esbeltez']
            elif element['type'] == 'unstiffned':
                b, midC = sec2_3_1(w= element['w'], t= t, f= f, E= E0)
                element['b']= b
                element['rho']= midC['rho']
                element['esbeltez']= midC['esbeltez']
            elif element['type'] == 'stiffned_w_slps':
                if elements[3]['name'] == 'lip':
                    d = elements[3]['w']
                else:
                    print('El elemento',3, 'no corresponde al tipo <lip>. Redefinir los elemenentos en el perfil',profile.type)
                    raise Exception('>> Analisis abortado <<')
                b, midC = sec2_4_2(E0=E0, f = f, w= element['w'], t= t, d=d, r_out= profile.r_out)
                element['b']= b
                element['rho']= midC['rho']
                element['esbeltez']= midC['esbeltez']
                element['CASE'] = midC['CASE']
            else:
                print('El elemento:',element['name'], 'del perfil:',profile.name, 'no tiene asignada una clasificacion reconocida:', element['type'])
                raise Exception('>> Analisis abortado <<')

            profile.Ae =  profile.Ae - (element['w']-element['b'])*t


    def s3_FTB(self):
        '''Tensión y carga critica nominal de pandeo flexo-torsional.

            Basado en Ec. 3.4.3-1. Itera sobre Et(s) segun un esquema de Newton-Rapson.
            
        Parameters
        ----------
            none

        Returns
        -------
            Fn : float
                Tension critica de pandeo flexo-torsional
            Pn : float
                Carga critica de pandeo flexo-torsional (sobre area nominal)

        Raises
        ------
            none

        Tests
        -----
            En archivo
        ''' 
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel

        FF = E3_4_3_e1(E0 = steel.E0, G0 = steel.G0,
                        Kx = dP.Kx, Kt = dP.Kz, Lx = dP.Lx, Lt = dP.Lz,
                        rx = profile.rx, ry = profile.ry, c_x = profile.c_x, sc_x = profile.sc_x,
                        A = profile.A, Cw = profile.Cw, J = profile.J,
                        eta = 1)
        Fn = eta_iter(FF,steel)
        if Fn > steel.FY:
            Fn = steel.FY

        Pn = Fn* profile.A
        return Fn, Pn

    def s3_FB(self):
        '''Tensión y carga critica nominal para pandeo a flexion en x e y.

            Basado en Ec. 3.3.1.2-6. Itera sobre Et(s) segun un esquema de Newton-Rapson.

        Parameters
        ----------
            none

        Returns
        -------
            [Fnx, Pnx] : list of float
                Fnx : Tension critica de pandeo flexional sobre el eje -x-
                Pnx : Carga critica de pandeo flexional sobre el eje -x- (sobre area nominal)
            [Fny, Pny] : list of float
                Fny : Tension critica de pandeo flexional sobre el eje -y-
                Pny : Carga critica de pandeo flexional sobre el eje -y- (sobre area nominal)

        Raises
        ------
            none

        Tests
        -----
            En archivo
        '''
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel
        #fi_n = 0.9 # chequear valor
        
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

        return [Fnx, Pnx], [Fny, Pny]

    def s3_TB(self):
        '''Tensión y carga critica nominal para pandeo torsional.

            Basado en Ec. 3.4.2-1. Itera sobre Et(s) segun un esquema de Newton-Rapson.

        Parameters
        ----------
            none

        Returns
        -------
            Fn : float
                Tension critica de pandeo torsional
            Pn : float
                Carga critica de pandeo torsional (sobre area nominal)

        Raises
        ------
            none

        Tests
        -----
            En archivo
        '''
        
        dP = self.member.dP
        profile = self.member.profile
        steel = self.member.steel
        
        FF = E3_4_2_e1(E0= steel.E0, Kt= dP.Kz, Lt= dP.Lz, rx= profile.rx, ry= profile.ry,
                    c_x= profile.c_x, sc_x= profile.sc_x, A= profile.A, Cw= profile.Cw, G0= steel.G0, J= profile.J,
                    eta= 1)
        Fn = eta_iter(FF,steel)
        if Fn > steel.FY:
            Fn = steel.FY
        Pn = Fn* profile.A

        return Fn, Pn

def eta_iter(FF, mat, s = 0):
    ''' A partir de la constante FF, se itera con un esquema de newton-rapson para 
    satisfacer la ecuacion f(s): s- FF*eta(s) = 0

    Parameters
    ----------
        FF : float
            Valor de la ecuacion para eta = 1
        mat : <class steel>
            Material del miembro
        s : float
            Tension incial de la iteracion. Por default s = 0.75*FY

    Tests
    -----
        incluido en test generales
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