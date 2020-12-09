
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
from .sec_2 import sec2_1_1_c1,sec2_1_1_c3, sec2_2_1, sec2_3_1, sec2_4_2
#from .sec_2 import sec2_1_1, sec2_2_1, sec2_3_1, sec2_4_2
from .sec_3 import sec3_2
# Imports for Section 3.3.1.1
from .sec_3 import sec3_3_1_1, E_3_3_1_1_e1, LocalDistorsion
# Imports for Section 3.3.1.2
from .sec_3 import sec3_3_1_2_eta, sec3_3_1_2_3_i, E_3_3_1_2_e1, E_3_3_1_2_e2, E_3_3_1_2_e4, E_3_3_1_2_e6, E_3_3_1_2_e8, E_3_3_1_2_e9
# Imports for Section 3.3.2
from .sec_3 import E_3_3_2_e1
# Imports for Section 3.3.3
from .sec_3 import E_3_3_3_e1, E_3_3_3_e2
# Imports for Section 3.3.4

# Imports for Section 3.4
from .sec_3 import E_3_4_e1, E_3_4_2_e1, E_3_4_3_e1, E_3_4_3_e3
# Imports for Section 3.5
from .sec_3 import E_3_5_e1, E_3_5_e2, E_3_5_e3, E_3_5_e4, E_3_5_e5
from .appendix_B import B_2, B_1
from .properties import c_w_lps_profile, c_profile, steel, I_builtup_c_profile
from .functions import eta_iter


