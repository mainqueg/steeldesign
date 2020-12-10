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
def sec3_3_1_1(FY, Se, procedure = 'PI', comp_flange = 'UNSTIFF', localDistorsion= False):
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
        Example 8.1 - I-section w/unstiffened flanges 
        >>> fiMn, _ = sec3_3_1_1(FY=50, Se=1.422, procedure = 'PI', comp_flange = 'UNSTIFF')
        >>> round(fiMn, 2)
        60.43
    '''
    midC={}
    if comp_flange == 'UNSTIFF':    # Unstiffened compresion flanges
        fi = 0.85
    elif comp_flange == 'STIFF':    # Stiffened or partially stiffened flanges
        fi = 0.90

    if procedure == 'PI':    # Procedimiento I - basado en fluencia
        Mn = E_3_3_1_1_e1(Se=Se, FY=FY)
    elif procedure == 'PII':    # Procedimiento II - basado en endurecimiento 
        print('Seccion 3.3.1.1 - Procedimiento II No implementada.')
        raise NotImplementedError

    if localDistorsion:     # Local Distorsion Considerations
        Mld, midC = LocalDistorsion()
        midC['Mld']= Mld

    midC.update({'Mn_no': Mn, 'fi_no': fi})
    fiMn = fi*Mn

    return fiMn, midC

def LocalDistorsion():
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


def sec3_3_1_2_eta(prof_type, E0, d, Iyc, L, rx, ry, c_x, sc_x, A, Lx, Kx, Ly, Ky, Lz, Kz, Cw, G0, J, j, Cb):
    '''Strength for Bending Only. Design Lateral Buckling Strength.
    Parameters
    ----------
        prof_type: string,
            seccion del miembro.
        Cb: float,
            coeficiente de flexion.
        E0: float,
            modulo de elasticidad inicial.
        d: float,
            altura total de la seccion.
        Iyc: float,
            momento de inercia de la porcion de la seccion en compresion con respecto al eje vertical.
        L: float,
            longitud del miembro sin soporte.
        rx, ry: float,
            radios de giro.
        c_x: float
            coordenada x del centroide de la seccion.
        sc_x,: float
            coordenada x del centro de corte.
        A: float,
            area de la seccion.
        Lx, Kx: float,
            longitud efectiva para miembros en compresion sometidos a flexion en x.
        Ly, Ky: float,
            longitud efectiva para miembros en compresion sometidos a flexion en y.
        Lz, Kz: float,
            longitud efectiva para miembros en compresion sometidos a torsion.
        Cw: float,
            constante de warping
        G0: float,
            modulo de elasticida de corte inicial.
        J: float,
            constante de St Venant.
        j: float
            mitad de la constante monociclica a compresion en eje -y- (beta22-)
    Returns
    -------
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        Example 8.1 - I-section w/unstiffened flanges
        >>> round(sec3_3_1_2_eta(prof_type='I_builtup_cee', E0=27000, d=6.0, Iyc=0.172, L=4*12, rx=2.224, ry=0.564, c_x=0, sc_x=0, A=1.083, Lx=4*12, Kx=1.0, Ly=4*12, Ky=1.0, Lz=4*12, Kz=1.0, Cw=3.00, G0=10384.61, J=0.0037, beta=0.0, Cb=1.75), 2)
        208.88

        Example 9.1 - C-section w/lateral buckling consideration
        En realidad el valor de ref es 326.54 pero sigma_ey en ref es 47.14 y en calculos es 47.37 (leve error en ref)
        >>> round(sec3_3_1_2_eta(prof_type='cee', Cb=1.685, E0=27000, d=7.0, Iyc=0.204/2, L=2.5*12, rx=2.47, ry=0.40, c_x=0.217, sc_x=-0.417, A=1.284, Lx=2.5*12, Kx=1.0, Ly=2.5*12, Ky=1.0, Lz=2.5*12, Kz=1.0, Cw=1.819, G0=10500, J=0.0078, beta=0), 2)
        327.35
    '''    
    if prof_type in ['I_builtup_cee', 'I_builtup_cee_w_lps']:  # perfil I - aplica CASE I
        Mc_eta = E_3_3_1_2_e2(E0=E0, Cb=Cb, d=d, Iyc=Iyc, L=L)
    elif prof_type in ['cee', 'c_w_lps']:  # perfil C - aplica CASE III
        # implemento solo flexion alrededor del eje de simetria (tambien hay que ver como va disernir entre un caso y otro)
        # Mc_eta = Mc/eta
        Mc_eta = sec3_3_1_2_3_i(Cb=Cb, rx=rx, ry=ry, c_x=c_x, sc_x=sc_x, E0=E0, A=A, Ly=Ly, Ky=Ky, Lz=Lz, Kz=Kz, Cw=Cw, G0=G0, J=J)
        # Mc_eta = sec3_3_1_2_3_ii(Cb=Cb, rx=rx, ry=ry, c_x=c_x, sc_x=sc_x, E0=E0, A=A, Lx=Lx, Kx=Kx, Lz=Lz, Kz=Kz, Cw=Cw, G0=G0, J=J, j=j)
    else:
        print('Seccion del tipo', prof_type,'no implementada en analisis 3.3.1.2.')
        raise NotImplementedError
        
    return Mc_eta

def sec3_3_1_2_3_i(Cb, rx, ry, c_x, sc_x, E0, A, Ly, Ky, Lz, Kz, Cw, G0, J):
    '''Lateral Buckling Strength. Singly symmetric sections bent about the axis of symmetry.
    Parameters
    ----------
        Cb: float,
            coeficiente de flexion.
        rx, ry: float,
            radios de giro.
        c_x: float
            coordenada x del centroide de la seccion.
        sc_x,: float
            coordenada x del centro de corte.
        E0: float,
            modulo de elasticidad inicial.
        A: float,
            area de la seccion.
        Ly, Ky: float,
            longitud efectiva para miembros en compresion sometidos a flexion en y.
        Lz, Kz: float,
            longitud efectiva para miembros en compresion sometidos a torsion.
        Cw: float,
            constante de warping
        G0: float,
            modulo de elasticida de corte inicial.
        J: float,
            constante de St Venant.
    Returns
    -------
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        Example 9.1 - C-section w/lateral buckling consideration
        En realidad el valor de ref es 326.54 pero sigma_ey en ref es 47.14 y en calculos es 47.37 (leve error en ref)
        >>> round(sec3_3_1_2_3_i(Cb=1.685, rx=2.47, ry=0.40, c_x=0.217, sc_x=-0.417, E0=27000, A=1.284, Ly=2.5*12, Ky=1.0, Lz=2.5*12, Kz=1.0, Cw=1.819, G0=10500, J=0.0078), 2)
        327.35
    '''
    # parametros para calculo r0
    x0 = -abs(c_x-sc_x)
    r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)

    sigma_ey_eta = E_3_3_1_2_e6(E0=E0, K=Ky, L=Ly, r=ry)
    sigma_t_eta = E_3_3_1_2_e8(E0=E0, Kt=Kz, Lt=Lz, r0=r0, A=A, Cw=Cw, G0=G0, J=J)

    Mc_eta = E_3_3_1_2_e4(Cb=Cb, r0=r0, A=A, sigma_ey_eta=sigma_ey_eta, sigma_t_eta=sigma_t_eta)
    return Mc_eta

def sec3_3_1_2_3_ii(Cb, Cs, rx, ry, c_x, sc_x, E0, A, Lx, Kx, Lz, Kz, Cw, G0, J, j):
    '''Lateral Buckling Strength. Singly symmetric sections bent about the axis perpendicular to the axis of symmetry.
    Parameters
    ----------
        Cb: float,
            coeficiente de flexion.
        Cs: float,
            +1 si hay compresion en el lado del centro de corte, sino -1.
        rx, ry: float,
            radios de giro.
        c_x: float
            coordenada x del centroide de la seccion.
        sc_x,: float
            coordenada x del centro de corte.
        E0: float,
            modulo de elasticidad inicial.
        A: float,
            area de la seccion.
        Lx, Kx: float,
            longitud efectiva para miembros en compresion sometidos a flexion en x.
        Lz, Kz: float,
            longitud efectiva para miembros en compresion sometidos a torsion.
        Cw: float,
            constante de warping
        G0: float,
            modulo de elasticida de corte inicial.
        J: float,
            constante de St Venant.
        j: float,
            mitad de la constante monociclica a compresion en eje -y- (beta22-)
    Returns
    -------
        Mc_eta: float,
            resistencia nominal al LB de la seccion.
    Raises
    ------
        none
    Tests
    -----
        # >>> round(sec3_3_1_2_3_ii(Cb=1.0, Cs=1.0, rx=3.121, ry=1.073, c_x=0.820, sc_x=-1.371, E0=27000, A=1.551, Lx=16*12, Kx=1.0, Lz=16*12, Kz=1.0, Cw=23.468, G0=10500, J=0.005699, j=4.567), 1)
        # 1022.0
    '''
    '''
    # parametros para calculo r0
    x0 = -abs(c_x-sc_x)
    r0 = E_3_3_1_2_e9(rx=rx, ry=ry, x0=x0)

    sigma_ex_eta = E_3_3_1_2_e6(E0=E0, K=Kx, L=Lx, r=rx)
    sigma_t_eta = E_3_3_1_2_e8(E0=E0, Kt=Kz, Lt=Lz, r0=r0, A=A, Cw=Cw, G0=G0, J=J)

    Mc_eta = E_3_3_1_2_e5(Cb=Cb, Cs=Cs, r0=r0, A=A, sigma_ex_eta=sigma_ex_eta, sigma_t_eta=sigma_t_eta, j=j)
    return Mc_eta'''

    raise NotImplementedError


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
        fiMn: float,
            resistencia de diseño nominal al Lateral Buckling.
        [LB_fi, LB_Mn, Mc, eta]: list of float,
            LB_fi: factor de diseno.
            Lb_Mn: resistencia nominal al Lateral Buckling.
    Raises
    ------
        none
    Tests
    -----
        >>> fiMn, _ = E_3_3_1_2_e1(Sc=2.239, Mc=42.12*2.239, Sf=2.239)
        >>> round(fiMn, 2)
        80.16
    '''
    fi = 0.85
    Mn = Sc*(Mc/Sf)

    fiMn = fi*Mn
    midC = {'Mn_LB': Mn, 'fi_LB': fi}
    return fiMn, midC

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
            longitud del miembro sin soporte lateral.
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
            mitad de la constante monociclica a compresion en eje -y- (beta22-)
    Returns
    -------
        Mc_eta: float,
            momento critico dividido por eta (para iterar).
    Raises
    ------
        none
    Tests
    -----
        >>> round(E_3_3_1_2_e5(Cb=1.0, Cs=1.0, r0=3.961, A=1.551, sigma_ex_eta=70.41, sigma_t_eta=9.43, j=4.567), 1)
        1022.0
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
        x0 : float
            distancia entre el centro de corte y centroide
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
        Example 9.1 - C-profile with LB consideration 
        >>> round(E_3_3_2_e1(E0=27e3, t=0.135, h=6.354), 2)
        50.6
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
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.
    Tests
    -----
        Example 9.1 - C-profile with LB consideration 
        >>> round(E_3_3_3_e1(fiMn=80.16, fiVn=27.88, Mu=44.16, Vu=2.21), 2)
        0.31
    '''
    comb = (Mu/fiMn)**2 + (Vu/fiVn)**2
    limit = 1.0
    ratio = comb/limit
    return ratio

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
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.
    Tests
    -----
        >>> round(E_3_3_3_e1(fiMn=80.16, fiVn=27.88, Mu=44.16, Vu=2.21), 2)
        0.31
    '''
    comb = (Mu/fiMn)*0.6 + (Vu/fiVn)
    limit = 1.3
    ratio = comb/limit
    return ratio

 
