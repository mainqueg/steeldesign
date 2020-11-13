'''Ecuaciones de la seccion 2 de ASCE - 8 - 02

'''

from math import pi
import numpy as np

class  sec2_1_1():
    '''Section 2.1.1: Dimensional Limits and Considerations.

    # Parametros
    profile: Dimensiones del perfil
    stiffCondition: Rigidización de los elementos 'UNSTIFFNED' (iii) | STIFFNED_SL (i) | STIFFNED (ii)

    '''
    #valores predefinidos
    def __init__(self, member):
        self.Name = 'Sec2.1.1'
        if member.profile.type == 'c_w_lps':
            self.w = member.profile.B
            self.wf = member.profile.B-member.profile.r_out
            self.t = member.profile.t
            self.L = member.L
            # chequear cada elemento de la seccion: alma/ala/labio
        elif member.profile.type == 'cee':
            self.w = member.profile.B
            self.wf = member.profile.B-member.profile.r_out
            self.t = member.profile.t
            self.L = member.L
            # chequear cada elemento de la seccion: alma/ala
        else:
            print('Error en chequeo de',self.Name,'. El perfil tipo', member.profile.type,'no está implementado.')

    def Cl_1(self, stiffCondition = 'UNSTIFFNED'):
        ''' Determina la relación máxima entre el ancho del ala y su esperor. Los valores limites se dan para tres condiciones de rigidización
        '''
        if stiffCondition == 'UNSTIFFNED':
            ratioAdm = 50.0 # 2.1.1-1.iii
            ratio = self.w/self.t
            print ('Esbeltez =',round(ratio,2), '<','Esbeltez admisible =', ratioAdm)
            return ratio < ratioAdm
        elif stiffCondition == 'STIFFNED':
            ratioAdm = 400.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (round(ratio,2), '<', ratioAdm)
            return ratio < ratioAdm
        elif stiffCondition == 'STIFFNED_SL':
            ratioAdm = 90.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (round(ratio,2), '<', ratioAdm)
            return ratio < ratioAdm
    def Cl_2(self):
        raise 'Not implemented'
    def Cl_3(self):
        '''Especifica el ancho efectivo en el caso de vigas cortas soportando una carga puntual.
        '''
        if self.L < 30*self.wf:
            self.ratio = self.TABLE1()
        else:
            self.ratio = 1.0
        self.w_eff = self.w*self.ratio
    def TABLE1(self):
        '''TABLE 1. Short, Wide Flanges: Maximum Allowable Ratio of Effective Design Width to Actual Width

        # Tests

        #>>> TABLE1()
        '''
        table1 = np.array(((30, 1.00),
                (25, 0.96),
                (20, 0.91),
                (18, 0.89),
                (16, 0.86),
                (14, 0.82),
                (12, 0.78),
                (10, 0.73),
                (8, 0.67),
                (6, 0.55),
        ))
        r = np.interp( table1[:,0], table1[:,1], self.L/self.wf )
        return r
########################### USO

################################ RELEVAMIENTO SECCIONES ASCE 8 ################################

def sec_2_1(self, element):
    '''descripcion

    Parameters
    ----------
    -
    -

    Returns
    -------
    -
    -

    Tests
    -----
    >>>
    
    '''


class load():
    '''Configuracion de la carga aplicada a la seccion y sus elementos.

    Parameters
    ----------
    -element: class,
        elemento de la seccion a la cual se aplicaran las secciones 2.2 y 2.3.
    -distribucion: string,
        determina si la distribucion de la tension es UNIFORME o GRADIENTE.
    -f: float,
        tension uniforme sobre el elemento calculada segun NOTA 3 - RELEVAMIENTO ASCE 8 para el calculo de ancho efectivo.
        para capacidad de carga.
    -f_d: float,
        tension uniforme sobre el elemento calculada segun NOTA 3 - RELEVAMIENTO ASCE 8 para el calculo de ancho efectivo.
        para defelexion reemplazando E0 por Er.
    -f1: float,
        tension en el elemento segun figura 2 - ASCE 8 para el calculo de ancho efectivo para capacidad de carga.
    -f2: float,
        tension en el elemento segun figura 2 - ASCE 8 para el calculo de ancho efectivo para capacidad de carga
    -f_d1: float,
        tension basada en la seccion efectiva para el calculo de ancho efectivo para defelexion.
    f_d2: float,
        tension basada en la seccion efectiva para el calculo de ancho efectivo para defelexion.

    
    '''
    def __init__(self, element = '', distribucion = '', f = '', f_d = '', f1 = '', f2 = '', f_d1 = '', f_d2 = ''):
        self.element = element
        self.sdist = distribucion

