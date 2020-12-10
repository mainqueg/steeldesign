
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
from .sec_2 import sec2_1_1_c1,sec2_1_1_c3, sec2_2_1, sec2_3_1, sec2_3_2, sec2_4_2, sec2_2_2
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
from .functions import eta_iter, adjustNeutralAxis, get_linear_stress


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
    def __init__(self, Kx = 1.0, Ky = 1.0, Kz = 1.0, Lx = 0.0, Ly = 0.0, Lz = 0.0, cLoadFlag = True, Cb= 1.0, Cm_x = 0.85, Cm_y = 0.85, N = 0.0, N_theta = 90.0):
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
        s3_4() : 
            Design axial strength
        s3_3_1() :
            Strength for Bending Only
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

    
    def s3_3_1(self, procedure= 'PI', localDistorsion = False):
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
        else:
            print('Prodedimiento',procedure,'no roconocido en Section 3.1.1')
            raise Exception('>> Analisis abortado <<')

        if localDistorsion:
            print('Seccion 3.3.1.1 - Local Distortion Consideration no implementado.')
            raise NotImplementedError

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
        if localDistorsion:
            print('Seccion 3.3.1.1 - Local Distortion Consideration no implementado.')
            raise NotImplementedError

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
        else:
            print('Prodedimiento',procedure,'no roconocido en Section 3.1.1')
            raise Exception('>> Analisis abortado <<')

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
        if tau > FY_v:
            tau = FY_v    # limite de fluencia en corte
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

        Ae = 1
        fiPn_0 = E_3_4_e1(Fn=self.member.steel.FY, Ae=Ae)
        if 1 == 1:
            raise NotImplementedError
        return Cm_x, Cm_y, alpha_nx, alpha_ny, fiPn_0 # para sacar los warnigs BORRAR

        if Pu/fiPn > 0.15:
            ratio_1 = E_3_5_e1(Pu=Pu, fiPn=fiPn, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y, alpha_nx=alpha_nx, alpha_ny=alpha_ny, Cm_x=Cm_x, Cm_y=Cm_y)
            ratio_2 = E_3_5_e2(Pu=Pu, fiPn_0=fiPn_0, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y)
            return ratio_1, ratio_2
        else:
            ratio_1 = E_3_5_e3(Pu=Pu, fiPn=fiPn, Mu_x=Mu_x, Mu_y=Mu_y, fiMn_x=fiMn_x, fiMn_y=fiMn_y)
            return ratio_1
        

        