## 3.3.4 Web Crippling Strength
def sec3_3_4(self):
    '''Web Crippling Strength.
    Parameters
    ----------
        
    Returns
    -------
        
    Raises
    ------
        none
    Tests
    -----
        none
    '''
    steel = self.member.steel
    profile = self.member.profile
    dpar = self.member.dP

    # Parametros

    fi = 0.70

    FY = steel.FY
    h = profile.H - 2*profile.r_out
    t = profile.t

    ct = Ct(units='US')
    k = FY/33/ct
    m = E_3_3_4_e22(t= t, units='US')

    N = dpar.N
    R = profile.r_out - t
    theta = dpar.N_theta

    # Calculo de coeficientes
    C1 = E_3_3_4_e10(FY=FY, Ct=Ct, k=k)
    C2 = E_3_3_4_e11(R=R, t=t)
    C3 = E_3_3_4_e12(FY=FY, Ct=Ct, k=k)
    C4 = E_3_3_4_e13(R=R, t=t)
    C5 = E_3_3_4_e14(k=k)
    C6 = E_3_3_4_e15(h=h, t=t)
    C7 = E_3_3_4_e17(h=h, t=t, k=k)
    C8 = E_3_3_4_e19(h=h, t=t, k=k)
    C_theta = E_3_3_4_e20(theta=theta)

    ## Shapes Having Single Webs
        # Stiffened or Partially Stiffened Flenges
            # End Reaction
    E_3_3_4_e1(t, C3, C4, Ctheta, h, N, Ct)
            # Interior Reaction
    E_3_3_4_e4(t, C1, C2, Ctheta, h, N, Ct)

       # Unstiffened Flanges
            # End Reaction
    E_3_3_4_e2(t, C3, C4, Ctheta, h, N, Ct)
            # Interior Reaction
    E_3_3_4_e4(t, C1, C2, Ctheta, h, N, Ct)

    ## I-sections or Similar Sections
        # Stiffened, Partially Stiffened and Unstiffened Flanges
            # End Reaction
    E_3_3_4_e3(N, t, FY, C6)
            # Interior Reaction
    E_3_3_4_e5(N, t, FY, C5, m)


