#########################################################################################
#########################################################################################
#########################################################################################

import numpy as np
from math import pi, sin, cos


# DIMENSIONAL LIMITS AND CONSIDERATIONS
def sec2_1_1(condition, L, w, t, stiff_type = 'SL'):
    '''Flange Flat-Width-to-Thickness Considerations.
    Parameters
    ----------
        condition: string,
            determina si se aplica caso i, ii o iii de la seccion 2.1.1-1.
        L: float,
            longitud del miembro.
        w: float,
            ancho del elemento.
        t: float,
            espesor del elemento.
    Returns
    -------
        ratio_1: float,
            maximo ratio ancho-plano/espesor segun seccion 2.1.1-1.
        ratio_3: float,
            maximo ratio permitido ancho-diseno/ancho-real segun seccion 2.1.1-3.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    Tests
    -----
        >>> ratio_1_adm, w_eff, midC = sec2_1_1(condition='i', L=430, w=10, t=1)
        >>> print('ratio 1 adm: {:{fmt}} | w_eff: {:{fmt}} | ratio 1: {m[ratio w/t]:{fmt}} | ratio 3 adm: {m[ratio L/w]:{fmt}}'.format(ratio_1_adm, w_eff, m = midC, fmt = '.2f'))
        ratio 1 adm: 50.00 | w_eff: 10.00 | ratio 1: 10.00 | ratio 3 adm: 1.00
    '''

    ratio_1 = w/t
    ratio_3 = L/w

    if condition == 'i':
        if stiff_type == 'SL': ratio_adm_1 = 50
        if stiff_type == 'OTHER': ratio_adm_1 = 90

    if condition == 'ii': ratio_adm_1 = 400
    if condition == 'iii': ratio_adm_1 = 50

    ratio_3 = TABLE1(L,w)
    if ratio_3 > 1: ratio_3 = 1
    w_eff = w*ratio_3

    midC = {'ratio w/t': ratio_1, 'ratio L/w': ratio_3}

    return ratio_adm_1, w_eff, midC

