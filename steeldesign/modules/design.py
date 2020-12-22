
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
import numpy as np
from .sec_2 import sec2_1_1_c1,sec2_1_1_c3, sec2_2_1, sec2_3_1, sec2_3_2, sec2_4_2, sec2_2_2
from .sec_3 import sec3_2
# Imports for Section 3.3.1.1
from .sec_3 import sec3_3_1_1, E_3_3_1_1_e1, LocalDistorsion, E_3_3_1_1_e5, E_3_3_1_1_e6, E_3_3_1_1_e7, E_3_3_1_1_e8, E_3_3_1_1_e9
# Imports for Section 3.3.1.2
from .sec_3 import sec3_3_1_2_eta, sec3_3_1_2_3_i, E_3_3_1_2_e1, E_3_3_1_2_e2, E_3_3_1_2_e4, E_3_3_1_2_e6, E_3_3_1_2_e8, E_3_3_1_2_e9
# Imports for Section 3.3.2
from .sec_3 import E_3_3_2_e1
# Imports for Section 3.3.3
from .sec_3 import E_3_3_3_e1, E_3_3_3_e2
# Imports for Section 3.3.4
from .sec_3 import E_3_3_4_e1, E_3_3_4_e2, E_3_3_4_e3, E_3_3_4_e4, E_3_3_4_e5, E_3_3_4_e6, E_3_3_4_e7, E_3_3_4_e8, E_3_3_4_e9, coeff_units
from .sec_3 import E_3_3_4_e10, E_3_3_4_e11, E_3_3_4_e12, E_3_3_4_e13, E_3_3_4_e14, E_3_3_4_e15, E_3_3_4_e17, E_3_3_4_e19, E_3_3_4_e20, E_3_3_4_e21, E_3_3_4_e22
# Imports for Section 3.3.5
from .sec_3 import E_3_3_5_e1, E_3_3_5_e2
# Imports for Section 3.4
from .sec_3 import E_3_4_e1, E_3_4_2_e1, E_3_4_3_e1, E_3_4_3_e3
# Imports for Section 3.5
from .sec_3 import E_3_5_e1, E_3_5_e2, E_3_5_e3, E_3_5_e4, E_3_5_e5
# Imports for Section 4.1
from .sec_4 import E_4_1_1_e1, E_4_1_1_e2, E_4_1_1_e3, E_4_1_1_e4, E_4_1_1_e5, sec_4_1_2
from .appendix_B import B_2, B_1
from .properties import c_w_lps_profile, c_profile, steel, I_builtup_c_profile
from .functions import eta_iter, eta_iter_shear, adjustNeutralAxis, get_linear_stress, TableA12


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
        Cb: float
            Factor de distribucion de momento. Valor por defecto 1.0. Si se espeficica Cb= 0 se calcula internamente.
        Cm_x, Cm_y: float
            coeficiente segun restriccion al movimiento de sus extremos.
        N: float
            longitud de la placa de apoyo donde se encuentran las reacciones o fuerzas concentradas | def : 0.0
        N_theta: float
            angulo entre el plano del alma de la seccion y la superficie de la placa de apoyo | def : 90.0

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
    def __init__(self, Kx = 1.0, Ky = 1.0, Kz = 1.0, Lx = 0.0, Ly = 0.0, Lz = 0.0, cLoadFlag = True, Cb= 1.0, Cm_x = 1.0, Cm_y = 1.0, N = 0.0, N_theta = 90.0):
        self.Kx = Kx
        self.Ky = Ky
        self.Kz = Kz
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz
        self.Cb = Cb
        self.Cm_x = Cm_x
        self.Cm_y = Cm_y
        self.N = N
        self.N_theta = N_theta
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

    def __init__(self, L, name = 'none', profile = '', steel = '', designParameters = '', loads = '', reports = '', loadProfileFromDB= True):

        self.name = name
        self.L = L
        if not profile:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado ningun pefil.')
        else:
            self.profile = profile
            try:
                profile.A
                profile.Ix
                profile.J
            except AttributeError:
                profile.calculate(loadProfileFromDB)

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
        s3_5() :
            Combined Axial Load and Bending
        s3_4() : 
            Design axial strength
        s3_3_1() :
            Strength for Bending Only
        s3_3_2() :
            Strength for Shear Only
        s3_3_3() :
            Strength for Combined Bending and Shear
        s3_3_4() :
            Web Crippling Strength
        s3_3_5() :
            Strength for Combined Bending and Web Crippling
        s3_2() :
            Design Tensile Strength
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


    ## 2.1 Dimensional Limits and Considerations
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
        
        # 2.1.1 Flange Flat-Width-to-Thickness Considerations
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

        # 2.1.2 Maximum Web Depth-to-Thickness Ratio


    ## 3.2 Tension Members
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


    ## 3.2 Flexural Members
    ## 3.3.1 Strength for Bending Only
    def s3_3_1(self, procedure= 'PI', localDistorsion = False, LD_cond = 'i', stress_grad_web = False, stress_grad_web = False):
        '''Design Flexural Strength. Bending Only. Smaller of Sections 3.3.1.1 and 3.3.1.2.
        Parameters
        ----------
            procedure : string,
                Indica el procedimiento a aplicar segun 3.3.1.1
                    PI: 1. Procedure I—Based on Initiation of Yielding
                    PII: 2. Procedure II—Based on Inelastic Reserve Capacity
            localDistorsion: bool,
                determina si se consideran distorsiones locales para la resistencia a la flexion nominal (3.3.1.1-3 [CASE III]).
            LD_cond: string,
                Indica si se usa la condicion
                    3.3.1.1-3-i: pequeñas casi imperceptibles distorsiones locales son aceptadas.
                    3.3.1.1-3-ii: no se permiten distorsiones locales algunas.
            stress_grad_flange: bool,
                determina si el ala esta sometido a gradiente de tension o no.
            stress_grad_web: bool,
                determina si el alma esta sometido a gradiente de tension o no.

            comp_element: string,
                indica si el elemento al cual se le restringen las distorsiones locales esta rigidizado o no.
        Returns
        -------
            fiMn : float
                resistencia de diseno a la flexion.
            midC : dict
                fi: Design factor segun 3.3.1.1 Nominal section strength.
                Mn: resistencia nominal de la seccion a flexion segun 3.3.1.1
                LB_fi: Design factor segun 3.3.1.2 Lateral buckling strength
                LB_Mn: resistencia nominal al Lateral Buckling segun 3.3.1.2.
                Mc: momento critico al lateral buckling.
                eta: factor plastico de reduccion utilizado en 3.3.1.2
                nEffAreas: diccionario con las areas no
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
        dp = self.member.dP
        member = self.member

        # Section 3.3.1.1 - Nominal Strength
        comp_flange = 'UNSTIFF' # valor por defecto
        for element in elements.values(): # determino si el ala esta rigidizada o no
            if element['name'] == 'flange':
                if element['type'] == 'stiffned_w_slps':
                    comp_flange = 'STIFF'
                elif element['type'] == 'unstiffned':
                    comp_flange = 'UNSTIFF'

        if procedure == 'PI':    
            Sex, nEffAreas = self.s3_Se_effective(fFlange= steel.FY)
            fiMn_no, midC = sec3_3_1_1(FY=steel.FY, Se=Sex, procedure=procedure, comp_flange=comp_flange)
            midC['nEffAreas-3.3.1.1'] = nEffAreas
        
        elif procedure == 'PII':
            print('Seccion 3.3.1.1 - Procedimiento II no implementado.')
            raise NotImplementedError

        elif localDistorsion:
            fiMld = s3_3_1_1_LD(LD_cond = 'i', stress_grad_web = False, stress_grad_web = False)
            
        else:
            print('Prodedimiento',procedure,'no roconocido en Section 3.1.1')
            raise Exception('>> Analisis abortado <<')

        # Section 3.3.1.2 - Lateral Buckling Strength
        Sf = profile.Sx

        Mc_eta_LB = sec3_3_1_2_eta(prof_type=profile.type, Cb=dp.Cb, E0=steel.E0, d=profile.H, Iyc=profile.Iy/2, L=member.L,
                                     rx=profile.rx, ry=profile.ry, c_x=profile.c_x, sc_x=profile.sc_x, A=profile.A,
                                     Lx=dp.Lx, Kx=dp.Kx, Ly=dp.Ly, Ky=dp.Ky, Lz=dp.Lz, Kz=dp.Kz,
                                     Cw=profile.Cw, G0=steel.G0, J=profile.J, j=profile.j)
        # construyo ecuacion: f - Mc/Sf = 0
        #                     f - (Mc_eta_LB/Sf)*eta(f) = 0
        #                     f - FF*eta(f) = 0 (itero con eta_iter)
        FF = Mc_eta_LB/Sf
        f = eta_iter(FF=FF, mat=steel)
        if f > steel.FY:
            f = steel.FY    # limite de fluencia
        Sc, nEffAreas= self.s3_Se_effective(f)

        fiMn_LBx, midC2 = E_3_3_1_2_e1(Sc=Sc, Mc=f*Sf, Sf=Sf)

        # Defino que resistencia controla
        fiMnx = min(fiMn_no, fiMn_LBx)
        midC.update(midC2)  # merge entre los diccionarios
        midC.update({'nEffAreas-3.3.1.2': nEffAreas,'fiMn_LBx': fiMn_LBx, 'fiMn_no': fiMn_no})

        return fiMnx, midC

    def s3_3_1_1_y(self, procedure= 'PI', localDistorsion = False):
        '''Design Flexural Strength. Bending Only. Smaller of Sections 3.3.1.1 and 3.3.1.2.
        Parameters
        ----------
            procedure : string
                Indica el procedimiento a aplicar segun 3.3.1.1 
                    PI: 1. Procedure I—Based on Initiation of Yielding
                    PII: 2. Procedure II—Based on Inelastic Reserve Capacity
            localDistorsion: bool
                determina si se consideran distorsiones locales para la resistencia a la flexion nominal (3.3.1.1-3 [CASE III]).
        Returns
        -------
            fiMn : float
                resistencia de diseno a la flexion.
            midC : dict
                fi: Design factor segun 3.3.1.1 Nominal section strength.
                Mn: resistencia nominal de la seccion a flexion segun 3.3.1.1
                LB_fi: Design factor segun 3.3.1.2 Lateral buckling strength
                LB_Mn: resistencia nominal al Lateral Buckling segun 3.3.1.2.
                Mc: momento critico al lateral buckling.
                eta: factor plastico de reduccion utilizado en 3.3.1.2
                nEffAreas: diccionario con las areas no
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

        # Section 3.3.1.1 - Nominal Strength
        comp_flange = 'UNSTIFF' # valor por defecto
        for element in elements.values(): # determino si el ala esta rigidizada o no
            if element['name'] == 'flange':
                if element['type'] == 'stiffned_w_slps':
                    comp_flange = 'STIFF'
                elif element['type'] == 'unstiffned':
                    comp_flange = 'UNSTIFF'

        if procedure == 'PI':
            ## Cs = 1
            tol = 0.005
            f1= 20
            err = 1
            while err > tol:
                fFlange = f1
                Sex, nEffAreas= self.s3_Se_effective_y(fFlange, Cs = 1, origin= 'sec3.3.1-y+')
                cx= elements[1]['sec3.3.1-y+']['cx']
                xCG= profile.c_x + cx
                f1= steel.FY*xCG/(profile.B - xCG)
                err = abs((fFlange - f1)/fFlange)
            fiMny_plus, midC = sec3_3_1_1(FY=steel.FY, Se=Sex, procedure=procedure, comp_flange=comp_flange)
            midC['nEffAreas-3.3.1.1-y+'] = nEffAreas

            ## Cs = -1
            fiMny_minus = 'N/A'

            return fiMny_plus, fiMny_minus, midC

        elif procedure == 'PII':
            print('Seccion 3.3.1.1 - Procedimiento II no implementado.')
            raise NotImplementedError
        elif localDistorsion:
            print('Seccion 3.3.1.1 - Local Distortion Consideration no implementado.')
            raise NotImplementedError
        else:
            print('Prodedimiento',procedure,'no roconocido en Section 3.1.1')
            raise Exception('>> Analisis abortado <<')
    
    def s3_3_1_1_LD(self, LD_cond = 'i', stress_grad_web = False, stress_grad_web = False):
        '''Nominal Section Strength. Local Distorsion Consideration. Equation 3.3.1.1-4.
        Parameters
        ----------
            LD_cond: string,
                Indica si se usa la condicion
                    3.3.1.1-3-i: pequeñas casi imperceptibles distorsiones locales son aceptadas.
                    3.3.1.1-3-ii: no se permiten distorsiones locales algunas.
            stress_grad_flange: bool,
                determina si el ala esta sometido a gradiente de tension o no.
            stress_grad_web: bool,
                determina si el alma esta sometido a gradiente de tension o no.
        Returns
        -------
            fiMld: float,
                resistencia de diseño a la flexion considerando distorsiones locales.
        Raises
        ------
            none
        Tests
        -----
            none
        '''
        steel = self.member.steel
        profile = self.member.profile
        elements = self.member.profile.elements
        dp = self.member.dP
        Sf = profile.Sx
        flange = {}
        web = {}
        
        for element in elements.values():
            if element['name'] == 'flange':
                if element['type'] == 'stiffned_w_slps': 
                    flange['cond'] = 'STIFF'
                    if not stress_grad_flange:
                        _, midC = sec2_4_2(E0=steel.E0, f=steel.FY, w=profile.B-2*profile.r_out, t=profile.t, 
                                                d=profile.D-profile.r_out, r_out=profile.r_out)
                    else: 
                        raise NotImplementedError
                    flange['k'] = midC['k']
                elif element['type'] == 'unstiffned': 
                    flange['cond'] = 'UNSTIFF'
                    if not stress_grad_flange:
                        flange['k'] = 0.5
                    else: 
                        raise NotImplementedError
            if element['name'] == 'web'
                web['cond'] = 'STIFF'
                if not stress_grad_web:
                    web['k'] = 4.0
                else: 
                    raise NotImplementedError

        flange['Fcr'] = E_3_3_1_1_e9(k=flange['k'], E0=steel.E0, w=profile.B-2*profile.r_out, t=profile.t)
        web['Fcr'] = E_3_3_1_1_e9(k=web['k'], E0=steel.E0, w=profile.H-2*profile.r_out, t=profile.t)

        if LD_cond == 'i':
            if flange['cond'] == 'STIFF' or web['cond'] == 'STIFF':
                flange['Fcr'] = eta_iter(FF=flange['Fcr'], mat=steel, eq='B-3')
                flange['fb'] = E_3_3_1_1_e5(Fcr=flange['Fcr'])
                web['Fcr'] = eta_iter(FF=web['Fcr'], mat=steel, eq='B-3')
                web['fb'] = E_3_3_1_1_e5(Fcr=web['Fcr'])

            elif flange['cond'] == 'UNSTIFF' or web['cond'] == 'UNSTIFF':
                flange['Fcr'] = eta_iter(FF=flange['Fcr'], mat=steel, eq='B-4')
                flange['fb'] = E_3_3_1_1_e6(Fcr=flange['Fcr'])
                web['Fcr'] = eta_iter(FF=web['Fcr'], mat=steel, eq='B-4')
                web['fb'] = E_3_3_1_1_e6(Fcr=web['Fcr'])
            else:
                print('Condicion de rigidizacion del elemento |comp_element| no aceptada')
                raise Exception('>> Analisis abortado <<')
        
        elif LD_cond == 'ii':
            if flange['cond'] == 'STIFF' or web['cond'] == 'STIFF':
                flange['Fcr'] = eta_iter(FF=flange['Fcr'], mat=steel, eq='B-3')
                flange['fb'] = E_3_3_1_1_e7(Fcr=flange['Fcr'])
                web['Fcr'] = eta_iter(FF=web['Fcr'], mat=steel, eq='B-3')
                web['fb'] = E_3_3_1_1_e7(Fcr=web['Fcr'])

            elif flange['cond'] == 'UNSTIFF' or web['cond'] == 'UNSTIFF':
                flange['Fcr'] = eta_iter(FF=flange['Fcr'], mat=steel, eq='B-4')
                flange['fb'] = E_3_3_1_1_e8(Fcr=flange['Fcr'])
                web['Fcr'] = eta_iter(FF=web['Fcr'], mat=steel, eq='B-4')
                web['fb'] = E_3_3_1_1_e8(Fcr=web['Fcr'])
            else:
                print('Condicion de rigidizacion del elemento |comp_element| no aceptada')
                raise Exception('>> Analisis abortado <<')

        else:
            print('Condicion |LD_cond| no aceptada ')
            raise Exception('>> Analisis abortado <<')
    
        flange['fiMld'], midC = LocalDistorsion(Sf=Sf, fb=flange['fb'])
        web['fiMld'], midC = LocalDistorsion(Sf=Sf, fb=web['fb'])
        midC.update(flange)
        midC.update(web)
        return min(flange['fiMld'], web['fiMld']), midC

    def s3_Se_effective(self, fFlange, tol = 0.005, maxIter = 100):
        '''
        Parameters
        ----------
            fFlange : float
                Tension a considerar en el elemento a compresion uniforme
            tol : float
                Valor requerido a alcanzar del ratio relativo de la variacion de yMax entre dos iteraciones
            maxIter : int
                Numero maximo de iteraciones admitidas

        '''

        profile= self.member.profile
        elements = profile.elements
        t= profile.t
        E0= self.member.steel.E0
        nEffAreas= {}

        if profile.type in ['I_builtup_cee', 'I_builtup_cee_w_lps']:
            nEf= 2.0
        elif profile.type in ['cee', 'c_w_lps']:
            nEf= 1.0
        else:
            print('Seccion del tipo', profile.type,'no implementada en analisis 3.3.1 Se effecivo')
            raise NotImplementedError
        
        # calculo beff para flange
        flange = elements[1]
        flange['sec3.3.1.1'] = {}
        if 3 in elements.keys():
            lip = elements[3]
            lip['sec3.3.1.1'] = {}
        if flange['name'] != 'flange':
            print('El elemento', 1, 'no corresponde al tipo 1:<flange>. Reordenar los elemenentos en el perfil',profile.type)
            raise Exception('>> Analisis abortado <<')
        elif flange['type'] == 'unstiffned':
            b, midC = sec2_3_1(w= flange['w'], t= t, f= fFlange, E= E0)
            flange['sec3.3.1.1'].update({'b':b,'rho': midC['rho'],'esbeltez': midC['esbeltez']})
            cy_ = (profile.H-t)/2.0
            nEffAreas[1] = {'t': t, 'b_': (flange['w'] - b)*nEf, 'cy_': cy_, 'paralel': True}
        elif flange['type'] == 'stiffned_w_slps':
            if lip['name'] == 'lip':
                d = lip['w']
            else:
                print('El elemento',3, 'no corresponde al tipo <lip>. Reordenar los elemenentos en el perfil',profile.type)
                raise Exception('>> Analisis abortado <<')
            #flange
            b, midC = sec2_4_2(E0= E0, f= fFlange, w= flange['w'], t= t, d= d, r_out= profile.r_out)
            flange['sec3.3.1.1'].update(midC)
            flange['sec3.3.1.1']['b']= b
            cy_ = (profile.H-t)/2.0
            nEffAreas[1] = {'t': t, 'b_': (flange['w'] - b)*nEf, 'cy_': cy_, 'paralel': True}
            
            #lip
            b, midC = sec2_3_2(w= lip['w'], t= t, f3= fFlange, E= E0)
            lip['sec3.3.1.1'].update(midC)
            lip['sec3.3.1.1']['b']= b

            if flange['sec3.3.1.1']['ds'] < b: # ancho efectivo del lip (ver definicion ds en 2.4)
                b = flange['sec3.3.1.1']['ds']
            b_ = lip['w'] - b
            cy_ = (profile.H + b_)/2.0 - profile.D
            nEffAreas[3] = {'t': t, 'b_': b_*nEf , 'cy_': cy_, 'paralel': False}                         
            lip['sec3.3.1.1'].update({'b':b, 'cy_': cy_})
            lip['sec3.3.1.1'].update(midC)
        else:
            print('El elemento:', flange['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', flange['type'])
            raise Exception('>> Analisis abortado <<')
        
        ## calculo el yCG, primer iteracion [web fully effective]
        
        cy, Ix = adjustNeutralAxis(Ix= profile.Ix, A= profile.A, nEffAreas= nEffAreas)
        yMAX = (profile.H/2 + cy) # distancia mayor desde el eje neutro al borde de la seccion
        Se = Ix/yMAX
        flange['sec3.3.1.1'].update({'Se': Se,'Ix': Ix, 'cy': cy})

        # calculo beff para web, itero
        web = elements[2]
        web['sec3.3.1.1']= {}
        if web['name'] != 'web':
            print('El elemento', 2, 'no corresponde al tipo 1:<web>. Reordenar los elemenentos en el perfil',profile.type)
            raise Exception('>> Analisis abortado <<')
        elif web['type'] != 'stiffned':
            print('El elemento:', web['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', web['type'])
            raise Exception('>> Analisis abortado <<')
        
        err = 1.0
        nIter = 0
        while err > tol and nIter < maxIter:
            f1= get_linear_stress(fFlange, yCG= yMAX, y= profile.r_out)
            f2= get_linear_stress(fFlange, yCG= yMAX, y= profile.H - profile.r_out)
            b1, b2, midC = sec2_2_2(w= web['w'], t= t, f1= f1, f2=f2, E0= E0) 
            web['sec3.3.1.1'].update({'b1':b1, 'b2':b2, 'f1': f1, 'f2': f2})
            web.update(midC)

            yMAX_prev = yMAX
            if b1 + b2 < yMAX - profile.r_out:
                b_ = yMAX - profile.r_out - b1 - b2
                cy_= b1 + b_/2.0 - cy # distancia del centroide del area no-efectiva respecto de x-x (incial)
                nEffAreas[2]= {'t': t, 'b_': b_ , 'cy_': cy_, 'paralel': False}
                cy, Ix = adjustNeutralAxis(Ix= profile.Ix, A= profile.A, nEffAreas= nEffAreas)
                yMAX = (profile.H/2 + cy) # distancia mayor desde el eje neutro al borde de la seccion
                
            err = abs((yMAX_prev-yMAX)/yMAX_prev)
            nIter += 1
        if nIter >= maxIter:
            print('Sec. 3, determinacion de Se: Se alcanzo el numero maximo de iteraciones. Error % alcanzado:', err*100)
        
        Se = Ix/yMAX
        flange['sec3.3.1.1'].update({'Se': Se,'Ix': Ix, 'cy': cy})

        return Se, nEffAreas

    def s3_Se_effective_y(self, fFlange, Cs, origin, tol = 0.005, maxIter = 100):
        '''
        Parameters
        ----------
            fFlange : float
                Tension a considerar en el elemento a compresion uniforme
            Cs : int [-1, +1]
                +1: centro de corte a compresion, -1 centro de corte a traccion -> [Mny_plus, Mny_minus]
            tol : float
                Valor requerido a alcanzar del ratio relativo de la variacion de yMax entre dos iteraciones
            maxIter : int
                Numero maximo de iteraciones admitidas

        '''

        profile= self.member.profile
        elements = profile.elements
        t= profile.t
        E0= self.member.steel.E0
        nEffAreas= {}

        # factor de multiplicacion para tener el cuenta elementos duplicados (e.g. flanges, lips)
        if profile.type in ['I_builtup_cee', 'I_builtup_cee_w_lps']:
            raise NotImplementedError
        elif profile.type in ['cee', 'c_w_lps']:
            pass
        else:
            print('Seccion del tipo', profile.type,'no implementada en analisis 3.3.1 Se effecivo')
            raise NotImplementedError
        
        # chequeo si tiene lips
        lipFlag = False
        if 3 in elements.keys():
            lip = elements[3]
            lip[origin] = {}
            lipFlag = True

        # calculo beff para flange (en esta orientacion flanges-> web y lips; web -> flanges )
        # web in uniform compression
        if Cs > 0:
            web = elements[2]
            web[origin]= {}
            if web['name'] != 'web':
                print('El elemento', 2, 'no corresponde al tipo 1:<web>. Reordenar los elemenentos en el perfil',profile.type)
                raise Exception('>> Analisis abortado <<')
            elif web['type'] != 'stiffned':
                print('El elemento:', web['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', web['type'])
                raise Exception('>> Analisis abortado <<')
            b, midC = sec2_2_1(w= web['w'], t= t, f= fFlange, E= E0)
            web[origin].update(midC)
            web[origin]['b']= b
            cx_ = profile.c_x - t/2.0
            nEffAreas[2] = {'t': t, 'b_': (web['w'] - b), 'cy_': cx_, 'paralel': True}
        
            ## calculo el yCG, primer iteracion [web fully effective]
            cx, Iy = adjustNeutralAxis(Ix= profile.Iy, A= profile.A, nEffAreas= nEffAreas)
            xMAX = profile.B -(profile.c_x + cx) # distancia mayor desde el eje neutro al borde de la seccion
            Sex = Iy/xMAX
            web[origin].update({'Sex': Sex,'Iy': Iy, 'cx': cx})
        elif Cs < 0 and lipFlag:
            raise NotImplementedError

        # calculo beff para flange, itero
        flange = elements[1]
        flange[origin] = {}
        if flange['name'] != 'flange':
            print('El elemento', 1, 'no corresponde al tipo 1:<flange>. Reordenar los elemenentos en el perfil',profile.type)
            raise Exception('>> Analisis abortado <<')
        elif flange['type'] == 'unstiffned':
            print('El elemento:', flange['name'], 'del perfil:', profile.name, 'es del tipo:', flange['type'],'. Este perfil no esta implementado en s3_Se_effective_y()')
            raise NotImplementedError
        elif flange['type'] == 'stiffned_w_slps':
            if lip['name'] == 'lip':
                _ = lip['w']                
            else:
                print('El elemento',3, 'no corresponde al tipo <lip>. Reordenar los elemenentos en el perfil',profile.type)
                raise Exception('>> Analisis abortado <<')
            #flange
            err = 1.0
            nIter = 0
            while err > tol and nIter < maxIter:
                f1= get_linear_stress(fFlange, yCG= profile.c_x + cx, y= profile.r_out)
                f2= get_linear_stress(fFlange, yCG= profile.c_x + cx, y= profile.B - profile.r_out)
                b1, b2, midC = sec2_2_2(w= flange['w'], t= t, f1= f1, f2=f2, E0= E0) 
                flange[origin].update({'b1':b1, 'b2':b2, 'f1': f1, 'f2': f2})
                flange.update(midC)

                xMAX_prev = xMAX
                if b1 + b2 < profile.c_x + cx - profile.r_out:
                    b_ = profile.c_x + cx - profile.r_out - b1 - b2
                    cy_= b1 + b_/2.0 - cx # distancia del centroide del area no-efectiva respecto de x-x (incial)
                    nEffAreas[1]= {'t': t, 'b_': b_*2.0 , 'cy_': cy_, 'paralel': False}
                    cx, Iy = adjustNeutralAxis(Ix= profile.Iy, A= profile.A, nEffAreas= nEffAreas)
                    xMAX = profile.B -(profile.c_x + cx) # distancia mayor desde el eje neutro al borde de la seccion
                    
                err = abs((xMAX_prev-xMAX)/xMAX_prev)
                nIter += 1
            if nIter >= maxIter:
                print('Sec. 3, determinacion de Se: Se alcanzo el numero maximo de iteraciones. Error % alcanzado:', err*100)
        else:
            print('El elemento:', flange['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', flange['type'])
            raise Exception('>> Analisis abortado <<')

        Sex = Iy/xMAX
        flange[origin].update({'Sex': Sex,'Iy': Iy, 'cx': cx})

        return Sex, nEffAreas


    ## 3.3.2 Strength for Shear Only
    def s3_3_2(self, FY_v = 0, steel_type='1/4 Hard'):
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

        web = profile.elements[2]
        web['sec3.3.1.1']= {}
        if web['name'] != 'web':
            print('El elemento', 2, 'no corresponde al tipo 1:<web>. Reordenar los elemenentos en el perfil',profile.type)
            raise Exception('>> Analisis abortado <<')
        elif web['type'] != 'stiffned':
            print('El elemento:', web['name'], 'del perfil:', profile.name, 'no tiene asignada una clasificacion reconocida:', web['type'])
            raise Exception('>> Analisis abortado <<')

        t = profile.t
        h = web['w']
        Av = h*t    # Area del alma

        if FY_v == 0:
            FY_v = 0.8*steel.FY

        # asumo Vn = tau*Area
        # construyo ecuacion: tau - FF*eta(tau) = 0
        #                     FF = 4.84*E0*t**3/h/Area
        Vn_eta, _ = E_3_3_2_e1(E0=steel.E0, t=t, h=h)
        FF = Vn_eta/Av
        tau = eta_iter_shear(FF=FF, mat=steel, s=steel.FY/2, steel_type=steel_type)
        Vn, fiVn = E_3_3_2_e1(E0=steel.E0, t=t, h=h, eta= tau/FF)

        limit = 0.95*FY_v*h*t
        if fiVn > limit: fiVn = limit   # no puede superar fluencia del alma

        midC= {'Vn': Vn, 'Av': Av, 'tau': tau}
        return fiVn, midC


    ## 3.3.3 Strength for Combined Bending and Shear
    def s3_3_3(self, Mu, Vu, fiMn = 0, fiVn = 0):
        '''Strength for Combined Bending and Shear.
        Parameters
        ----------
            fiMn: float,
                resistencia de diseno a la flexion.
            fiVn: float,
                resistencia de diseno al corte.
            Mu: float,
                resistencia requerida a la flexion. 
            Vu: float,
                resistencia requerida al corte.
        Returns
        -------
            ratio: float,
                ratio entre las resistencias requeridas y las correspondientes de diseno.
            states: diccionario,
                verificacion de las ecuaciones de interaccion.
        Raises
        ------
            none
        Tests
        -----
            none
        '''
        if fiMn == 0:
            fiMn = s3_3_1()

        if fiVn == 0:
            fiVn = s3_3_2()

        bend = Mu/fiMn
        shear = Vu/fiVn
        states = {}
        if bend > 0.5 and shear > 0.7:
            ratio = E_3_3_3_e2(fiMn, fiVn, Mu, Vu)
            if ratio > 1.0:
                states['Eq 3.3.3-2'] = 'Not Pass'
            else: states['Eq 3.3.3-2'] = 'Pass'
        else:
            ratio = E_3_3_3_e1(fiMn, fiVn, Mu, Vu)
            if ratio > 1.0:
                states['Eq 3.3.3-1'] = 'Not Pass'
            else: states['Eq 3.3.3-1'] = 'Pass'

        return ratio, states


    ## 3.3.4 Web Crippling Strength
    def s3_3_4(self, units, reaction, FlangeLoading = '1'):
        '''Web Crippling Strength.
        Parameters
        ----------
            units: string,
                SI para sistema internacional o US para sistema imperial.
            reaction: string,
                vale 'end' o 'interior' y define si se trata de una carga interior o una de borde (apoyo).
            tableA2_row: string,
                vale '1' (default) o '2', y define si se utiliza la primera 1ra o 2da fila de la tabla A-2.
        Returns
        -------
            
        Raises
        ------
            none
        Tests
        -----
            none
        '''
        steel = self.member.steel
        profile = self.member.profile
        dpar = self.member.dP

        # Parametros

        midC = {}
        fi = 0.70
        midC['fi'] = fi

        FY = steel.FY
        h = profile.H - 2*profile.r_out
        t = profile.t

        Ct =coeff_units(units=units)
        k = E_3_3_4_e21(FY=FY, Ct=Ct)
        m = E_3_3_4_e22(t=t, units=units)

        N = dpar.N
        R = profile.r_out - t
        theta = dpar.N_theta

        # Limits
        if N/t > 210 or N/h > 3.5 or R/t > 6.0:
            print('No se satisfacen los requerimientos para aplicar la Tabla 2 - Seccion 3.3.4')
            raise Exception('>> Analisis abortado <<')

        # Calculo de coeficientes
        C1 = E_3_3_4_e10(FY=FY, Ct=Ct, k=k)
        C2 = E_3_3_4_e11(R=R, t=t)
        C3 = E_3_3_4_e12(FY=FY, Ct=Ct, k=k)
        C4 = E_3_3_4_e13(R=R, t=t)
        C5 = E_3_3_4_e14(k=k)
        C6 = E_3_3_4_e15(h=h, t=t)
        C7 = E_3_3_4_e17(h=h, t=t, k=k)
        C8 = E_3_3_4_e19(h=h, t=t, k=k)
        Ctheta = E_3_3_4_e20(theta=theta)

        # print(N,R,t,theta,k,m,h,Ct,C1,C2,C3,C4,C5,C6,C7,C8,Ctheta)

        # Oppsing Loads Spaced > 1.5h
        if FlangeLoading == '1':

            ## Shapes Having Single Webs
                # Stiffened or Partially Stiffened Flanges
            if profile.type == 'c_w_lps':
                    # End Reaction
                if reaction == 'end':
                    Pn = E_3_3_4_e1(t=t, C3=C3, C4=C4, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                    # Interior Reaction
                elif reaction == 'interior':
                    Pn = E_3_3_4_e4(t=t, C1=C1, C2=C2, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                else:
                    print('Definir si reaction es /end/ o /interior/')
                    raise Exception('>> Analisis abortado <<')

                # Unstiffened Flanges
            elif profile.type == 'cee':
                    # End Reaction
                if reaction == 'end':
                    Pn = E_3_3_4_e2(t=t, C3=C3, C4=C4, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                    # Interior Reaction
                elif reaction == 'interior':
                    Pn = E_3_3_4_e4(t=t, C1=C1, C2=C2, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                else:
                    print('Definir si reaction es /end/ o /interior/')
                    raise Exception('>> Analisis abortado <<')

            ## I-sections or Similar Sections
            elif profile.type == 'I_builtup_cee_wlps' or profile.type == 'I_builtup_cee':
                t = t/2 # se calcula para cada alma individualmente

                # Stiffened, Partially Stiffened and Unstiffened Flanges
                    # End Reaction
                if reaction == 'end':
                    Pn = E_3_3_4_e3(N=N, t=t, FY=FY, C6=C6)*2
                    # Interior Reaction
                elif reaction == 'interior':
                    Pn = E_3_3_4_e5(N=N, t=t, FY=FY, C5=C5, m=m)*2
                else:
                    print('Definir si reaction es /end/ o /interior/')
                    raise Exception('>> Analisis abortado <<')
            else:
                print('Seccion no implementada para Seccion 3.3.4')
                raise Exception('>> Analisis abortado <<')

        # Oppsing Loads Spaced <= 1.5h
        if FlangeLoading == '2':

            ## Shapes Having Single Webs
                # Stiffened or Partially Stiffened Flanges
            if profile.type == 'c_w_lps' or profile.type == 'cee':
                    # End Reaction and Unstiffened Flanges
                if reaction == 'end':
                    Pn = E_3_3_4_e6(t=t, C3=C3, C4=C4, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                    # Interior Reaction
                elif reaction == 'interior':
                    Pn = E_3_3_4_e8(t=t, C1=C1, C2=C2, Ctheta=Ctheta, h=h, N=N, Ct=Ct)
                else:
                    print('Definir si reaction es /end/ o /interior/')
                    raise Exception('>> Analisis abortado <<')

            ## I-sections or Similar Sections
            elif profile.type == 'I_builtup_cee_wlps' or profile.type == 'I_builtup_cee':
                t = t/2 # se calcula para cada alma individualmente
                # Stiffened, Partially Stiffened and Unstiffened Flanges
                    # End Reaction
                if reaction == 'end':
                    Pn = E_3_3_4_e7(t=t, C8=C8, FY=FY, N=N, m=m)*2
                    # Interior Reaction
                elif reaction == 'interior':
                    Pn = E_3_3_4_e9(t=t, C7=C7, FY=FY, N=N, m=m)*2
                else:
                    print('Definir si reaction es /end/ o /interior/')
                    raise Exception('>> Analisis abortado <<')

            else:
                print('Seccion no implementada para Seccion 3.3.4')
                raise Exception('>> Analisis abortado <<')

        midC['Pn'] = Pn
        return fi*Pn, midC


    ## 3.3.5 Combined Bending and Web Crippling Strength
    def s3_3_5(self, Pu, Mu, fiPn = 0, fiMn = 0):
        '''Combined Bending and Web Crippling Strength for unreinforced webs
        Parameters
        ----------
            fiMn: float,
                resistencia de diseno a la flexion, cuando actua solo la flexion.
            fiPn: float,
                resistencia de diseno a una carga concentrada o reaccion, en ausencia de flexion segun seccion 3.3.4.
            Mu: float,
                resistencia requerida a la flexion. 
            Pu: float,
                resistencia requerida a una carga concentrada o reaccion, en ausencia de flexion.
        Returns
        -------
            ratio: float,
                ratio entre las resistencias requeridas y las correspondientes de diseno.
            states: diccionario,
                verificacion de las ecuaciones de interaccion.
        Tests
            none
        '''
        steel = self.member.steel
        profile = self.member.profile
        dpar = self.member.dP

        if fiMn == 0:
            fiMn = s3_3_1()

        if fiPn == 0:
            fiPn = s3_3_4()

        states = {}
        # Single Unreinforced Web
        if profile.type == 'I_builtup_cee_wlps' or profile.type == 'I_builtup_cee':
            ratio = E_3_3_5_e1(Pu=Pu, fiPn=fiPn, Mu=Mu, fiMn=fiMn)
            if ratio > 1.0:
                states['Eq 3.3.5-1'] = 'Not Pass'
            else: states['Eq 3.3.5-1'] = 'Pass'

        # Multiple Unreinforced Web
        # Exception

        elif profile.type == 'c_w_lps' or profile.type == 'cee':
            ratio = E_3_3_5_e1(Pu=Pu, fiPn=fiPn, Mu=Mu, fiMn=fiMn)
            if ratio > 1.0:
                states['Eq 3.3.5-2'] = 'Not Pass'
            else: states['Eq 3.3.5-2'] = 'Pass'

        return ratio, states

    
    # Area efectiva para miembros a compresion calculado para una tension f
    def s2_Ae_compMemb(self, f, origin):
        '''Area efectiva para miembros a compresion, segun 2.2.1 (stiffned), 2.3.1 (unstiffned) y 2.4.2 (stiffned_w_slps)
        
        Parameters
        ----------
            f : float
                Valor de la tension a compresion uniforme del elemento
            origin : string
                Label para almacenar los midC
        Returns
        -------
            Ae : float
                Area efectiva a la tension f
        Raises
        ------
            none
        Tests
        -----
            En archivo
        '''
        profile= self.member.profile
        # inicio con el area neta
        Ae = profile.A
        elements = profile.elements
        t= profile.t
        E0= self.member.steel.E0

        if profile.type in ['I_builtup_cee', 'I_builtup_cee_w_lps']:
            nEf= 4.0
        elif profile.type in ['cee', 'c_w_lps']:
            nEf= 2.0
        else:
            print('Seccion del tipo', profile.type,'no implementada en analisis 3.3.1 Se effecivo')
            raise NotImplementedError

        for element in elements.values():
            if element['type'] == 'stiffned':
                element[origin]= {}
                b, midC = sec2_2_1(w= element['w'], t= t, f= f, E= E0)
                element[origin].update({'b':b,'rho': midC['rho'],'esbeltez': midC['esbeltez']})
                element[origin]['A_'] = (element['w'] - b)*t
            elif element['type'] == 'unstiffned' and element['name'] != 'lip':
                element[origin]= {}
                b, midC = sec2_3_1(w= element['w'], t= t, f= f, E= E0)
                element[origin].update({'b':b,'rho': midC['rho'],'esbeltez': midC['esbeltez']})
                element[origin]['A_'] = (element['w'] - b)*t*nEf
            elif element['type'] == 'stiffned_w_slps':
                element[origin]= {}
                if elements[3]['name'] == 'lip':
                    d = elements[3]['w']
                    lip = elements[3]
                    lip[origin]= {}
                else:
                    print('El elemento',3, 'no corresponde al tipo <lip>. Reordenar los elemenentos en el perfil',profile.type)
                    raise Exception('>> Analisis abortado <<')
                b, midC = sec2_4_2(E0=E0, f = f, w= element['w'], t= t, d=d, r_out= profile.r_out)
                element[origin].update(midC)
                element[origin]['b']= b
                element[origin]['A_'] = (element['w'] - b)*t*nEf

                #lip
                b, midC = sec2_3_1(w= lip['w'], t= t, f= f, E= E0)
                lip[origin].update(midC)
                lip[origin]['b']= b
                if element[origin]['ds'] < b: # ancho efectivo del lip (ver definicion ds en 2.4)
                    lip[origin]['b'] = element[origin]['ds']
                lip[origin]['A_'] = (lip['w'] - lip[origin]['b'])*t*nEf
            elif element['name'] != 'lip':
                print('El elemento:',element['name'], 'del perfil:',profile.name, 'no tiene asignada una clasificacion reconocida:', element['type'])
                raise Exception('>> Analisis abortado <<')

            Ae =  Ae - element[origin]['A_']
        return Ae


    # Tension y Carga críticas de pandeo flexo-torsional
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

    # Tension y Carga críticas de pandeo flexional
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

    # Tension y Carga críticas de pandeo torsional
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


    # 3.4 Concentrically Loaded Compression Members.
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
            fiPno : float
                Resistencia axial de diseño nominal (f=FY)
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
        FY = self.member.steel.FY
        ([Fn_FBx, _], [Fn_FBy, _]) = self.s3_FB()
        (Fn_TB, _) = self.s3_TB()
        (Fn_FTB, _) = self.s3_FTB()

        Fn = min(Fn_FBx, Fn_FBy, Fn_TB, Fn_FTB)

        Ae = self.s2_Ae_compMemb(Fn, origin= 'sec 3.4-fiPn')
        fiPn = E_3_4_e1(Fn, Ae)

        Ae_no = self.s2_Ae_compMemb(FY, origin= 'sec 3.4-fiPno')
        fiPno = E_3_4_e1(FY, Ae_no)

        midC = {'fiPno': fiPno, 'Pno': Ae_no*FY ,'Pn': Ae*Fn, 
                'Fn_FBx': Fn_FBx, 'Fn_FBy': Fn_FBy, 'Fn_TB': Fn_TB, 'Fn_FTB':Fn_FTB,
                'Fn': Fn, 'Ae': Ae, 'Ae_no': Ae_no}

        return fiPn, midC


    # 3.5 Combined Axial Load and Bending.
    def s3_5(self, Pu, fiPn, Ae, Mu_x = 0, Mu_y = 0, fiMn_x = 0, fiMn_y = 0):
        '''Combined Axial Load and Bending.
        Parameters
        ----------
            Pu: float,
                resistencia axial requerida a la compresion.
            fiPn: float,
                resistencia de diseno a la compresion.
            Mu_x, Mu_y: float,
                resistencias requeridas a la flexion.
            fiMn_x, fiMn_y: float,
                resistencias de diseno a la flexion.
            Ae: float,
                area efectiva.
        Returns
        -------
            ratios: float,
                ratios entre las resistencias requeridas y las correspondientes de diseno.
            states: diccionario,
                verificacion de las ecuaciones de interaccion.
        Tests
        -----
        '''
        # Parametros
        steel = self.member.steel
        profile = self.member.profile
        dpar = self.member.dP

        E0 = steel.E0
        FY = steel.FY
        Kx = dpar.Kx
        Ky = dpar.Ky
        Lx = dpar.Lx
        Ly = dpar.Ly
        Ix = profile.Ix
        Iy = profile.Iy
        Cm_x = dpar.Cm_x
        Cm_y = dpar.Cm_y

        Pe_x = E_3_5_e5(E0=E0, Kb=Kx, Lb=Lx, Ib=Ix)
        Pe_y = E_3_5_e5(E0=E0, Kb=Ky, Lb=Ly, Ib=Iy)
        alpha_nx = E_3_5_e4(Pu=Pu, Pe=Pe_x)
        alpha_ny = E_3_5_e4(Pu=Pu, Pe=Pe_y)

        # Ae = 1
        fiPn_0 = E_3_4_e1(Fn=self.member.steel.FY, Ae=Ae)
        # if 1 == 1:
        #     raise NotImplementedError
        # return Cm_x, Cm_y, alpha_nx, alpha_ny, fiPn_0 # para sacar los warnigs BORRAR

        ratios = np.zeros(3)
        states = {}
        if Pu/fiPn > 0.15:
            ratios[0] = E_3_5_e1(Pu=Pu, fiPn=fiPn, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y, alpha_nx=alpha_nx, alpha_ny=alpha_ny, Cm_x=Cm_x, Cm_y=Cm_y)
            ratios[1] = E_3_5_e2(Pu=Pu, fiPn_0=fiPn_0, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y)
            # Verificacion de las ecuaciones de interaccion
            if ratios[0] > 1.0: states['Eq 3.5-1'] = 'Not Pass'
            else: states['Eq 3.5-1'] = 'Pass'
            if ratios[1] > 1.0: states['Eq 3.5-2'] = 'Not Pass'
            else: states['Eq 3.5-2'] = 'Pass'
        else:
            ratios[2] = E_3_5_e3(Pu=Pu, fiPn=fiPn, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y)
            if ratios[2] > 1.0: states['Eq 3.5-3'] = 'Not Pass'
            else: states['Eq 3.5-3'] = 'Pass'

        return ratios, states
        

    # 4.1.1 I-Sections Composed of Two Channels
    def s4_1_1(self, member_type, member_C, q, Ts, Pu = 0, g = 0):
        '''Built-Up Sections. I-Sections Composed of Two Channels.
        Parameters
        ----------
            member_type: string,
                especifica si el miembro esta sometido a comepresion o flexion.
                | igual a: 'compression member' o 'flexural member' |
            member_C: class member,
                Perfil-C que forma el built-up de perfil-I configurado con profile.
            Pu: float,
                carga concentrada o reaccion. Solo definir si member_type es 'flexural member'
            g: float,
                distancia vertical entre las lineas de conexiones mas cercanas a los topes superior e inferior.
                | por default g = altura del perfil |
            q: float,
                carga de diseño sobre la viga para determinar s_max:
                    1. Para carga concentrada o reaccion q es la carga sobre la longitud del soporte (N).
                    2. Para carga distribuida q es 3 veces la misma.
            Ts: float,
                resistencia disponible de la conexion a traccion.
        Returns
        -------
            s_max: float,
                espaciado maximo entre soldaduras u otro tipo de conectores.
        Raises
        ------
            none
        Tests
        -----
            none
        '''
        L = self.member.L
        if g == 0: g = self.profile.H

        if member_type == 'compression member':
            r_cy = member_C.profile.ry
            r_I = self.profile.ry
            s_max = E_4_1_1_e1(L=L, r_cy=r_cy, r_I=r_I)

        elif member_type == 'flexural member':
            s_max = E_4_1_1_e2(L=L)

            profile = self.profile
            B = profile.B
            t = profile.t
            Ix = member_C.profile.Ix
            d = profile.H
            try: D = self.profile.D
            except: D = 0
            m = E_4_1_1_e4(B=B, t=t, Ix=Ix, d=d, D=D)
            
            if self.member.dP.N < s_max: q = E_4_1_1_e5(Pu=Pu, m=m, g=g)

            limit = E_4_1_1_e3(g=g, Ts=Ts, m=m, q=q)
            if s_max > limit: s_max = limit
        
        else:
            print('No se especifica si el member es |compression member| o |flexural member|')
            raise Exception('>> Analisis abortado <<')

        return s_max

    # 4.1.2 Spacing of Connections in Compression
    def s4_1_2(self, t_N, f_s):
        '''Built-Up Sections. Spacing of Connections in Compression.
        Parameters
        ----------
            t_N: float,
                espesor del cover plate or sheet.
            f_s: float,
                tension de servicio sobre el cover plate or sheet.
        Returns
        -------
            s_max: float,
                espaciado maximo entre soldaduras u otro tipo de conectores.
        Raises
        ------
            none
        Tests
        -----
            none
        '''
        Et = self.steel.Et(s=f_s)
        # w = 
        [s_max_1, s_max_2] = sec_4_1_2(t_N=t_N, Et=Et, f_s=f_s, w=w)
        E0 = self.steel.E0
        FY = self.steel.FY
        if w/t < 0.5*(E0/FY)**0.5:  s_min = 1.03*t*(E0/FY)**0.5
        else:    s_min = 1.24*t*(E0/FY)**0.5
        if s_max_2 < s_min: s_max_2 = s_min

        return min(s_max_1, s_max_2)