def E_3_3_4_e1(t, C3, C4, Ctheta, h, N, Ct):
    '''Ecuacion 3.3.4-1.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e1(t=0.135, C3=1.258, C4=0.942, Ctheta=1.0, h=6.354, N=3.0, Ct=1.0), 2)
        7.98
    '''
    f1 = t**2*C3*C4*Ctheta
    f2 = 331 - 0.61*h/t
    f3 = 1 + 0.01*N/t

    return f1*f2*f3*Ct

def E_3_3_4_e2(t, C3, C4, Ctheta, h, N, Ct):
    '''Ecuacion 3.3.4-2.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e2(t=0.135, C3=1.258, C4=0.942, Ctheta=1.0, h=6.354, N=3.0, Ct=1.0), 2)
        5.38
    '''
    f1 = t**2*C3*C4*Ctheta
    f2 = 217 - 0.28*h/t
    f3 = 1 + 0.01*N/t

    return f1*f2*f3*Ct

def E_3_3_4_e3(N, t, FY, C6):
    '''Ecuacion 3.3.4-3.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e3(N=3.0, t=0.135, FY=50, C6=1+6.354/0.135/750), 2)
        16.06
    '''
    f1 = 0.71 + 0.015*N/t
    f2 = t**2*FY*C6
    f3 = 10 + 1.25*(N/t)**0.5

    return f1*f2*f3