def TABLE1(L, wf):
    '''TABLE 1. Short, Wide Flanges: Maximum Allowable Ratio of Effective Design Width to Actual Width
    Parameters
    ----------
        L: float,
            longitud del miembro.
        wf: float,
            ancho del ala proyectado luego del alma.

    Returns
    -------
        r: float,
            ratio permitido de ancho de diseno a ancho real.

    Tests
    -----
        >>> round(TABLE1(L=170, wf=10), 3)
        0.875
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
    r = np.interp(L/wf, table1[::-1,0], table1[::-1,1] )
    return r

def sec2_1_2(h, t, reinforced = 'NO', condition = 'i'):

    '''Maximum Web Depth-to-Thickness Ratio.
    Parameters
    ----------
        h: float,
            altura plana del alma medido sobre el plano de la misma.
        t: float,
            espesor del elemento.
        reinforced: string,
            determina si el alma esta reforzada o no para aplicar 1 o 2 de la seccion 2.1.2 segun corresponda.
        condition: string,
            determina si se aplica caso i o ii de la seccion 2.1.2-2.

    Returns
    -------
        ratio: float,
            ratio maximo altura/espesor del alma.

    Tests
    -----
        >>> ratio_adm, midC = sec2_1_2(h=300, t=5, reinforced='YES', condition='i') 
        >>> print('ratio_adm: {:{fmt}} | ratio: {m[ratio h/t]:{fmt}}'.format(ratio_adm, m = midC, fmt = '.2f'))
        ratio_adm: 260.00 | ratio: 60.00

    '''

    ratio = h/t

    if reinforced == 'NO': ratio_adm = 200
    if reinforced == 'YES':
        if condition == 'i': ratio_adm = 260
        if condition == 'ii': ratio_adm = 300

    midC = {'ratio h/t': ratio}

    return ratio_adm, midC


# EFFECTIVE WIDTH OF STIFFENED ELEMENTS 
def sec2_2_1(w, t, f, E, k = 4):
    '''Uniformly Compressed Stiffened Elements. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
        w: float,
            ancho plano del elemento (ver figura 3 - ASCE 8).
        t: float,
            espsesor del elemento.
        f: float
            tension sobre el elemento.
        E: float,
            modulo de elasticidad.
        k: float,
            coeficiente de pandeo en placas para el elemento en consideracion.
    Returns
    -------
        b_eff: float,
            ancho efectivo del elemento rigidizado bajo compresion uniforme.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    Test
    ----
        >>> b, midC = sec2_2_1(w= 50, t= 1, f= 20, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 50.00 | esbeltez: 0.26 | rho: 1.00
        >>> b, midC = sec2_2_1(w= 50, t= 1 , f= 200, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 44.22 | esbeltez: 0.83 | rho: 0.88
    '''
    esbeltez = E_2_2_1_e4(w=w, t=t ,f=f, E=E, k=k)
    rho = E_2_2_1_e3(esbeltez=esbeltez)
    
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

def E_2_2_1_e4(w, t, f, E, k):
    '''Ecuacion 2.2.1-4.
    Parameters
    ----------
        w: float,
            ancho plano del elemento (ver figura 3 - ASCE 8).
        t: float,
            espsesor del elemento.
        f: float
            tension sobre el elemento.
        E: float,
            modulo de elasticidad.
        k: float,
            coeficiente de pandeo en placas para el elemento en consideracion.

    Returns
    -------
        esbeltez: float,
            esbeltez del elemento considerado.

    Tests
    -----
        >>> round(E_2_2_1_e4(w= 50, t= 1, k=4, f= 200, E= 200e3), 2)
        0.83
    '''
    esbeltez = (1.052/(k**0.5))*(w/t)*(((f/E)**0.5))
    return esbeltez


def sec2_2_2(w, t, f1, f2, E, k):
    '''Effective Widths of Webs and Stiffened Elements with Stress Gradient. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
        w: float,
            altura del alma o ancho plano del elemento (ver figura 3 - ASCE 8).
        t: float,
            espsesor del alma o elemento.
        f1: float
            tension sobre el alma o elemento (ver figura 2 - ASCE 8).
        f2: float,
            tension sobre el alma o elemento.
        E: float,
            modulo de elasticidad.
        k: float,
            coeficiente de pandeo en placas para el elemento en consideracion.

    Returns
    -------
        b_eff_1, b_eff_2: float,
            anchos efectivos del alma o del elemento rigidizado bajo gradiente de compresion.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    Test
    ----
        >>>
    '''

    psi = f2/f1
    k = 4 + 2*(1-psi)**3 + 2*(1-psi)
    b_e = sec2_2_1(w=w, t=t, f=f1, E=E0, k=k)

    b_eff_1 = b_e/(3-psi)

    if psi <= -0.236: b_eff_2 = b_e/2
    else: b_eff_2 = b_e - b_eff_1

    midC = {'b1_eff': b_eff_1, 'b2_eff': b_eff_2, 'k': k, 'psi': psi}
    return b_e, midC


# EFFECTIVE WIDTH OF UNSTIFFENED ELEMENTS
def sec2_3_1(w, t, f, E, k = 0.5):
    '''Uniformly Compressed Unstiffened Elements. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
        w: float,
            ancho plano del elemento (ver figura 3 - ASCE 8).
        t: float,
            espsesor del elemento.
        f: float
            tension sobre el elemento (ver figura 3 - ASCE 8).
        E: float,
            modulo de elasticidad.
        k: float,
            coeficiente de pandeo en placas para el elemento en consideracion.  
    Returns
    -------
        b : float
            ancho efectivo del elemento no rigidizado bajo compresion uniforme
        midC: diccionario,
            calculos intermedios.
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
    b_eff, midC = sec2_2_1(w= w, t= t, f=f, E= E, k= k)
    return b_eff, midC


def sec2_3_2(w, t, f3, E, k = 0.5):
    '''Uniformly Compressed Unstiffened Elements. Load Capacity Determination or Deflection Determination.
    Parameters
    ----------
        w: float,
            ancho plano del elemento (ver figura 3 - ASCE 8).
        t: float,
            espsesor del elemento.
        f3: float
            tension sobre el elemento (ver figura 5 - ASCE 8).
        E: float,
            modulo de elasticidad.
        k: float,
            coeficiente de pandeo en placas para el elemento en consideracion.
    Returns
    -------
        b_eff: float,
            ancho efectivo del elemento no rigidizado bajo compresion uniforme.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    Test
    ----
        >>> b, midC = sec2_2_1(w= 50, t= 1, f= 20, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 50.00 | esbeltez: 0.26 | rho: 1.00
        >>> b, midC = sec2_2_1(w= 50, t= 1 , f= 200, E = 200e3)
        >>> print('b: {:{fmt}} | esbeltez: {m[esbeltez]:{fmt}} | rho: {m[rho]:{fmt}}'.format(b, m= midC, fmt = '.2f'))
        b: 44.22 | esbeltez: 0.83 | rho: 0.88
    '''
    b, midC = sec2_2_1(w=w, t=t, f=f3, E=E, k=0.5)
    return b, midC


# EFFECTIVE WIDTGHS OF ELEMENTS WITH EDGE STIFFENERS OR ONE INTERMEDIATE STIFFENERS
def sec2_4_1():
    raise 'Seccion 2.4.1 No Aplica.'


def sec2_4_2(E0, f, w, t = 0, d = 0, r = 0, theta = 90,  stiff = 'SL'):
    '''Uniformly Compressed Elements with Edge Stiffener. Load Capacity or Deflection Determiation.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        f: float,
            tension en el elemento.
        w: float,
            ancho del elemento sin tener en cuenta las curvaturas (ver figura 5 - ASCE 8).
        t: float
            espesor del elemento.
        d: float,
            ancho del rigidizador sin tener en cuenta la curvatura (ver figura 5 - ASCE 8).
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        r: float,
            radio de la curvatura del rigidizador.
        theta: float,
            angulo de inclinacion del rigidizador de labio simple.
        stiff: string,
            clase de rigidizador (labio simple u otro).
    Returns
    -------
        b: float,
            ancho efectivo del elemento.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    Tests
    -----
        # Ejemplo 17.1 - I-section
        >>> b, midC = sec2_4_2(E0=27000, f=10, w=1.178, t=0.135)
        >>> print('b: {:{fmt}} | Is: {m[Is]:{fmt}} | Ia: {m[Ia]:{fmt}} | As: {m[As]:{fmt}} | As_prima: {m[As_prima]:{fmt}} | ds: {m[ds]:{fmt}} | ds_prima: {m[ds_prima]:{fmt}} | k: {m[k]:{fmt}}'.format(b, m = midC, fmt = '.2f'))
        b: 1.18 | Is: 0.00 | Ia: 0.00 | As: 0.00 | As_prima: 0.00 | ds: 0.00 | ds_prima: 0.00 | k: 0.50

        # Ejemplo 18.1 - I-section
        >>> b, midC = sec2_4_2(E0=27000, f=23.52, w=1.855, t=0.135, d=0.498, r=3/16, theta=90, stiff='SL')
        >>> print('b: {:{fmt}} | Is: {m[Is]:{fmt}} | Ia: {m[Ia]:{fmt}} | As: {m[As]:{fmt}} | As_prima: {m[As_prima]:{fmt}} | ds: {m[ds]:{fmt}} | ds_prima: {m[ds_prima]:{fmt}} | k: {m[k]:{fmt}}'.format(b, m = midC, fmt = '.5f'))
        b: 1.85500 | Is: 0.00139 | Ia: 0.00000 | As: 0.06723 | As_prima: 0.06723 | ds: 0.49800 | ds_prima: 0.49800 | k: 0.50000

        # Ejemplo 16.1 - C-section with wide flanges - FALLA POR REDONDEO Ia_original=0.000842
        >>> b, midC = sec2_4_2(E0=27000, f=19.92, w=2.914, t=0.105, d=0.607, r=3/16, theta=90, stiff='SL')
        >>> print('b: {:{fmt2}} | Is: {m[Is]:{fmt5}} | Ia: {m[Ia]:{fmt5}} | As: {m[As]:{fmt5}} | As_prima: {m[As_prima]:{fmt5}} | ds: {m[ds]:{fmt2}} | ds_prima: {m[ds_prima]:{fmt2}} | k: {m[k]:{fmt2}}'.format(b, m = midC, fmt2 = '.2f', fmt5 = '.5f'))
        b: 2.91 | Is: 0.00196 | Ia: 0.00086 | As: 0.06374 | As_prima: 0.06374 | ds: 0.61 | ds_prima: 0.61 | k: 3.71

        # Ejemplo CASE III
        >>> b, midC = sec2_4_2(E0=27000, f=150.0, w=3.0, t=0.135, d=0.498, r=3/16, theta=90, stiff='SL')
        >>> print('b: {:{fmt}} | Is: {m[Is]:{fmt}} | Ia: {m[Ia]:{fmt}} | As: {m[As]:{fmt}} | As_prima: {m[As_prima]:{fmt}} | ds: {m[ds]:{fmt}} | ds_prima: {m[ds_prima]:{fmt}} | k: {m[k]:{fmt}}'.format(b, m = midC, fmt = '.5f'))
        b: 1.76703 | Is: 0.00139 | Ia: 0.05109 | As: 0.00183 | As_prima: 0.06723 | ds: 0.01354 | ds_prima: 0.49800 | k: 1.46826
    '''

    S = E_2_4_e1(E=E0, f=f)
    Is = E_2_4_e2(d=d, t=t, theta=theta)
    ds_prima, trash = sec2_3_1(w=d, t=t, f=f, E=E0)
    As_prima = E_2_4_e3(ds_prima=ds_prima, t=t)

    # a partir del radio de curvatura del rigidizador y del angulo calculo D
    D = d + (r + t)*(1 - cos(theta*pi/180))/sin(theta*pi/180)
    if D/w > 0.8:
        raise 'No se cumple la condicion D/w < 0.8'

    if w/t <= S/3:  # Ec 2.4.2-1
        b, midC = sec2_4_2_CASEI(Is=Is, As_prima=As_prima, w=w, ds_prima=ds_prima, t=t)
    elif w/t > S/3 and w/t < S:
        b, midC = sec2_4_2_CASEII(E0=E0, f=f, t=t, w=w, theta=theta, D=D, ds_prima=ds_prima, stiff=stiff, S=S, Is=Is, As_prima=As_prima)
    else:
        b, midC = sec2_4_2_CASEIII(E0=E0, f=f, t=t, w=w, theta=theta, D=D, ds_prima=ds_prima, stiff=stiff, S=S, Is=Is, As_prima=As_prima)
    
    return b, midC

def E_2_4_e1(E, f):
    '''Ecuacion 2.4-1
    Parameters
    ----------
        E: float,
            modulo de elasticidad.
        f: float,
            tension en el elemento.
    Returns
    -------
        S: float,
            parametro.
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_2_4_e1(E = 200e3, f = 200.0), 3)
        40.477
    '''
    S = 1.28*(E/f)**0.5
    return S

def E_2_4_e2(d, t, theta = 90):
    '''Ecuacion 2.4-2.
    Parameters
    ----------
        d: float,
            ancho total del rigidizador sin contar la curvatura.
        t: float,
            espesor del rigidizador.
        theta: float,
            angulo de inclinacion del rigidizador de labio simple.
    Returns
    -------
        Is: float,
            momento de inercia del rigidizador con respecto al eje paralelo del elemento al que rigidiza, medido en su centroide.
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_2_4_e2(d = 20.0, t = 3.0), 2)
        2000.0
    '''
    theta = theta*pi/180
    Is = (d**3*t*sin(theta))/12

    return Is

def E_2_4_e3(ds_prima, t):
    '''Ecuacion 2.4-3.
    Parameters
    ----------
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        t: float,
            espesor del rigidizador.
    Returns
    -------
        As_prima: float,
            area efectiva del rigidizador.
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_2_4_e3(10.0, 3.0), 2)
        30.0
    '''
    As_prima = ds_prima*t
    return As_prima

def sec2_4_2_CASEI(Is, As_prima, w, ds_prima, t, k = 0.5):
    '''Ecuacion 2.4.2-CASE I
    Parameters
    ----------
        w: float,
            ancho del elemento sin tener en cuenta las curvaturas (ver figura 5 - ASCE 8).
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        t: float,
            espesor del rigidizador.
    Returns
    -------
        b: float,
            ancho efectivo del elemento.
        midC: diccionario,
            calculos intermedios y valores de propiedades geometricas.
    Raises
    ------
        none
    '''
    Ia = 0
    b = w
    ds = ds_prima
    As = As_prima

    midC = {'Is': Is, 'Ia': Ia, 'As': As, 'As_prima': As_prima, 'ds': ds, 'ds_prima': ds_prima, 'k': k}

    return b, midC #devolver todas las propiedades efectivas + midC
 
def sec2_4_2_CASEII(E0, f, t, w, theta, D, ds_prima, stiff, S, Is, As_prima):
    '''Ecuacion 2.4.2-CASE II
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        f: float,
            tension en el elemento.
        t: float,
            espesor del elemento.
        w: float,
            ancho del elemento sin tener en cuenta las curvaturas (ver figura 5 - ASCE 8).
        theta: float,
            angulo de inclinacion del rigidizador de labio simple.
        D: float,
            ancho del rigidizador teniendo en cuenta la curvatura (ver figura 5 - ASCE 8).
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        stiff: float,
            clase de rigidizador (labio simple u otro).
        S: float;
            parametro.
        Is: float,
            momento de inercia del rigidizador con respecto al eje paralelo del elemento al que rigidiza, medido en su centroide.
        As_prima: float;
            area efectiva del rigidizador.
    Returns
    -------
        b: float,
            ancho efectivo del elemento.
        midC: diccionario,
            calculos intermedios.
    Raises
    ------
        none
    '''

    n = 0.5
    k_u = 0.43
    Ia = t**4*399*(w/t/S - (k_u/4)**0.5)**3 # Ec 2.4.2-6

    b, midC = E_2_4_2_CASES(E0=E0, f=f, t=t, w=w, theta=theta, D=D, ds_prima=ds_prima, stiff=stiff, Is=Is, As_prima=As_prima, n=n, Ia=Ia, k_u=k_u)

    return b, midC

def sec2_4_2_CASEIII(E0, f, t, w, theta, D, ds_prima, stiff, S, Is, As_prima):
    '''Ecuacion 2.4.2-CASE III
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        f: float,
            tension en el elemento.
        t: float,
            espesor del elemento.
        w: float,
            ancho del elemento sin tener en cuenta las curvaturas (ver figura 5 - ASCE 8).
        theta: float,
            angulo de inclinacion del rigidizador de labio simple.
        D: float,
            ancho del rigidizador teniendo en cuenta la curvatura (ver figura 5 - ASCE 8).
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        stiff: float,
            clase de rigidizador (labio simple u otro).
        S: float;
            parametro.
        Is: float,
            momento de inercia del rigidizador con respecto al eje paralelo del elemento al que rigidiza, medido en su centroide.
        As_prima: float;
            area efectiva del rigidizador.
    Returns
    -------
        b: float,
            ancho efectivo del elemento.
        midC: diccionario,
            calculos intermedios y valores de propiedades geometricas.
    Raises
    ------
        none
    '''

    n = 1/3
    k_u = 0.43
    Ia = t**4*(115*w/t/S + 5) # Ec 2.4.2-13

    b, midC = E_2_4_2_CASES(E0=E0, f=f, t=t, w=w, theta=theta, D=D, ds_prima=ds_prima, stiff=stiff, Is=Is, As_prima=As_prima, n=n, Ia=Ia, k_u=k_u)

    return b, midC
    
def E_2_4_2_CASES(E0, f, t, w, theta, D, ds_prima, stiff, Is, As_prima, n, Ia, k_u = 0.43):
    '''Funcion para evaluar CASE I o CASE II segun corresponda.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        f: float,
            tension en el elemento.
        t: float,
            espesor del elemento.
        w: float,
            ancho del elemento sin tener en cuenta las curvaturas (ver figura 5 - ASCE 8).
        theta: float,
            angulo de inclinacion del rigidizador de labio simple.
        D: float,
            ancho del rigidizador teniendo en cuenta la curvatura (ver figura 5 - ASCE 8).
        ds_prima: float,
            ancho efectivo del rigidizador calculado segun seccion 2.3.1 (ver figura 5 - ASCE 8).
        stiff: float,
            clase de rigidizador (labio simple u otro).
        S: float;
            parametro.
        Is: float,
            momento de inercia del rigidizador con respecto al eje paralelo del elemento al que rigidiza, medido en su centroide.
        As_prima: float;
            area efectiva del rigidizador.
    Returns
    -------
        b: float,
            ancho efectivo del elemento.
        midC: diccionario,
            calculos intermedios y valores de propiedades geometricas.
    Raises
    ------
        none
    '''

    C2 = Is/Ia  # Ec 2.4.2-7
    if C2 > 1: C2 = 1
    C1 = 2 - C2 # Ec 2.4.2-8

    if stiff == 'SL':

        if theta > 140 or theta < 40 or D/w > 0.8:
            raise 'Rigidizador de labio simple no cumple las condiciones para aplicar Ec 2.4.2-10 y Ec 2.4.2-11'
        
        else:
            k_a = 5.25 - 5.0*(D/w)  # Ec 2.4.2-10
            if k_a > 4: k_a = 4.0
            ds = C2*ds_prima
            As = ds*t

    else: 
        k_a = 4.0
        As = C2*As_prima
        ds = As/t

    k = C2**n*(k_a - k_u) + k_u # Ec 2.4.2-9
    b, trash = sec2_2_1(w=w, t=t, f=f, E=E0, k=k)
    
    midC = {'Is': Is, 'Ia': Ia, 'As': As, 'As_prima': As_prima, 'ds': ds, 'ds_prima': ds_prima, 'k': k}

    return b, midC #devolver todas las propiedades efectivas + midC

#########################################################################################
#########################################################################################
#########################################################################################

