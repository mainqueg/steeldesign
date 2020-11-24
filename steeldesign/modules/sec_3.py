from math import pi
import numpy as np

## 3.2 Tension Members
def sec3_2(An, FY):
    '''Design Tensile Strength. Eq 3.2-1.
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
        >>> fiTn, _ = sec3_2(An=1.551, FY=50)
        >>> round(fiTn, 2)
        65.92
    '''
    fi = 0.85
    Tn = An*FY

    midC = {'Tension_Tn': Tn, 'Tension_fi': fi}

    return Tn*fi, midC

## 3.3 Flexural Memebers

## 3.3.1 Strength for Bending Only
def s3_3_1_Nominal(member, LD = 'NO'):
    '''Design Nominal Section Strength. Section 3.3.1.1.
    Parameters
    ----------
        LD: string,
            determina si se consideran distorsiones locales para la resistencia a la flexion nominal (3.3.1.1-CASE III).
    Returns
    -------
        fiMn_Nominal: float,
            resistencia nominal de diseno a la flexion.
        [Nominal_fi, Nominal_Mn]: list of float,
            Nominal_fi: factor de diseno.
            Nominal_Mn: resistencia nominal de la seccion a flexion. 
    Raises
    ------
        none
    Tests
    -----
        En archivo
    '''
    steel = member.steel
    profile = member.profile
    elements = member.profile.elements

    FY = steel.FY
    # en realidad es el Sx de la seccion efectiva con tension Fyc o Fyt, pero por ahora va Sx full
    Se = profile.Sx

    for key in elements.keys(): # determino si el ala esta rigidizada o no
        element = elements[key]
        
        if element['name'] == 'flange':
            
            if element['type'] == 'stiffned_w_slps':
                comp_flange = 'STIFF'
            
            if element['type'] == 'stiffned_w_slps':
                comp_flange = 'UNSTIFF'

    if  LD == 'YES': # determino el procedimiento para 3.3.1.1
        procedure = 'LD'

    else:
        procedure = 'PI'

    fiMn_Nominal, midC = sec3_3_1_1(FY=FY, Se=Se, procedure=procedure, comp_flange=comp_flange)
    return fiMn_Nominal, midC

def s3_3_1_LB(member):
    '''Design Lateral Buckling Strength. Section 3.3.1.2.
    Parameters
    ----------
        none
    Returns
    -------
        fiMn_LB: float,
            resistencia de diseno al Lateral Buckling.
        [LB_fi, Nominal_Mn, Mc, eta]: list of float,
            LB_fi: factor de diseno.
            Lb_Mn: resistencia nominal al Lateral Buckling.
            Mc: momento critico.
            eta: factor plastico de reduccion.
    Raises
    ------
        none
    Tests
    -----
        En archivo
    '''
    fiMn_LB, midC = sec3_3_1_2(member)
    return fiMn_LB, midC


def sec3_3_1_1(FY, Se, procedure = 'PI', comp_flange = 'UNSTIFF'):
    '''Strength for Bending Only. Nominal Section Strength.
    Parameters
    ----------
        Fy: float,
            tension de fluencia segun Tabla A1 - ASCE 8.
        Se: float,
            modulo de seccion elastico efectivo, calculado con la fibra extrema en compresion con f=Fyc o f=Fyc, la que plastifique primero.
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
        >>> Mn, _ = sec3_3_1_1(FY=50, Se=1.422, procedure = 'PI', comp_flange = 'UNSTIFF')
        >>> round(Mn, 2)
        60.43
    '''
    if comp_flange == 'UNSTIFF':    # Unstiffened compresion flanges
        fi = 0.85
    elif comp_flange == 'STIFF':    # Stiffened or partially stiffened flanges
        fi = 0.90

    if procedure == 'PI':    # Procedimiento I - basado en fluencia
        Mn = E_3_3_1_1_e1(Se=Se, FY=FY)

    elif procedure == 'PII':    # Procedimiento II - basado en endurecimiento
        print('Seccion 3.3.1.1 - Procedimiento II No implementada.')
        raise NotImplementedError

    elif procedure == 'LD':     # Local Distorsion Considerations
        Mn, midC = LocalDistorsion()

    midC = {'Nominal_Mn': Mn, 'Nominal_fi': fi}
    fiMn = fi*Mn

    return fiMn, midC