def E_3_3_4_e4(t, C1, C2, Ctheta, h, N, Ct):
    '''Ecuacion 3.3.4-4.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e4(t=0.135, C1=1.343, C2=0.977, Ctheta=1.0, h=6.354, N=6.0, Ct=1.0), 2)
        15.78
    '''
    f1 = t**2*C1*C2*Ctheta
    f2 = 538 - 0.74*h/t
    f3 = 1 + 0.007*N/t

    return f1*f2*f3*Ct

def E_3_3_4_e5(N, t, FY, C5, m):
    '''Ecuacion 3.3.4-5.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e5(N=3.0, t=0.135, FY=50, C5=0.96, m=0.135/0.075), 2)
        28.91
    '''
    f1 = 0.75 + 0.011*N/t
    f2 = t**2*FY*C5
    f3 = 0.88 + 0.12*m
    f4 = 15 + 3.25*(N/t)**0.5

    return f1*f2*f3*f4

def E_3_3_4_e6(t, C3, C4, Ctheta, h, N, Ct):
    '''Ecuacion 3.3.4-6.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e6(t=0.135, C3=1.34, C4=0.5, Ctheta=1.0, h=6.354, N=3.0, Ct=1.0), 2)
        3.24
    '''
    f1 = t**2*C3*C4*Ctheta
    f2 = 244 - 0.57*h/t
    f3 = 1 + 0.01*N/t

    return f1*f2*f3*Ct

