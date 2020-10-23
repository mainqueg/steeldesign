from math import pi
import numpy as np

def E3_3_1_2_e6(E0, K, L, r, eta):
    '''s_ex en Eq 3.3.1.2-6. Tension critica de pandeo flexional

    # Parametros
    E0: Modulo elasticidad
    K: Factor de longitud efectiva
    L: longitud del miembro
    r: radio de giro del miembro | sqrt(I/A)
    eta: factor de reduccion plastica | Et(s)/E0

    # Tests
    >>> round (E3_3_1_2_e6(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
    2220.56
    '''

    den = (K*L/r)**2
    s_ex = pi**2*E0 / den * eta
    return s_ex

def E3_4_2_e1(E0,Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''Fn = s_t en Eq 3.4.2-1. Tension critica de Torsional
    
    
    # Parametros
    E0: Modulo elasticidad
    Kt: Factor de longitud efectiva a torsion
    Lt: longitud del miembro a torsion
    rx, ry: radio de giro del miembro | sqrt(I/A)
    eta: factor de reduccion plastica | Et(s)/E0
    c_x: coordenada del centroide de la seccion
    sc_x: coordenada del centro de corte
    A: Area de la seccion
    Cw: Constante torsional de warping de la seccion
    G0: Modulo de corte inicial
    J: Constante de torsion de St. Venant  

    # Tests
    >>> round ( E3_4_2_e1(E0 = 180510, Kt = 0.5, Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = 23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
    276.66
    '''
    Fn = E3_3_1_2_e8(E0,Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J)
    return Fn

def E3_4_3_e1(E0, Kx, Lx, Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''Fn = en Eq 3.4.3-1. Tension critica de pandeo Flexo-torsional


    # Parametros
    E0: Modulo elasticidad
    Kt: Factor de longitud efectiva a torsion
    Lt: longitud del miembro a torsion
    rx, ry: radio de giro del miembro | sqrt(I/A)
    eta: factor de reduccion plastica | Et(s)/E0
    c_x: coordenada del centroide de la seccion
    sc_x: coordenada del centro de corte
    A: Area de la seccion
    Cw: Constante torsional de warping de la seccion
    G0: Modulo de corte inicial
    J: Constante de torsion de St. Venant  

    # Tests
    >>> round ( E3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = 1800, Kt = 0.5, Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = 23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
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


def E3_4_3_e3(E0,K,L,r,eta):
    '''s_ex en Eq 3.4.3-3.

    # Parametros
    E0: Modulo elasticidad
    K: Factor de longitud efectiva
    L: longitud del miembro
    r: radio de giro del miembro | sqrt(I/A)
    eta: factor de reduccion plastica | Et(s)/E0

    # Tests
    >>> round (E3_4_3_e3(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
    2220.56
    '''

    s_ex = E3_3_1_2_e6(E0,K,L,r,eta)
    return s_ex

def E3_3_1_2_e8(E0,Kt,Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
    '''s_t en Eq 3.3.1.2-6.

    Ver parametros de seccion en https://sectionproperties.readthedocs.io/en/latest/rst/post.html

    # Parametros
    E0: Modulo elasticidad
    Kt: Factor de longitud efectiva a torsion
    Lt: longitud del miembro a torsion
    rx, ry: radio de giro del miembro | sqrt(I/A)
    eta: factor de reduccion plastica | Et(s)/E0
    c_x: coordenada del centroide de la seccion
    sc_x: coordenada del centro de corte
    A: Area de la seccion
    Cw: Constante torsional de warping de la seccion
    G0: Modulo de corte inicial
    J: Constante de torsion de St. Venant  

    # Tests
    >>> round ( E3_3_1_2_e8(E0 = 180510, Kt = 0.5, Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = 23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
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
    '''r0 en Eq 3.3.1.2-8. Radio de giro polar

    # Parametros\n
    rx, ry: radios de giro\n
    x0: distancia desde el centro de corte al centroide, en valor negativo\n

    # Tests\n
    >>> round( E3_3_1_2_e9(40.272,18.2673,38.69), 2)
    58.76
    '''
    r0 = (rx**2 + ry**2 + x0**2)**0.5
    return r0