def LocalDistorsion(self):
    '''Nominal Section Strength. Local Distorsion Consideration.
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
        >>> 
    '''
    raise NotImplementedError


def sec3_3_1_2(member):
    '''Strength for Bending Only. Design Lateral Buckling Strength.
    Parameters
    ----------
        none
    Returns
    -------
        fiMn: float,
            resistencia de diseno al Lateral Buckling.
        midC: diccionario,
            calculos intermedios y parametros.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    steel = member.steel
    profile = member.profile
    dpar = member.designParameters
    
    # habria que implementar la formula de calculo (1 es conservativo)
    Cb = 1

    if profile.type == 'I_builtup_cee' or profile.type == 'I_builtup_cee_w_lps':  # perfil I - aplica CASE I
        
        E0 = steel.E0
        d = profile.H
        Iyc = profile.Iy/2
        L = member.L
        # Mc_eta = Mc/eta
        Mc_eta = E_3_3_1_2_e2(E0=E0, Cb=Cb, d=d, Iyc=Iyc, L=L)
    
    elif profile.type == 'cee' or profile.type == 'c_w_lps':  # perfil C - aplica CASE III
        
        # implemento solo flexion alrededor del eje de simetria (tambien hay que ver como va disernir entre un caso y otro)
        # Mc_eta = Mc/eta
        Mc_eta = sec3_3_1_2_3_i(member=member, Cb=Cb)
        # Mc_eta = sec3_3_1_2_3_ii(member=member, Cb=Cb, Cs=Cs)

    Sf = profile.Sx
    # en realidad es el Sc de la seccion efectiva con tension Mc/Sf, pero por ahora va Sx full
    Sc = profile.Sx

    # construyo ecuacion: f - Mc/Sf = 0
    #                     f - (Mc_eta/Sf)*eta(f) = 0
    #                     f - FF*eta(f) = 0 (itero con eta_iter)
    FF = Mc_eta/Sf
    f = eta_iter(FF=FF, mat=steel)
    eta = f/FF

    Mn = E_3_3_1_2_e1(Sc=Sc, Mc=Mc_eta*eta, Sf=Sf)


    fi = 0.85
    fiMn = fi*Mn

    midC['LB_Mn'] = Mn
    midC['LB_fi'] = fi
    midC['Mc'] = Mc_eta*eta
    midC['eta'] = eta

    return fiMn, midC

def sec3_3_1_2_3_i(member, Cb):
    '''Lateral Buckling Strength. Singly symmetric sections bent about the axis of symmetry.
    Parameters
    ----------
        member: class,
            miembro a analizar segun seccion 3.3.1.2.
        Cb: float,
            coeficiente de flexion.
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
    steel = member.steel
    profile = member.profile
    dpar = member.designParameters

    # parametros para calculo r0
    rx = profile.rx
    ry = profile.ry
    c_x = profile.c_x
    sc_x = profile.sc_x
    x0 = -abs(c_x-sc_x)
    r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)

    # parametros para calculo sigmas
    E0 = steel.E0
    A = profile.A
    Ly = dpar.Ly
    Ky = dpar.Ky
    Lz = dpar.Lz
    Kz = dpar.Kz

    sigma_ey_eta = E_3_3_1_2_e6(E0=E0, K=Ky, L=Ly, r=ry)
    sigma_t_eta = E_3_3_1_2_e8(E0=E0, Kt=Kz, Lt=Lz, r0=r0, A=A, Cw=Cw, G0=G0, J=J)

    Mc_eta = E_3_3_1_2_e4(Cb=Cb, r0=r0, A=A, sigma_ey_eta=sigma_ey_eta, sigma_t_eta=sigma_t_eta)
    return Mc_eta

