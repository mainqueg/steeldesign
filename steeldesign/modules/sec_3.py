from math import pi
import numpy as np
from .appendix_B import B_5, TableA12

## 3.2 Tension Members
def sec3_2(An, FY):
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
    Tn = An*FY

    midC = {'Tn': Tn, 'fi': fi}

    return Tn*fi, midC

## 3.3 Flexural Memebers
def E_3_3_1_1_e1(Se, FY):
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
    Mn = Se*FY
    return Mn

def sec3_3_1_2_CASEIII(E0, eta, Cb, L, Kx, Ky, Lt, Kt, rx, ry, c_x, sc_x, A, G0, J, Cw, j, axis):
    '''Strength for Bending Only. Lateral Buckling Strength.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        eta: float,
            factor de reduccion por plasticidad.
        Cb: float,
            coeficiente de flexion.
        L: float,
            longitud del miembro.
        Kx,Ky: float,
            coeficientes de longitud efectiva para flexion.
        Kt*Lt: float,
            longitud efectiva para torsion.
        rx, ry: float,
            radios de giro (eje x es el eje de simetria).
        c_x: float,

        sc_x: float,

        A: float,
            full area.
        G0: float,
            modulo de corte inicial.
        J: float,
            constante de torsion de St Venant.
        Cw: float,
            constante de warping.
        j: float,
            constante monosimetrica.
        axis: string,
            determina si la flexion se produce en el eje menor (symm axis) o el eje mayor (perp symm axis).
    Returns
    -------
        Mc: float,
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
    x0 = -abs(c_x-sc_x)
    r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)
    sigma_t = E_3_3_1_2_e8(E0=E0, eta=eta, Kt=Kt, Lt=Lt, r0=r0, A=A, G0=G0, J=J, Cw=Cw)
    midC['sigma_et'] = sigma_et

    # Flexion en el eje de simetria
    if axis == 'minor': 
        sigma_ey = E_3_3_1_2_e6(E0=E0, eta=eta, K=Ky, L=L, r=r)
        midC['sigma_ey'] = sigma_ey
        Mc = E_3_3_1_2_e4(Cb=Cb, r0=r0, A=A, sigma_ey=sigma_ey, sigma_t=sigma_t)

    # Flexion en el eje perpendicular al eje de simetria
    elif axis == 'mayor':   
        sigma_ex = E_3_3_1_2_e6(E0=E0, eta=eta, K=Kx, L=L, r=r)
        midC['sigma_ex'] = sigma_ex
        Mc = E_3_3_1_2_e5(Cb=Cb, Cs=Cs, r0=r0, A=A, sigma_ex=sigma_ex, sigma_t=sigma_t, j=j)
    
    return Mc, midC

def E_3_3_1_2_e2(E0, Cb, d, Iyc, L):
    '''Lateral Buckling Strength. CASE I: doubly symmetric I-sections bent about their minor axis. 
    Parameters
    ----------
        E0: float,
            odulo de elasticidad inicial.
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
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    Mc_eta = pi**2*E0*Cb*(d*Iyc/L**2)
    return Mc_eta

def E_3_3_1_2_e4(Cb, r0, A, sigma_ey_eta, sigma_t_eta):
    '''Lateral Buckling Strength. CASE III: singly symmetric sections bent about their minor axis (symm axis).
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
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    Mc_eta = Cb*r0*A*(sigma_ey_eta*sigma_t_eta)**0.5
    return Mc_eta

def E_3_3_1_2_e5(Cb, Cs, r0, A, sigma_ex_eta, sigma_t_eta, j):
    '''Lateral Buckling Strength. CASE III: singly symmetric sections bent about their mayor axis (perp symm axis).
    Parameters
    ----------
        Cb: float,
            coeficiente de flexion.
        Cs: float,
            igual a +1 si se produce compresion en el alma, de lo contrario igual a -1.
        r0: float,
            radio polar de la seccion con respecto al centro de corte.
        A: float,
            full area.
        sigma_ex_eta: float,
            tension critica de pandeo con respecto al eje x (eje menor) dividida por eta.
        sigma_t_eta: float,
            tension critica de pandeo torsional dividida por eta.
        j: float,
            constante monosimetrica.
    Returns
    -------
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    Mc_eta = Cs*Cb*A*sigma_ex_eta*(j + Cs*(j**2 + r0**2*sigma_t_eta/sigma_ex_eta)**0.5)
    return Mc_eta

def E_3_3_1_2_e6(E0, K, L, r):
    '''Lateral Buckling Strength. Tension critica de pandeo.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        K*L: float,
            longitud efectiva.
        r: float,
            radio de giro.
    Returns
    -------
        sigma_eta: float,
            tension critica de pandeo dividida por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> round (E3_3_1_2_e6(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
        2220.56
    '''
    sigma_eta = pi**2*E0/(K*L/r)**2
    return sigma_eta

