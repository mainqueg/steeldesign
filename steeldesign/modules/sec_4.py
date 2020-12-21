import numpy as np
from math import pi

## 4.1 - Built-up Sections
## 4.1.1 - I-Sections Composed of Two Channels
def E_4_1_1_e1(L, r_cy, r_I):
    '''Maximun permissible longitudinal spacing of welds or other connectors joining two channels. For compression members.
    Parameters
    ----------
        L: float,
            longitud en compresion sin soporte lateral.
        r_cy: float,
            radio de giro de un perfil C.
        r_I: float,
            radio de giro de la seccion con respecto al eje perpendicular a la direccion de pandeo.
    Raises
    ------
        none
    Returns
    -------
        s_max: float,
            espaciado maximo entre soldaduras.
    Tests
    -----
        >>> round(E_4_1_1_e1(L=6*12, r_cy=0.4, r_I=0.6), 2)
        24.0
    '''
    return L*r_cy/2/r_I 

def E_4_1_1_e2(L):
    '''Maximun permissible longitudinal spacing of welds or other connectors joining two channels. For flexural members.
    Parameters
    ----------
        L: float,
            longitud en compresion sin soporte lateral.
    Raises
    ------
        none
    Returns
    -------
        s_max: float,
            espaciado maximo entre soldaduras.
    Tests
    -----
        >>> round(E_4_1_1_e2(L=6*12), 2)
        12.0
    '''
    return L/6

def E_4_1_1_e3(g, Ts, m, q):
    '''Limit for the maximun spacing of welds or connections for flexural members.
    Parameters
    ----------
        g: float,
            distancia vertical entre las lineas de conexiones mas cercanas a los topes superior e inferior.
        Ts: float,
            resistencia de diseño de la conexion a la traccion (Seccion 5).
        m: float,
            distancia entre el centro de corte de un perfil C al plano medio de su alma.
        q: float,
            carga de diseño sobre la viga para determinar s_max.
    Raises
    ------
        none
    Returns
    -------
        s_max_limit: float,
            limite de espaciado maximo entre soldaduras.
    Tests
    -----
        >>> round(E_4_1_1_e3(g=7.0, Ts=0.18, m=0.629, q=1.0), 2)
        4.01
    '''
    return 2*g*Ts/m/q

def E_4_1_1_e4(B, t, Ix, d, D = 0):
    '''Calculo de m.
    Parameters
    ----------
        B: float,
            ancho del ala.
        t: float,
            espesor del perfil.
        Ix: float,
            momento de inercia del perfil C.
        d: float,
            altura total del perfil.
        D: float,
            altura del labio rigidizador. Sino se especifica vale 0 por default.
    Raises
    ------
        none
    Returns
    -------
        m: float,
            distancia entre el centro de corte de un perfil C al plano medio de su alma.
    Tests
    -----
        >>> round(E_4_1_1_e4(B=1.5, t=0.135, Ix=7.8329, d=7.0, D = 0), 3)
        0.417
    '''
    if D == 0: alpha = 0
    else: alpha = 1
    b_hat = B - (t/2 + alpha*t/2)
    d_hat = d - t
    Dhat = alpha*(D - t/2)

    f1 = b_hat*t/12/Ix
    f2 = 6*Dhat*d_hat**2 + 3*b_hat*d_hat**2 - 8*Dhat**3
    return f1*f2

def E_4_1_1_e5(Pu, m, g):
    '''Required strength of the welds or connections closest to the load or reaction Pu.
    Parameters
    ----------
        Pu: float,
            carga concentrada o reaccion.
        m: float,
            distancia entre el centro de corte de un perfil C al plano medio de su alma.
        g: float,
            distancia vertical entre las lineas de conexiones mas cercanas a los topes superior e inferior.
    Raises
    ------
        none
    Returns
    -------
        Tr: float,
            resistencia requerida de la conexion a la traccion.
    Tests
    -----
        >>> round(E_4_1_1_e5(Pu=4.05, m=0.629, g=7.0), 2)
        0.18
    '''
    return Pu*m/2/g


## 4.1.2 - Spacing of Connections in Compression Elements
def sec_4_1_2(t_N, Et, f_s, w):
    '''
    Parameters
    ----------
        t_N: float,
            espesor del cover plate or sheet.
        Et: float,
            modulo de elasticidad tangente en compresion.
        f_s: float,
            tension de servicio sobre el cover plate or sheet.
        w: float,
            ancho plano del menor elemento no rigidizado en compresion tributario a la conexion.
    Raises
    ------
        none
    Returns
    -------
        s_maxs: string,
            contiene los s_max segun condiciones (2) y (3).
    Tests
    -----
        >>> 
    '''
    raise NotImplementedError

    s_maxs = np.zeros(2)
    s_maxs[0] = 1.11*t_N*(Et/f_s)**0.5
    s_maxs[1] = 3*w

    return s_maxs


## Eq I1.2-1 - Slenderness - Compression Members Composed of Two Sections in Contact

# Note: this equation aplies when the buckling modes involve relative deformations that 
# produce shear forces in the connectors between indivivual shapes
def E_I_1_2_e1(K, L, r, a, ri):
    '''Maximun permissible longitudinal spacing of welds or other connectors joining two channels.
    Parameters
    ----------
        K,L: float,
            longitud efectiva.
        r: float,
            radio de giro.
        a: float,
            espaciado entre soldaduras o bulones.
        ri: float,
            minimo radio de giro de la seccion individual del built-up.
    Raises
    ------
        none
    Returns
    -------
        slend_modif: float
            esbeltez modificada.
    Tests
    -----
        >>> round(E_I_1_2_e1(K=1.0, L=6*12, r=0.6, a=18.0, ri=0.4), 2)
        128.16
    '''
    slend = (K*L/r)
    return ( slend**2 + (a/ri)**2 )**0.5

#####################################################################################
#####################################################################################