def sec3_3_1_2_3_ii(member, Cb, Cs):
    '''Lateral Buckling Strength. Singly symmetric sections bent about the axis perpendicular to the axis of symmetry.
    Parameters
    ----------
        member: class,
            miembro a analizar segun seccion 3.3.1.2.
        Cb: float,
            coeficiente de flexion.
        Cs: float,
            +1 si hay compresion en el lado del centro de corte, sino -1.
    Returns
    -------
        Mc_eta: float,
            resistencia nominal al LB de la seccion.
    Raises
    ------
        none
    Tests
    -----
        >>> 
    '''
    raise NotImplementedError

    steel = member.steel
    profile = member.profile
    dpar = member.designParameters

    # parametros para calculo r0
    rx = profile.rx
    ry = profile.ry
    c_x = profile.c_x
    sc_x = profile.sc_x
    x0 = -abs(c_x-sc_x)
    r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)

    # parametros para calculo sigmas
    E0 = steel.E0
    A = profile.A
    Lx = dpar.Lx
    Kx = dpar.Kx
    Lz = dpar.Lz
    Kz = dpar.Kz
    Cw = dpar.Cw
    J = dpar.J

    sigma_ex_eta = E_3_3_1_2_e6(E0=E0, K=Kx, L=Lx, r=rx)
    sigma_t_eta = E_3_3_1_2_e8(E0=E0, Kt=Kz, Lt=Lz, r0=r0, A=A, Cw=Cw, G0=G0, J=J)

    j = dpar.j
    Mc_eta = E_3_3_1_2_e5(Cb, Cs, r0, A, sigma_ex_eta, sigma_t_eta, j)
    return Mc_eta


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
        >>> round(E_3_3_1_1_e1(Se=2.239, FY=50), 2)
        111.95
    '''
    Mn = Se*FY
    return Mn


def E_3_3_1_2_e1(Sc, Mc, Sf):
    '''Lateral Buckling Strength. Strength of laterally unbraced segments.
    Parameters
    ----------
        Sc: float,
            modulo de seccion elastico efectivo calculado a una tension Mc/Sf.
        Mc: float,
            momento critico.
        Sf: float,
            modulo de seccion elastico.
    Returns
    -------
        Mn: float,
            resistencia nominal al Lateral Buckling.
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_3_3_1_2_e1(Sc=2.239, Mc=42.12*2.239, Sf=2.239), 2)
        94.31
    '''
    
    Mn = Sc*(Mc/Sf)
    return Mn

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
        Ejemplo 8.1 - Eq 3.3.1.2-2 dividido por eta
        >>> round(E_3_3_1_2_e2(E0=27000, Cb=1.75, d=6, Iyc=0.172, L=4*12), 2)
        208.88
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
        >>> round(E_3_3_1_2_e4(Cb=1.685, r0=2.581, A=1.284, sigma_ey_eta=47.14, sigma_t_eta=72.54), 2)
        326.54
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
        >>> round (E_3_3_1_2_e6(E0=27000, K=1.0, L=2.5*12, r=0.40), 2)
        47.37
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
        >>> round (E_3_3_1_2_e8(E0=27000, Kt=1.0, Lt=2.5*12, r0=2.581, A=1.284, Cw=1.819, G0=10500, J=0.0078), 2)
        72.54
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
        >>> round( E_3_3_1_2_e9(rx=40.272, ry=18.2673, x0=38.69), 2)
        58.76
    '''
    r0 = (rx**2 + ry**2 + x0**2)**0.5
    return r0


