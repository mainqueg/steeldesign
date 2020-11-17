from math import pi
import numpy as np
from .appendix_B import B_5, TableA12

def E3_4_e1(Fn, Ae):
    ''' Design axial strength Ec 3.4-1

    Parameters
    ----------
        Fn : float
            El menor de los valores de tension para pandel flexiona, torsional o flexo-torsional
        Ae : float
            Area efectiva calculada a la tension Fn
    Returns
    -------
        fiPn : float
            Resistencia axial de diseño
    Tests
    -----
        >>> round( E3_4_e1(1.5, 1.5), 4)
        1.9125
    '''
    fi_c = 0.85 # factor de resistencia a compresion
    fiPn = fi_c*Fn*Ae
    return fiPn

def E3_3_1_2_e6(E0, K, L, r, eta):
    '''s_ex en Eq 3.3.1.2-6. Tension critica de pandeo flexional

        Parameters
        ----------
        E0 : float
            Modulo elasticidad
        K : float
            Factor de longitud efectiva
        L : float
            longitud del miembro
        r : float
            radio de giro del miembro | sqrt(I/A)
        eta : float
            factor de reduccion plastica | Et(s)/E0

        Returns
        -------
        s_ex : float
            Tension critica de pandeo flexional

        Tests
        -----
            >>> round (E3_3_1_2_e6(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
            2220.56
    '''

    den = (K*L/r)**2
    s_ex = pi**2*E0 / den * eta
    return s_ex