def E_3_3_4_e7(t, C8, FY, N, m):
    '''Ecuacion 3.3.4-7.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e7(t=0.135, C8=0.91, FY=50.0, N=3.0, m=0.135/0.075), 2)
        15.79
    '''
    f1 = t**2*FY*C8
    f2 = 0.64 + 0.31*m
    f3 = 10 + 1.25*(N/t)**0.5

    return f1*f2*f3

def E_3_3_4_e8(t, C1, C2, Ctheta, h, N, Ct):
    '''Ecuacion 3.3.4-8.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e8(t=0.135, C1=1.343, C2=0.977, Ctheta=1.0, h=6.354, N=3.0, Ct=1.0), 2)
        16.35
    '''
    f1 = t**2*C1*C2*Ctheta
    f2 = 771 - 2.26*h/t
    f3 = 1 + 0.0013*N/t

    return f1*f2*f3*Ct

def E_3_3_4_e9(t, C7, FY, N, m):
    '''Ecuacion 3.3.4-9.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e9(t=0.135, C7=0.98, FY=50.0, N=3.0, m=0.135/0.075), 2)
        14.89
    '''
    f1 = t**2*FY*C7
    f2 = 0.82 - 0.15*m
    f3 = 15 + 3.25*(N/t)**0.5

    return f1*f2*f3

def Ct(units = 'SI'):
    '''Ct.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> Ct(units='US')
        1.0
    '''
    if units == 'SI':
        return 6.9
    if units == 'US':
        return 1.0

def E_3_3_4_e10(FY, Ct, k):
    '''C1. Ecuacion 3.3.4-10.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e10(FY=50, Ct=1.0, k=1.515), 3)
        1.343
    '''
    limit = FY/91.5/Ct
    if limit <= 1:
        return (1.22 - 0.22*k)*k
    else:
        return 1.69

def E_3_3_4_e11(R, t):
    '''C2. Ecuacion 3.3.4-11.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e11(R=3.0/16.0, t=0.135), 3)
        0.977
    '''
    C2 = (1.06 - 0.06*R/t)
    if C2 > 1: C2 = 1.0
    return C2

def E_3_3_4_e12(FY, Ct, k):
    '''C3. Ecuacion 3.3.4-12.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e12(FY=50, Ct=1.0, k=1.515), 3)
        1.258
    '''
    limit = FY/66.5/Ct
    if limit <= 1:
        return (1.33 - 0.33*k)*k
    else:
        return 1.34

def E_3_3_4_e13(R, t):
    '''C4. Ecuacion 3.3.4-13.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e13(R=3.0/16.0, t=0.135), 3)
        0.942
    '''
    C4 = (1.15 - 0.15*R/t)
    if C4 < 0.5: C4 = 0.5
    return C4

def E_3_3_4_e14(k):
    '''C5. Ecuacion 3.3.4-14.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e14(k=1.0), 2)
        0.96
    '''
    C5 = (1.49 - 0.53*k)
    if C5 < 0.6: C5 = 0.6
    return C5

def E_3_3_4_e15(h, t):
    '''C6. Ecuacion 3.3.4-15.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e15(h=6.354, t=0.135), 2)
        1.06
    '''
    if h/t <= 150:
        C6 = 1.0 + h/t/750
    else: C6 = 1.20
    return C6

def E_3_3_4_e17(h, t, k):
    '''C7. Ecuacion 3.3.4-17.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e17(h=6.354, t=0.08, k=1.0), 2)
        0.98
    '''
    if h/t <= 66.5:
        C7 = 1/k
    else: C7 = (1.10 - h/t/660)/k
    return C7

def E_3_3_4_e19(h, t, k):
    '''C8. Ecuacion 3.3.4-19.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e19(h=6.354, t=0.135, k=1.0), 2)
        0.91
    '''
    return (0.98 - h/t/665)/k

def E_3_3_4_e20(theta):
    '''C_theta. Ecuacion 3.3.4-20.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e20(theta=90), 2)
        1.0
    '''
    return 0.7 + 0.3*(theta/90)**2

def E_3_3_4_e21(FY, Ct):
    '''k. Ecuacion 3.3.4-21.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e21(FY=50, Ct=1.0), 3)
        1.515
    '''
    return FY/33/Ct

def E_3_3_4_e22(t, units='SI'):
    '''m. Ecuacion 3.3.4-22.
    Parameters
    ----------
        
    Returns
    -------
        
    Tests
    -----
        >>> round(E_3_3_4_e22(t=0.135), 2)
        0.07
    '''
    if units == 'SI':
        return t/1.91
    if units == 'US':
        return t/0.075


