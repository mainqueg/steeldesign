'''Ecuaciones de la seccion 2 de ASCE - 8 - 02

'''

from math import pi
import numpy as np

class sec2_1_1():
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

def sec2_2_1(w, t , f, E, k = 4):
    '''Uniformly Compressed Stiffened Elements. Load Capacity Determination or Deflection Determination.

    Test
    ----
        >>> b, midC = sec2_2_1(w= 50, t= 1 , f= 20, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 50.00 | esbeltez: 0.26 | rho: 1.00
        >>> b, midC = sec2_2_1(w= 50, t= 1 , f= 200, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 44.22 | esbeltez: 0.83 | rho: 0.88
    '''
    esbeltez = E_2_2_1_e4(w, t, k ,f, E)
    rho = E_2_2_1_e3(esbeltez)
    
    b_eff = w*rho

    midC = {'esbeltez': esbeltez, 'rho': rho}
     
    return b_eff, midC

def E_2_2_1_e3(esbeltez):
    '''Factor rho definida en ecuacion 2.2.1-3

    Parameters
    ----------
        esbeltez : float
            Esbeltez del elemento segun ecuacion 2.2.1-4
    Returns
    -------
        rho : float
            Factor de correccion de ancho
    Raises
    ------
        none
    Tests
    -----
        >>> round( E_2_2_1_e3(esbeltez= 0.83), 2)
        0.89
    '''
    if esbeltez <= 0.673: 
        rho = 1.0
    else:
        rho = (1-0.22/esbeltez)/esbeltez
    return rho

def sec2_3_1(w, t, f, E, k = 0.5):
    '''Uniformly Compressed Unstiffened Elements. Load Capacity Determination or Deflection Determination.

    Parameters
    ----------
        esbeltez : float
            Esbeltez del elemento segun ecuacion 2.2.1-4
    Returns
    -------
        rho : float
            Factor de correccion de ancho
    Raises
    ------
        none
    Test
    ----
        >>> b, midC = sec2_3_1(w= 50, t= 1 , f= 5, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 50.00 | esbeltez: 0.37 | rho: 1.00
        >>> b, midC = sec2_3_1(w= 50, t= 1 , f= 200, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 19.27 | esbeltez: 2.35 | rho: 0.39
    '''
    b_eff, midC = sec2_2_1(w, t, f, E, k)
    return b_eff, midC
    
def E_2_2_1_e4(w, t, k, f, E):
    '''
    Tests
    -----
        >>> round(E_2_2_1_e4(w= 50, t= 1, k=4, f= 200, E= 200e3), 2)
        0.83
    '''
    esbeltez = (1.052/(k**0.5)) * (w/t) * ((f/E)**0.5)
    return esbeltez