## 3.3.2 Strength for Shear Only
def E_3_3_2_e1(E0, t, h):
    '''Strength for Shear Only. Resistencia nominal al corte dividida por eta_shear.
    Parameters
    ----------
        E0: float,
            modulo de elasticidad inicial.
        t: float,
            espesor de la seccion.
        h: float,
            altura de la seccion.
    Returns
    -------
        Vn_eta: float,
            resistencia nominal al corte dividida por eta_shear (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_3_3_2_e1(E0=27e3, t=0.06, h=6.0), 2)
        4.7
    '''
    Vn_eta = 4.84*E0*t**3/h
    return Vn_eta


## 3.3.3 Strength for Combined Bending and Shear
def E_3_3_3_e1(fiMn, fiVn, Mu, Vu):
    '''Ecuacion de interaccion flexion-corte. Ecuacion 3.3.3-1.
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
        bool
    Tests
    -----
        none        
    '''
    comb = (Mu/fiMn)**2 + (Vu/fiVn)**2
    if comb <= 1: 
        return True
    else:
        return False

def E_3_3_3_e2(fiMn, fiVn, Mu, Vu):
    '''Ecuacion de interaccion flexion-corte. Ecuacion 3.3.3-2.
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
        bool
    Tests
    -----
        none        
    '''
    comb = (Mu/fiMn)*0.6 + (Vu/fiVn)
    if comb <= 1.3: 
        return True
    else:
        return False

## 3.3.4 Web Crippling Strength
def sec3_3_4():



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
    x0 = -abs(c_x-sc_x) # distancia desde el centroide al centro de corte, negativo
    r0 = E_3_3_1_2_e9(rx= rx, ry=ry, x0=x0) # radio de giro polar

    s_t_eta = E_3_3_1_2_e8(E0=E0, Kt= Kt, Lt=Lt, r0=r0, A=A, Cw=Cw, G0=G0, J=J)
    Fn = s_t_eta*eta
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

    beta = 1 - (x0/r0)**2
    t1 = eta/2/beta

    s_ex = E_3_3_1_2_e6(E0=E0, K=Kx, L=Lx, r=rx)

    s_t = E_3_3_1_2_e8(E0=E0, Kt=Kt, Lt=Lt, r0=r0, A=A, Cw=Cw, G0=G0, J=J)

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

    s_ex_eta = E_3_3_1_2_e6(E0=E0, K=K, L=L, r=r)
    s_ex = s_ex_eta*eta
    return s_ex


#####################################################################################
#####################################################################################
def eta_iter(FF, mat, s = 0):
    ''' A partir de la constante FF, se itera con un esquema de newton-rapson para 
    satisfacer la ecuacion f(s): s- FF*eta(s) = 0

    Parameters
    ----------
        FF : float
            Valor de la ecuacion para eta = 1
        mat : <class steel>
            Material del miembro
        s : float
            Tension incial de la iteracion. Por default s = 0.75*FY

    Tests
    -----
        incluido en test generales
    '''

    # tension inicial para iterar
    if not s:
        s = mat.FY*0.75
    ds = 0.1
    # error tolerado porcentual
    err = 1
    #inicializo el contador de iteraciones
    iterr = 0
    #inicializo eta
    eta = mat.eta(s)
    F = FF*eta

    # funcion para encontrar raices
    fn = s - F
    
    # newton-rapson para encontrar raiz de fn
    while abs((F-s)/s*100) > err and iterr < 100:
        # diferencial de eta
        eta_2 = mat.eta(s+ds)
        # diferencial de F
        F_2 = FF*eta_2
        # diferencial de fn
        fn_2 = s+ds - F_2
        # derivada  dfn/ds
        dfn = (fn_2 - fn)/ds
        # nuevo valor de s
        s = s - fn/dfn

        # actualizo valores, itero
        eta = mat.eta(s)
        F = FF*eta
        fn = s - F
        iterr += 1
        #print(iterr, s, F, 100-(F-s)/s*100)
    if abs((F-s)/s*100) > err:
        print('Se excedieron las 100 iteraciones')
    return F