## 3.3.5 Strength for Combined Bending and Web Crippling
def E_3_3_5_e1(Pu, fiPn, Mu, fiMn):
    '''Ecuacion de interaccion flexion-corte. Ecuacion 3.3.3-1.
    Parameters
    ----------
        fiMn: float,
            resistencia de diseno a la flexion, cuando actua solo la flexion.
        fiPn: float,
            resistencia de diseno a una carga concentrada o reaccion, en ausencia de flexion segun seccion 3.3.4.
        Mu: float,
            resistencia requerida a la flexion. 
        Pu: float,
            resistencia requerida a una carga concentrada o reaccion, en ausencia de flexion.
    Returns
    -------
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.
    Tests
    -----
        Example 9.1 - C-profile with LB consideration
        >>> round(E_3_3_5_e1(Pu=4.05, fiPn=11.05, Mu=44.16, fiMn=80.16), 2)
        0.66
    '''
    comb = Mu/fiMn + 1.07*Pu/fiPn
    limit = 1.42
    ratio = comb/limit
    return ratio

def E_3_3_5_e2(Pu, fiPn, Mu, fiMn):
    '''Ecuacion de interaccion flexion-corte. Ecuacion 3.3.3-1.
    Parameters
    ----------
        fiMn: float,
            resistencia de diseno a la flexion, cuando actua solo la flexion.
        fiPn: float,
            resistencia de diseno a una carga concentrada o reaccion, en ausencia de flexion segun seccion 3.3.4.
        Mu: float,
            resistencia requerida a la flexion. 
        Pu: float,
            resistencia requerida a una carga concentrada o reaccion, en ausencia de flexion.
    Returns
    -------
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.
    Tests
    -----
        >>> round(E_3_3_5_e2(Pu=4.05, fiPn=11.05, Mu=44.16, fiMn=80.16), 2)
        0.65
    '''
    comb = 0.82*Pu/fiPn + Mu/fiMn
    limit = 1.32
    ratio = comb/limit
    return ratio
    
## 3.4 Compression Members
def E_3_4_e1(Fn, Ae):
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
        >>> round( E_3_4_e1(1.5, 1.5), 4)
        1.9125
    '''
    fi_c = 0.85 # factor de resistencia a compresion
    fiPn = fi_c*Fn*Ae
    return fiPn

def E_3_4_2_e1(E0, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
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
            Tension critica de pandeo torsional con eta=1.

        Tests
        -----
            >>> round ( E_3_4_2_e1(E0 = 180510, Kt = 0.5, Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
            276.66
    """
    x0 = -abs(c_x-sc_x) # distancia desde el centroide al centro de corte, negativo
    r0 = E_3_3_1_2_e9(rx= rx, ry=ry, x0=x0) # radio de giro polar

    s_t_eta = E_3_3_1_2_e8(E0=E0, Kt= Kt, Lt=Lt, r0=r0, A=A, Cw=Cw, G0=G0, J=J)
    Fn = s_t_eta*eta
    return Fn

def E_3_4_3_e1(E0, Kx, Lx, Kt, Lt, rx, ry, eta, c_x, sc_x, A, Cw, G0, J):
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
            Tension critica de pandeo flexo-torsional con eta=1.

        Tests
        -----
            >>> round ( E_3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = 1800, Kt = 0.5, Lt = 1800, rx = 40.272, ry = 18.2673, eta = 0.6225, c_x = 15.59, sc_x = -23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239), 2)
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

def E_3_4_3_e3(E0, K, L, r, eta):
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
            >>> round (E_3_4_3_e3(E0 = 180510 ,K = 0.5,L = 1800, r = 40.272 , eta = 0.6225), 2)
            2220.56
    '''
    s_ex_eta = E_3_3_1_2_e6(E0=E0, K=K, L=L, r=r)
    s_ex = s_ex_eta*eta
    return s_ex