#########################################################################################
#########################################################################################
#########################################################################################

import numpy as np
from math import pi


# DIMENSIONAL LIMITS AND CONSIDERATIONS
def sec2_1_1(condition, L, w, stiff_type = 'SL'):
    '''Flange Flat-Width-to-Thickness Considerations.
    Parameters
    ----------
    -condition: string,
        determina si se aplica caso i, ii o iii de la seccion 2.1.1-1.
    -L: float,
        longitud del miembro.
    -w: float,
        ancho del elemento.

    Returns
    -------
    -ratio_1: float
        maximo ratio ancho-plano/espesor segun seccion 2.1.1-1.
    -ratio_3: float
        maximo ratio permitido ancho-diseno/ancho-real segun seccion 2.1.1-3. 

    Tests
    -----

    '''
    if condition == 'i':
        if stiff_type == 'SL': ratio_1 = 50
        if stiff_type == 'OTHER': ratio_1 = 90

    if condition == 'ii': ratio_1 = 400
    if condition == 'iii': ratio_1 = 50

    if L <= 30*w: 
        ratio_3 = TABLE1(L,w)
        w_eff = w*ratio_3
    else: w_eff = w

    return ratio_1, ratio_3

def TABLE1(L, wf):
    '''TABLE 1. Short, Wide Flanges: Maximum Allowable Ratio of Effective Design Width to Actual Width
    Parameters
    ----------
    -L: float,
        longitud del miembro.
    -wf: float,
        ancho del ala proyectado luego del alma.

    Returns
    -------
    -r: float,
        ratio permitido de ancho de diseno a ancho real.

    Tests
    -----
        >>> TABLE1()
    '''
    table1 = np.array(((30, 1.00),
            (25, 0.96),
            (20, 0.91),
            (18, 0.89),
            (16, 0.86),
            (14, 0.82),
            (12, 0.78),
            (10, 0.73),
            (8, 0.67),
            (6, 0.55),
    ))
    r = np.interp( table1[:,0], table1[:,1], L/wf )
    return r

def sec2_1_2(reinforced = 'NO', condition = 'i'):
    '''Maximum Web Depth-to-Thickness Ratio.
    Parameters
    ----------
    -reinforced: string,
        determina si el alma esta reforzada o no para aplicar 1 o 2 de la seccion 2.1.2 segun corresponda.
    -condition: string,
        determina si se aplica caso i o ii de la seccion 2.1.2-2.

    Returns
    -------
    -ratio: float,
        ratio maximo altura/espesor del alma.

    Tests
    -----

    '''
    if reinforced == 'NO': ratio = 200
    if reinforced == 'YES':
        if condition == 'i': ratio = 260
        if condition == 'ii': ratio = 300

    return ratio

# EFFECTIVE WIDTH OF STIFFENED ELEMENTS 
def sec2_2_1(w, t, f, E0, k = 4):
    '''Uniformly Compressed Stiffened Elements. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
    -w: float,
        ancho plano del elemento (ver figura 3 - ASCE 8).
    -t: float,
        espsesor del elemento.
    -f: float
        tension sobre el elemento.
    -E0: float,
        modulo de elasticidad inicial.
    -k: float,
        coeficiente de pandeo en placas para el elemento en consideracion.

    Returns
    -------
    -b_eff: float,
        ancho efectivo del elemento rigidizado bajo compresion uniforme.

    Test
    ----
    >>> sec2_2_1(w= 50, t= 1 , f= 20, E0 = 200e3)
        50
    >>> round(sec2_2_1(w= 50, t= 1 , f= 200, E0 = 200e3), 2)
        44.22
    '''
    esbeltez = E_2_2_1_e4(w, t, f, E0, k)
    if esbeltez <= 0.673: 
            b_eff = w
    else:
        rho = (1-0.22/esbeltez)/esbeltez
        b_eff = w*rho
        
    return b_eff

def sec2_2_2():


