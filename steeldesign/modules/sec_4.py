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
        >>> 
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
        >>> 
    '''
    return L/6

def E_4_1_1_e3(g, Ts, m, q)
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
            factor de intensidad de carga.
    Raises
    ------
        none
    Returns
    -------
        s_max_limit: float,
            limite de espaciado maximo entre soldaduras.
    Tests
    -----
        >>> 
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
        >>> 
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
        q: float,
            factor de intensidad de carga.
    Raises
    ------
        none
    Returns
    -------
        Ts: float,
            resistencia de diseño de la conexion a la traccion.
    Tests
    -----
        >>> 
    '''
    return Pu*m/2/g


## 4.1.2 - Spacing of Connections in Compression Elements
def sec_4_1_2():
    '''
    Parameters
    ----------

    Raises
    ------
        none
    
    Returns
    -------

    Tests
    -----
        >>> 
    '''
    raise NotImplementedError


## Eq I1.2-1 - Slenderness

# Note: this equation aplies when the buckling modes involve relative deformations that 
# produce shear forces in the connectors between indivivual shapes
def E_I_1_2_e1(slender_0, a, r):
    '''Maximun permissible longitudinal spacing of welds or other connectors joining two channels.
    Parameters
    ----------

    Raises
    ------
        none
    
    Returns
    -------

    Tests
    -----
        >>> 
    '''
    return ( slender_0**2 + (a/r)**2 )**0.5