## 3.5 Combined Axial Load and Bending
def E_3_5_e1(Pu, fiPn, Mu_x, Mu_y, fiMn_x, fiMn_y, alpha_nx, alpha_ny, Cm_x, Cm_y):
    '''Ecuacion de interaccion para carga axial y flexion. Caso Pu/fiPn > 0.15.
    Parameters
    ----------
        Pu: float,
            resistencia axial requerida a la compresion.
        fiPn: float,
            resistencia de diseno a la compresion.
        Mu_x, Mu_y: float,
            resistencias requeridas a la flexion.
        fiMn_x, fiMn_y: float,
            resistencias de diseno a la flexion.
        alpha_nx, alpha_ny: float,
            factores de amplificacion.
        Cm_x, Cm_y: float,
            coeficientes segun restriccion en la junta.
    
    Returns
    -------
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.

    Tests
    -----
        >>> round(E_3_5_e1(Pu=3.22, fiPn=10.97, Mu_x=0.0, Mu_y=6.44, fiMn_x=1.0, fiMn_y=36.36, alpha_nx=1.0, alpha_ny=0.707, Cm_x=1.0, Cm_y=1.0), 3)
        0.544
    '''
    return Pu/fiPn + Cm_x*Mu_x/(fiMn_x*alpha_nx) + Cm_y*Mu_y/(fiMn_y*alpha_ny)

def E_3_5_e2(Pu, fiPn_0, Mu_x, Mu_y, fiMn_x, fiMn_y):
    '''Ecuacion de interaccion para carga axial y flexion. Caso Pu/fiPn > 0.15.
    Parameters
    ----------
        Pu: float,
            resistencia axial requerida a la compresion.
        fiPn_0: float,
            resistencia de diseno a la compresion segun seccion 3.4 con Fn=FY.
        Mu_x, Mu_y: float,
            resistencias requeridas a la flexion.
        fiMn_x, fiMn_y: float,
            resistencias de diseno a la flexion.
    
    Returns
    -------
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.

    Tests
    -----
        >>> round(E_3_5_e2(Pu=3.22, fiPn_0=45.58, Mu_x=0.0, Mu_y=6.44, fiMn_x=1.0, fiMn_y=36.36), 3)
        0.248
    '''
    return Pu/fiPn_0 + Mu_x/fiMn_x + Mu_y/fiMn_y

def E_3_5_e3(Pu, fiPn, Mu_x, Mu_y, fiMn_x, fiMn_y):
    '''Ecuacion de interaccion para carga axial y flexion. Caso Pu/fiPn <= 0.15.
    Parameters
    ----------
        Pu: float,
            resistencia axial requerida a la compresion.
        fiPn: float,
            resistencia de diseno a la compresion.
        Mu_x, Mu_y: float,
            resistencias requeridas a la flexion.
        fiMn_x, fiMn_y: float,
            resistencias de diseno a la flexion.
    
    Returns
    -------
        ratio: float,
            ratio entre las resistencias requeridas y las correspondientes de diseno.

    Tests
    -----
        >>> round(E_3_5_e3(Pu=3.22, fiPn=30.0, Mu_x=0.0, Mu_y=6.44, fiMn_x=1.0, fiMn_y=36.36), 3)
        0.284
    '''
    return Pu/fiPn + Mu_x/fiMn_x + Mu_y/fiMn_y

def E_3_5_e4(Pu, Pe):
    '''Magnification factor.
    Parameters
    ---------- 
        Pu: float,
            resistencia requerida axial a la compresion.
        Pe: float,
            resistencia de pandeo elastico.
    Returns
    -------
        alpha_n: float,
            factor de amplificacion.
    Tests
    -----
        >>> round(E_3_5_e4(Pu=3.22, Pe=0.85*12.91), 3)
        0.707
    '''
    return (1 - Pu/Pe)

def E_3_5_e5(E0, Kb, Lb, Ib):
    '''Elastic Buckling Strength.
    Parameters
    ----------
        fiMn_x, fiMn_y: float,
            resistencias de diseno a la flexion, cuando actuan solas.
        fiPn: float,
            resistencia de diseno axial a la compresion.
        Mu_x, Mu_y: float,
            resistencias requeridas a la flexion. 
        Pu: float,
            resistencia requerida axial a la compresion.
    Returns
    -------
        Pe: float,
            resistencia de pandeo elastico.
    Tests
    -----
        >>> round(E_3_5_e5(E0=27000, Kb=1.0, Lb=4*12, Ib=5.357), 2)
        619.59
    '''
    return pi**2*E0*Ib/(Kb*Lb)**2

#####################################################################################
#####################################################################################