# EFFECTIVE WIDTH OF UNSTIFFENED ELEMENTS 
def sec2_3_1(w, t, f, E, k = 0.5):
    '''Uniformly Compressed Unstiffened Elements. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
    -w: float,
        ancho plano del elemento (ver figura 3 - ASCE 8).
    -t: float,
        espsesor del elemento.
    -f: float
        tension sobre el elemento.
    -E0: float,
        modulo de elasticidad inicial.
    -k: float,
        coeficiente de pandeo en placas para el elemento en consideracion.

    Returns
    -------
    -b_eff: float,
        ancho efectivo del elemento no rigidizado bajo compresion uniforme.

    Tests
    -----

    '''

    b_eff = sec2_2_1(w, t, f, E, k)
    return b_eff
    
def E_2_2_1_e4(w, t, k, f, E):
    '''Ecuacion 2.2.1-4.
    Parameters
    ----------
    -w: float,
        ancho plano del elemento (ver figura 3 - ASCE 8).
    -t: float,
        espsesor del elemento.
    -f: float
        tension sobre el elemento.
    -E: float,
        modulo de elasticidad.
    -k: float,
        coeficiente de pandeo en placas para el elemento en consideracion.

    Returns
    -------
    -esbeltez: float,
        esbeltez del elemento considerado.

    Tests
    -----
    >>> round(E_2_2_1_e4(w= 50, t= 1, k=4, f= 200, E= 200e3), 2)
        0.83
    '''
    esbeltez = (1.052/(k**0.5))*(w/t)*(((f/E)**0.5))
    return esbeltez

#########################################################################################
#########################################################################################
#########################################################################################

def sec_2_2_2(self, element = '', load = '', k= ''):
    '''Ancho efectivo de elementos rigidizados.

    Parameters
    ----------
    -w: float,
        ancho plano (ver figura 1 ASCE 8).
    -esbeltez: float,
        factor de esbeltez del elemento rigidizado en compresion uniforme.
    -t: float,
        espesor del elemento rigidizado en compresion uniforme.
    -E0: float,
        modulo de elasticidad inicial.
    -k: float,
        coeficiente de pandeo en placas.
    -Er: float,
        modulo de elasticidad reducido.
    -E_st: float
        modulo secante en el ala tensionada de la seccion.
    -E_sc: float,
        modulo secante en el ala comprimida de la seccion.
    

    Returns
    -------
    -b_eff_LC: float
        ancho efectivo del elemento rigidizado en compresion uniforme para el calculo de capacidad de carga
    -b_eff_D: float,
        ancho efectivo del elemento rigidizado en compresion uniforme para el calculo de deflexion

    Tests
    -----
    >>>
    
    '''

    # COMPRESION UNIFORME EN ELEMENTOS RIGIDIZADOS - SECCION 2.2.1
    if load.dist == 'UNIFORME':

        esbeltez_LC = (1.052/sqrt(k))*(element.profile.w/element.profile.t)*(sqrt(load.f/element.steel.E0))
        Er = (E_st+E_sc)/2
        esbeltez_D = (1.052/sqrt(k))*(element.profile.w/element.profile.t)*(sqrt(load.f_d/element.steel.Er))

        if esbeltez_LC <= 0.673: 
            b_eff_LC = element.profile.w

        else:
            rho = (1-0.22/esbeltez)/esbeltez 
            b_eff_LC = rho*element.profile.w

    # ANCHO EFECTIVO DE ALMA Y ELEMENTOS RIGIDIZADOS CON GRADIENTES DE TENSION - SECCION 2.2.2
    #if load.dist == 'GRADIENTE':



# sec_3_1(self):
#     '''descripcion

#     Parameters
#     ----------
#     -
#     -

#     Returns
#     -------
#     -
#     -

#     Tests
#     -----
#     >>>
    
#     '''
    
# sec_3_2(self):
#     '''descripcion

#     Parameters
#     ----------
#     -
#     -

#     Returns
#     -------
#     -
#     -

#     Tests
#     -----
#     >>>
    
#     '''
    



'''#INPUT:
flangeCURLING = 'False'
shearLag = 'True'
# VERIFICACION
for member in members:
    sec2_1_1 = sec2_1_1(memberProperties(member))
    print ('Los elementos del miembro', member, 'cumplen con las dimensiones requeridas:', sec2_1_1.Cl_1())
    if flangeCURLING:
        sec2_1_1.Cl_2
    if shearLag:
        sec2_1_1.Cl_3'''