def E3_4_2_e1(E0, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    """Fn = s_t = TB en Eq 3.4.2-1. Tension critica de Torsional
    
        Parameters
        ----------
        E0 : float
            Modulo elasticidad
        Kt : float
            Factor de longitud efectiva de pandeo a torsion
        Lt : float
            longitud de pandeo a torsion
        rx, ry : float
            radio de giro del miembro | sqrt(I/A)
        eta : float
            factor de reduccion plastica | Et(s)/E0
        c_x : float
            coordenada del centroide de la seccion
        sc_x: float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        G0 : float
            Modulo de corte inicial
        J : float
            Constante de torsion de St. Venant  

        Returns
        -------
        Fn : float
            Tension critica de pandeo torsional

        Tests
        -----
            >>> round ( E3_4_2_e1(E0 = 180510, Kt = 0.5, Lt = 1800,
            ... rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59,
            ... sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
            276.66
    """
    Fn = E3_3_1_2_e8(E0,Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J)
    return Fn

def E3_4_3_e1(E0, Kx, Lx, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''Fn de FTB en Eq 3.4.3-1. Tension critica de pandeo Flexo-torsional

        Parameters
        ----------
        E0 : float
            Modulo elasticidad
        Kx : float
            Factor de longitud efectiva de pandeo a flexión en -x-
        Lx : float
            Longitud de pandeo a flexión en -x-
        Kt : float
            Factor de longitud efectiva de pandeo a torsion
        Lt : float
            longitud de pandeo a torsion
        rx, ry : float
            radio de giro del miembro | sqrt(I/A)
        eta : float
            factor de reduccion plastica | Et(s)/E0
        c_x : float
            coordenada del centroide de la seccion
        sc_x: float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        G0 : float
            Modulo de corte inicial
        J : float
            Constante de torsion de St. Venant  

        Returns
        -------
        Fn : float
            Tension critica de pandeo flexo-torsional

        Tests
        -----
            >>> round ( E3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = 1800, Kt = 0.5,
            ... Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59,
            ... sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
            261.53
    '''
    
    x0 = -abs(c_x-sc_x) # distancia desde el centroide al centro de corte, negativo
    r0 = E3_3_1_2_e9(rx, ry, x0) # radio de giro polar
    beta = 1- (x0/r0)**2
    
    t1 = eta/2/beta
    s_ex = E3_3_1_2_e6(E0, Kx, Lx, rx, 1.0)
    s_t = E3_3_1_2_e8(E0,Kt,Lt, rx, ry, 1.0, c_x, sc_x, A, Cw, G0, J)
    raiz = ( (s_ex + s_t)**2 - 4*beta*s_ex*s_t )**0.5
    Fn = t1*(s_ex + s_t - raiz)
    return Fn


def E3_4_3_e3(E0, K, L, r, eta):
    '''Tension critica de pandeo flexional. s_ex en Eq 3.4.3-3.

        Parameters
        ----------
        E0 : float
            Modulo elasticidad
        K : float
            Factor de longitud efectiva
        L : float
            longitud del miembro
        r : float
            radio de giro del miembro | sqrt(I/A)
        eta : float
            factor de reduccion plastica | Et(s)/E0

        Returns
        -------
        s_ex : float
            Tension critica de pandeo flexional

        Tests
        -----
            >>> round (E3_4_3_e3(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
            2220.56
    '''

    s_ex = E3_3_1_2_e6(E0, K, L, r, eta)
    return s_ex

def E3_3_1_2_e8(E0, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''Tension critica de pandeo torsional. s_t en Eq 3.3.1.2-6.

        Ver parametros de seccion en https://sectionproperties.readthedocs.io/en/latest/rst/post.html

        Parameters
        ----------
        E0 : float
            Modulo elasticidad
        Kt : float
            Factor de longitud efectiva a torsion
        Lt : float
            longitud del miembro a torsion
        rx, ry: float
            radio de giro del miembro | sqrt(I/A)
        eta : float
            factor de reduccion plastica | Et(s)/E0
        c_x : float
            coordenada del centroide de la seccion
        sc_x : float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        G0 : float
            Modulo de corte inicial
        J : float
            Constante de torsion de St. Venant  

        Returns
        -------
        s_t : float
                Tension critica de pandeo torsional

        Tests
        -----
            >>> round ( E3_3_1_2_e8(E0 = 180510, Kt = 0.5, Lt = 1800, rx = 40.272,
            ... ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = -23.1, A = 319,
            ... Cw = 215e6, G0 = 69426.9, J = 239), 2)
            276.66
    '''
    
    x0 = -abs(c_x-sc_x)
    r0 = E3_3_1_2_e9(rx, ry, x0)

    t1 = 1/A/r0/r0
    t2_den = (Kt*Lt)**2
    t2 = G0*J + pi**2*E0*Cw/t2_den

    s_t = t1*t2*eta
    return s_t

def E3_3_1_2_e9(rx,ry,x0):
    '''r0 en Eq 3.3.1.2-8. Radio de giro polar.

        Parameters
        ----------
        rx, ry : float
            radios de giro
        x0 : float
            distancia desde el centro de corte al centroide, en valor negativo\n

        Returns
        -------
        r0 : float
            Radio de giro polar

        Tests
        -----
            >>> round( E3_3_1_2_e9(40.272,18.2673,38.69), 2)
            58.76
    '''
    r0 = (rx**2 + ry**2 + x0**2)**0.5
    return r0


## 3.2 Tension Members
def sec3_2(A, Fy):
    '''Tension Members.
    Parameters
    ----------
        An: float,
            net area de la seccion.
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la tension.
        midC: diccionario,
            valores de fi y Tn.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    fi = 0.85
    Tn = An*Fy

    midC = {'Tn': Tn, 'fi': fi}

    return Tn*fi, midC

## 3.3 Flexural Memebers
def sec3_3_1(FY, procedure, comp_flange):
    '''Strength for Bending Only.
    Parameters
    ----------
        An: float,
            net area de la seccion.
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la tension.
        midC: diccionario,
            valores de fi y Tn.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    fiMn_nominal, midC1 = sec3_3_1_1(FY=FY, procedure=procedure, comp_flange=comp_flange)
    fiMn_LTB, midC2 = sec3_3_1_2()

    if Mn_LTB < Mn_nominal:
        fiMn = fiMn_LTB
        midC = midC2
    else:
        fiMn = fiMn_nominal
        midC = midC1

    return fiMn, midC

def sec3_3_1_1(FY, procedure = 'PI', comp_flange = 'UNSTIFF'):
    '''Strength for Bending Only. Nominal Section Strength.
    Parameters
    ----------
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
        procedure: string,
            especifica el procedimiento a implementar (Opciones: PI - PII - LD).
        comp_flange: string;
            determina si las alas en compresion estan rigidizadas o no.
    Returns
    -------
        Mn: float,
            resistencia de diseno a la flexion nominal de la seccion.
        midC: diccionario,
            calculos intermedios y parametros.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    if comp_flange == 'UNSTIFF':    # Unstiffened compresion flanges
        fi = 0.85
    elif comp_flange == 'STIFF':    # Stiffened or partially stiffened flanges
        fi = 0.90

    # hay que calcular de alguna forma Se y pasarlo
    # Se = 

    if procedure == 'PI':    # Procedimiento I - basado en fluencia
        Mn = Procedure_I(Se=Se, FY=FY)

    elif procedure == 'PII':    # Procedimiento II - basado en endurecimiento
        Mn, midC = Procedure_II()

    elif procedure == 'LD':     # Local Distorsion Considerations
        Mn, midC = LocalDistorsion()

    midC['Mn'] = Mn
    midC['fi'] = fi
    fiMn = fi*Mn

    return fiMn, midC

def Procedure_I(Se, FY):
    '''Nominal Section Strength. Procedure I. Based on Initiation of Yielding.
    Parameters
    ----------
        Se: float,
            modulo de seccion elastico efectivo, calculado con la fibra extrema en compresion con f=Fyc o f=Fyc, la que plastifique primero.
        FY: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
    Returns
    -------
        Mn: float,
            resistencia de diseno a la flexion.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    Mn = Se*FY  # Ec 3.3.1.1-1
    return Mn

def Procedure_II():
    '''Nominal Section Strength. Procedure II. Based on Inelastic Reserve Capacity.
    Parameters
    ----------
    
    Returns
    -------
        
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    raise 'NotImplemented'

def LocalDistorsion():
    '''Nominal Section Strength. Local Distorsion Consideration.
    Parameters
    ----------
    
    Returns
    -------
        
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    raise 'NotImplemented'

def sec3_3_1_2(case):
    '''Strength for Bending Only. Lateral Buckling Strength.
    Parameters
    ----------
        An: float,
            net area.
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la flexion segun LTB.
        midC: diccionario,
            calculos intermedios y parametros.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    fi = 0.85
    # plast_factor = B_5(sigma, FY, E0, offset, n)
    # Cb = 

    if case == 'CASE I':
        Mc = E_3_3_1_2_e2(E0, plast_factor, Cb, d, Iyc, L)
        # midC = 

    elif case == 'CASE II':
        r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)
        sigma_ey = E_3_3_1_2_e6(E0=E0, plast_factor=plast_factor, K=Ky, L=Ly, r=ry)
        sigma_t = E_3_3_1_2_e8(E0=E0, plast_factor=plast_factor, Kt=Kt, Lt=Lt, r0=r0, A=A, G0=G0, J=J, Cw=Cw)
        Mc = E_3_3_1_2_e4(Cb=Cb, r0=r0, A=A, sigma_ey=sigma_ey, sigma_t=sigma_t)
        # midC = 

    elif case == 'CASE II':
        raise 'NotImplemented'

    Mn = Sc*Mc/Sf   # Ec 3.3.1.2-1

    fiMn = Mn*fi

    return fiMn, midC


def E_3_3_1_2_e2(E0, plast_factor, Cb, d, Iyc, L):
    '''Lateral Buckling Strength. CASE 1: doubly symmetric I-sections bent about their minor axis.
    Parameters
    ----------
        E0: float,
            odulo de elasticidad inicial.
        plast_factor: float,
            factor de reduccion por plasticidad. 
        Cb: float,
            coeficiente de flexion.
        d: float,
            altura de la seccion.
        Iyc: float,
            momento de inercia de la porcion de la seccion en compresion con respecto al eje vertical.
        L: float,
            longitud del miembro sin soporte.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la tension.
        midC: diccionario,
            valores de fi y Tn.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    Mn = pi**2*E0*Cb*plast_factor*(d*Iyc/L**2)
    return Mn

def E_3_3_1_2_e4(Cb, r0, A, sigma_ey, sigma_t):
    '''Lateral Buckling Strength. CASE 1: doubly symmetric I-sections bent about their minor axis.
    Parameters
    ----------
        Cb: float,
            coeficiente de flexion.
        r0: float,
            radio polar de la seccion con respecto al centro de corte.
        A: float,
            full area.
        sigma_ey: float,
            tension critica de pandeo con respecto al eje y (eje mayor).
        sigma_t: float,
            tension critica de pandeo torsional.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la tension.
        midC: diccionario,
            valores de fi y Tn.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''

def E_3_3_1_2_e6(E0, plast_factor, K, L, r):
    '''Lateral Buckling Strength. Tension critica de pandeo con respecto al eje y (eje mayor).
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        plast_factor: float,
            factor de reduccion por plasticidad.
        K*L: float,
            longitud efectiva.
        r: float,
            radio de giro.
    Returns
    -------
        sigma: float,
            tension critica de pandeo.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    sigma = pi**2*E0/(K*L/r)*plast_factor
    return sigma

def E_3_3_1_2_e8(E0, plast_factor, Kt, Lt, r0, A, G0, J, Cw):
    '''Lateral Buckling Strength. Tension critica de pandeo con respecto al eje y (eje mayor).
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        plast_factor: float,
            factor de reduccion por plasticidad.
        Kt*Lt: float,
            longitud efectiva.
        r0: float,
            radio polar.
        A: float,
            full area.
        G0: float,
            modulo de corte inicial.
        J: float,
            constante de torsion de St Venant.
        Cw: float,
            constante de warping.
    Returns
    -------
        sigma: float,
            tension critica de pandeo torsional.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    sigma = (1/A/r0**2)*(G0*J + pi**2*E0*Cw/(Kt*Lt)**2)*plast_factor
    return sigma

def E_3_3_1_2_e9(rx, ry, x0):
    '''Lateral Buckling Strength. Radio polar de la seccion.
    ----------
        rx: float,
            radio de giro con respecto al eje x (eje menor).
        ry: float,
            radio de giro con respecto al eje y (eje mayor).
    Returns
    -------
        r0: float,
            radio polar de la seccion con respecto al centro de corte.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    r0 = (rx**2 + ry**2 + x0**2)**0.5
    return r0


def sec3_3_2():
    '''Strength for Shear Only.
    Parameters
    ----------
        An: float,
            net area de la seccion.
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
    Returns
    -------
        fiTn: float,
            resistencia de diseno a la tension.
        midC: diccionario,
            valores de fi y Tn.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    fi = 0.85
    Vn = E_3_3_2_e1()

def E_3_3_2_e1(E0, t, plast_factor_shear, h):
    '''Strength for Shear Only. Resistencia nominal al corte.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        t: float,
            espesor de la seccion.
        plast_factor_shear: float,
            coeficiente de reduccion por plasticidad de corte.
        h: float,
            altura de la seccion.
    Returns
    -------
        Vn: float,
            resistencia de diseno a la tension.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''

    Vn = 4.84*E0*t**3*(Gs/G0)/h