class designParameters:
    '''Parametros de diseño asociados a un miembro.

    Parameters
    ----------
        Kx, Ky, Kz : float
            Factor de longitud efectiva | def : 1.0 | z: direccion axial
        Lx, Ly, Lz : float
            longitud de referencia del miembro | def : 0.0
        cLoadFlag : bool
            Indica si el miembro soporta cargas puntuales para realizar chequeo segun 2.1.1-3 Shear Lag Effects

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
    def __init__(self, Kx = 1.0, Ky = 1.0, Kz = 1.0, Lx = 0.0, Ly = 0.0, Lz = 0.0, cLoadFlag = True):
        self.Kx = Kx
        self.Ky = Ky
        self.Kz = Kz
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz
        self.cLoadFlag = cLoadFlag

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

    def s2_1(self):
        '''Dimensional Limits and Considerations. 
        2.1.1 Flange Flat-Width-to-Thickness Considerations
            2.1.1-1 Maximum Flat-Width-to-Thickness Ratios
            2.1.1-2 Flange Curling NOT IMPLEMENTED
            2.1.1-3 Shear Lag Effects—Unusually Short Spans Supporting Concentrated Loads
        2.1.2 Maximum Web Depth-to-Thickness Ratio

        Parameters
        ----------
            none
        Returns
        -------
            none
        Raises
        ------
            none
        Tests
        -----
            En archivo
        '''
        profile = self.member.profile
        elements = profile.elements
        
        for key in elements.keys():
            element = elements[key]
            # condition i
            if element['type'] == 'stiffned_w_slps':
                ratio_adm_1, midC = sec2_1_1_c1(condition= 'i', w= element['w'], t= profile.t)
                element['ratioAdm_1']= ratio_adm_1
                element['ratio_1']= midC['ratio_1']
                element['condition']= 'i'
                if element['ratio_1'] > element['ratioAdm_1']:
                    print('El elemento:',key , element['name'],'del perfil:',profile.name, 'excede los limites la clausula 2.2.1-1')
                    raise Exception('>> Analisis abortado <<')
                # 2.1.1-3 Shear Lag Effects - Flanges
                if element['name'] == 'flange' and self.member.dP.cLoadFlag:
                    ratio_3, _ = sec2_1_1_c3(L = self.member.L*2, wf= element['wf'])
                    element['ratio_3'] = ratio_3
                    if ratio_3 < 1.0:
                        element['beff_max'] = element['w']*ratio_3
            # condition ii
            elif element['name'] == 'web':
                ratio_adm_1, midC = sec2_1_1_c1(condition= 'ii', w= element['w'], t= profile.t)
                element['ratioAdm_1']= ratio_adm_1
                element['ratio_1']= midC['ratio_1']
                element['condition']= 'ii'
                if element['ratio_1'] > element['ratioAdm_1']:
                    print('El elemento:',key , element['name'],'del perfil:',profile.name, 'excede los limites la clausula 2.2.1-1')
                    raise Exception('>> Analisis abortado <<')
            # condition iii
            elif element['type'] == 'unstiffned' or (element['type'] == 'stiffned_w_slps' and element['Is']<element['Ia']):
                ratio_adm_1, midC = sec2_1_1_c1(condition= 'iii', w= element['w'], t= profile.t)
                element['ratioAdm_1']= ratio_adm_1
                element['ratio_1']= midC['ratio_1']
                element['condition']= 'iii'
                if element['ratio_1'] > element['ratioAdm_1']:
                    print('El elemento:',key , element['name'],'del perfil:',profile.name, 'excede los limites la clausula 2.2.1-1')
                    raise Exception('>> Analisis abortado <<')
                # 2.1.1-3 Shear Lag Effects - Flanges
                if element['name'] == 'flange' and self.member.dP.cLoadFlag:
                    ratio_3, _ = sec2_1_1_c3(L = self.member.L*2, wf= element['wf'])
                    element['ratio_3'] = ratio_3
                    if ratio_3 < 1.0:
                        element['beff_max'] = element['w']*ratio_3
            else:
                print('El elemento:',element['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', element['type'])
                raise Exception('>> Analisis abortado <<')


    def s3_2(self):
        '''Design Tensile Strength. Eq 3.2-1.
        Parameters
        ----------
            none
        Returns
        -------
            fiTn : float
                Resistencia a la tension de diseño.
            [Tension_fi, Tension_Tn, An] : list of float
                Tension_fi: coeficiente de diseno en tension.
                Tension_Tn: resistencia nominal a la tension.
                An: area neta de la seccion.
        Raises
        ------
            none
        Tests
        -----
            En archivo
        '''
        profile = self.member.profile
        steel = self.member.steel
        # Area neta igual a Area total ??
        An = profile.A
        FY = steel.FY
        fiTn, midC = sec3_2(An=An, FY=FY)
        midC['An'] = An

        return fiTn, midC

    
    def s3_3_1(self, LD = 'NO'):
        '''Design Flexural Strength. Bending Only. Smaller of Sections 3.3.1.1 and 3.3.1.2.
        Parameters
        ----------
            LD: string,
                determina si se consideran distorsiones locales para la resistencia a la flexion nominal (3.3.1.1-CASE III).
        Returns
        -------
            fiMn: float,
                resistencia de diseno a la flexion.
            [Nominal_fi, Nominal_Mn, LB_fi, LB_Mn, Mc, eta]: list of float,
                Nominal_fi: factor de diseno.
                Nominal_Mn: resistencia nominal de la seccion a flexion.
                LB_fi: factor de diseno.
                Lb_Mn: resistencia nominal al Lateral Buckling.
                Mc: momento critico.
                eta: factor plastico de reduccion.
        Raises
        ------
            none
        Tests
        -----
            En archivo
        '''
        steel = self.member.steel
        profile = self.member.profile
        elements = self.member.profile.elements
        dpar = self.member.dP
        member = self.member

        # Section 3.3.1.1 - Nominal Strength
        for key in elements.keys(): # determino si el ala esta rigidizada o no
            element = elements[key]
            if element['name'] == 'flange':
                if element['type'] == 'stiffned_w_slps':
                    comp_flange = 'STIFF'
                if element['type'] == 'unstiffned':
                    comp_flange = 'UNSTIFF'

        if  LD == 'YES': # determino el procedimiento para 3.3.1.1
            procedure = 'LD'
        else:
            procedure = 'PI'

        FY = steel.FY
        # Valor corresponfiente al example 8.1
        # Falta implementar el calculo de Se
        Se = 1.422

        fiMn_Nominal, midC = sec3_3_1_1(FY=FY, Se=Se, procedure=procedure, comp_flange=comp_flange)


        # Section 3.3.1.2 - Lateral Buckling Strength
        prof_type = profile.type
        E0 = steel.E0
        d = profile.H
        Iyc = profile.Iy/2
        L = member.L
        rx = profile.rx
        ry = profile.ry
        c_x = profile.c_x
        sc_x = profile.sc_x
        A = profile.A
        Lx = dpar.Lx
        Kx = dpar.Kx
        Ly = dpar.Ly
        Ky = dpar.Ky
        Lz = dpar.Lz
        Kz = dpar.Kz
        Cw = profile.Cw
        G0 = steel.G0
        J = profile.J
        beta = 0
        # Valor corresponfiente al example 8.1
        # Falta implementar el calculo de Cb
        Cb = 1.75

        Sf = profile.Sx
        # Valor corresponfiente al example 8.1
        # Falta implementar el calculo de Sc
        Sc = 1.470

        Mc_eta_LB = sec3_3_1_2_eta(prof_type=prof_type, Cb=Cb, E0=E0, d=d, Iyc=Iyc, L=L, rx=rx, ry=ry, c_x=c_x, sc_x=sc_x, 
                                    A=A, Lx=Lx, Kx=Kx, Ly=Ly, Ky=Ky, Lz=Lz, Kz=Kz, Cw=Cw, G0=G0, J=J, beta=beta)
        # construyo ecuacion: f - Mc/Sf = 0
        #                     f - (Mc_eta_LB/Sf)*eta(f) = 0
        #                     f - FF*eta(f) = 0 (itero con eta_iter)
        FF = Mc_eta_LB/Sf
        f = eta_iter(FF=FF, mat=steel)
        eta = f/FF

        fiMn_LB, midC2 = E_3_3_1_2_e1(Sc=Sc, Mc=Mc_eta_LB*eta, Sf=Sf)

        # Defino que resistencia controla
        fiMn = min(fiMn_Nominal, fiMn_LB)
        midC.update(midC2)  # merge entre los diccionarios

        return fiMn, midC

    def s3_3_2(self, FY_v = 0):
        '''Design Strength for Shear Only. Shear Buckling.
        Parameters
        ----------
            FY_v: float,
                tension de fluencia de corte. Ver tabla A1 -  ASCE 8.
        Returns
        -------
            fiVn: float,
                resistencia de diseno al corte.
            [Shear_fi, Vn, Av]: list of float,
                Shear_fi: factor de diseno.
                Vn: resistencia nominal de la seccion a corte.
                Av: area para el calculo de resistencia a corte.
        Raises
        ------
            none
        Tests
        -----
            >>> 
        '''
        steel = self.member.steel
        profile = self.member.profile

        E0 = steel.E0
        FY = steel.FY
        t = profile.t
        h = profile.H - 2*profile.r_out
        Av = h*t    # Area del alma

        if FY_v == 0:
            FY_v = 0.8*FY

        # asumo Vn = tau*Area
        # construyo ecuacion: tau - FF*eta(tau) = 0
        #                     FF = 4.84*E0*t**3/h/Area
        Vn_eta = E_3_3_2_e1(E0=E0, t=t, h=h)
        FF = Vn_eta/Av
        tau = eta_iter(FF=FF, mat=steel)
        Vn = tau*Av

        fi = 0.85
        fiVn = fi*Vn
        limit = 0.95*FY_v*h*t
        if fiVn > limit: fiVn = limit   # no puede superar fluencia del alma

        midC= {'Shear_fi': fi, 'Vn': Vn, 'Av': Av}
        return fi*Vn, midC


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

        fiPn = E_3_4_e1(Fn, Ae)

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
                    print('El elemento',3, 'no corresponde al tipo <lip>. Reordenar los elemenentos en el perfil',profile.type)
                    raise Exception('>> Analisis abortado <<')
                b, midC = sec2_4_2(E0=E0, f = f, w= element['w'], t= t, d=d, r_out= profile.r_out)
                element['b']= b
                element['rho']= midC['rho']
                element['Is']= midC['Is']
                element['Ia']= midC['Ia']
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

        FF = E_3_4_3_e1(E0 = steel.E0, G0 = steel.G0,
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
        
        FFx = E_3_3_1_2_e6(E0= steel.E0, K = dP.Kx, L = dP.Lx, r = profile.rx)
        Fnx = eta_iter(FFx,steel)
        if Fnx > steel.FY:
            Fnx = steel.FY
        Pnx = Fnx* profile.A

        FFy = E_3_3_1_2_e6(E0= steel.E0, K = dP.Ky, L = dP.Ly, r = profile.ry)
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
        
        FF = E_3_4_2_e1(E0= steel.E0, Kt= dP.Kz, Lt= dP.Lz, rx= profile.rx, ry= profile.ry,
                    c_x= profile.c_x, sc_x= profile.sc_x, A= profile.A, Cw= profile.Cw, G0= steel.G0, J= profile.J,
                    eta= 1)
        Fn = eta_iter(FF,steel)
        if Fn > steel.FY:
            Fn = steel.FY
        Pn = Fn* profile.A

        return Fn, Pn

    def s3_5(self, Pu, fiPn, Mu_x, Mu_y, fiMn_x, fiMn_y):
        '''
        '''
        # Parametros
        steel = self.member.steel
        profile = self.member.profile
        dpar = self.member.dP

        E0 = steel.E0
        Kx = dpar.Kx
        Ky = dpar.Ky
        Lx = dpar.Lx
        Ly = dpar.Ly
        Ix = profile.Ix
        Iy = profile.Iy

        Cm_x = 0.85
        Cm_y = 0.85

        Pe_x = E_3_5_e5(E0=E0, Kb=Kx, Lb=Lx, Ib=Ix)
        Pe_y = E_3_5_e5(E0=E0, Kb=Ky, Lb=Ly, Ib=Iy)
        alpha_nx = E_3_5_e4(Pu=Pu, Pe=Pe_x)
        alpha_ny = E_3_5_e4(Pu=Pu, Pe=Pe_y)

        # Ae = 
        fiPn_0 = E_3_4_e1(Fn=FY, Ae=Ae)

        

        