def E_3_3_1_2_e8(E0, Kt, Lt, r0, A, Cw, G0, J):
    '''Tension critica de pandeo torsional. s_t en Eq 3.3.1.2-6.
    Ver parametros de seccion en https://sectionproperties.readthedocs.io/en/latest/rst/post.html.

    Parameters
    ----------
        E0 : float,
            Modulo elasticidad.
        Kt : float,
            Factor de longitud efectiva a torsion.
        Lt : float,
            longitud del miembro a torsion.
        r0: float,
            radio polar.
        A : float,
            Area de la seccion.
        Cw : float,
            Constante torsional de warping de la seccion.
        G0 : float,
            Modulo de corte inicial.
        J : float,
            Constante de torsion de St. Venant.

    Returns
    -------
        s_t_eta : float
            Tension critica de pandeo torsional dividida por eta (para iterar).

    Tests
    -----
        >>> round ( E3_3_1_2_e8(E0 = 180510, Kt = 0.5, Lt = 1800, r0=58.7575,
        ... eta = 0.6225, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
        276.66
    '''

    t1 = 1/A/r0/r0
    t2_den = (Kt*Lt)**2
    t2 = G0*J + pi**2*E0*Cw/t2_den

    s_t_eta = t1*t2
    return s_t_eta

def E_3_3_1_2_e9(rx, ry, x0):
    '''Lateral Buckling Strength. Radio polar de la seccion.
    Parameters
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
        >>> round( E3_3_1_2_e9(40.272,18.2673,38.69), 2)
        58.76
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

def E_3_3_2_e1(E0, t, eta_shear, h):
    '''Strength for Shear Only. Resistencia nominal al corte.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        t: float,
            espesor de la seccion.
        eta_shear: float,
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


## 3.4 Compression Members
def E3_4_e1(Fn, Ae):
    ''' Design axial strength Ec 3.4-1.

    Parameters
    ----------
        Fn : float,
            El menor de los valores de tension para pandel flexiona, torsional o flexo-torsional.
        Ae : float,
            Area efectiva calculada a la tension Fn.
    Returns
    -------
        fiPn : float,
            Resistencia axial de diseño.
    Tests
    -----
        >>> round( E3_4_e1(1.5, 1.5), 4)
        1.9125
    '''
    fi_c = 0.85 # factor de resistencia a compresion
    fiPn = fi_c*Fn*Ae
    return fiPn

def E3_4_2_e1(E0, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    """Fn = s_t = TB en Eq 3.4.2-1. Tension critica de Torsional.
    
        Parameters
        ----------
        E0 : float,
            Modulo elasticidad.
        Kt : float,
            Factor de longitud efectiva de pandeo a torsion.
        Lt : float,
            longitud de pandeo a torsion.
        rx, ry : float,
            radio de giro del miembro | sqrt(I/A).
        eta : float,
            factor de reduccion plastica | Et(s)/E0.
        c_x : float,
            coordenada del centroide de la seccion.
        sc_x: float,
            coordenada del centro de corte.
        A : float,
            Area de la seccion.
        Cw : float,
            Constante torsional de warping de la seccion.
        G0 : float,
            Modulo de corte inicial.
        J : float,
            Constante de torsion de St. Venant.

        Returns
        -------
        Fn : float,
            Tension critica de pandeo torsional.

        Tests
        -----
            >>> round ( E3_4_2_e1(E0 = 180510, Kt = 0.5, Lt = 1800,
            ... rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59,
            ... sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
            276.66
    """
    Fn = E_3_3_1_2_e8(E0,Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J)
    return Fn

def E3_4_3_e1(E0, Kx, Lx, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''Fn de FTB en Eq 3.4.3-1. Tension critica de pandeo Flexo-torsional.

        Parameters
        ----------
        E0 : float,
            Modulo elasticidad.
        Kx : float,
            Factor de longitud efectiva de pandeo a flexión en -x-.
        Lx : float,
            Longitud de pandeo a flexión en -x-.
        Kt : float,
            Factor de longitud efectiva de pandeo a torsion.
        Lt : float,
            longitud de pandeo a torsion.
        rx, ry : float,
            radio de giro del miembro | sqrt(I/A).
        eta : float,
            factor de reduccion plastica | Et(s)/E0.
        c_x : float,
            coordenada del centroide de la seccion.
        sc_x: float,
            coordenada del centro de corte.
        A : float,
            Area de la seccion.
        Cw : float,
            Constante torsional de warping de la seccion.
        G0 : float,
            Modulo de corte inicial.
        J : float,
            Constante de torsion de St. Venant.

        Returns
        -------
        Fn : float,
            Tension critica de pandeo flexo-torsional.

        Tests
        -----
            >>> round ( E3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = 1800, Kt = 0.5,
            ... Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59,
            ... sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
            261.53
    '''
    
    x0 = -abs(c_x-sc_x) # distancia desde el centroide al centro de corte, negativo
    r0 = E_3_3_1_2_e9(rx= rx, ry=ry, x0=x0) # radio de giro polar
    beta = 1- (x0/r0)**2
    
    t1 = eta/2/beta
    s_ex = E_3_3_1_2_e6(E0=E0, Kx=Kx, Lx=Lx, rx=rx, eta=1.0)
    s_t = E_3_3_1_2_e8(E0=E0, Kt=Kt, Lt=Lt, rx=rx, ry=ry, eta=1.0, c_x=c_x, sc_x=sc_x, A=A, Cw=Cw, G0=G0, J=J)
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

    s_ex = E_3_3_1_2_e6(E0=E0, K=K, L=L, r=r, eta=eta)
    return s_ex

