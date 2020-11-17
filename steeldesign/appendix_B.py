'''Ecuaciones del Apéndice B de ASCE - 8 - 02

'''

def B_1(FY, E0, offset, n, s):
    '''Modulo elasticidad secante segun Eq B-1

    Parameters
    ----------
    E0 : float
        Modulo elasticidad inicial
    FY : float
        Tension de fluencia con una deformacion permanente de offset
    offset : float
        Valor de deformacion permanente a la que se obtuvo FY
    n : float
        Exponente de Ramberg-Osgood
    s : float
        Tension a la que se debe determinar Es

    Returns
    ----------
    float
        Modulo secante Es para la tension s

    Raises
    ------
    none

    Tests
    -----
    >>> round( B_1(344.8, 186200,  0.002, 4.58, 159.3), 2)
    174334.98

    '''
    Es = E0 / (1 + offset*E0* ( s**(n-1)/(FY**n)) )
    return Es

def B_2(FY, E0, offset, n, s):
    '''Modulo elasticidad tangente segun Eq B-2

    Parameters
    ----------
    E0 : float
        Modulo elasticidad inicial
    FY : float
        Tension de fluencia con una deformacion permanente de offset
    offset : float
        Valor de deformacion permanente a la que se obtuvo FY
    n : float
        Exponente de Ramberg-Osgood
    s : float
        Tension a la que se debe determinar Et

    Returns
    ----------
    float
        Modulo tangente Et para la tension s

    Raises
    ------
    none

    Tests
    -----
    >>> round( B_2(344.8, 186200,  0.002, 4.58, 159.3), 2)
    141952.2

    '''
    Et = E0*FY/(FY+offset*n*E0* (s/FY)**(n-1))
    return Et   


def B_1(FY, E0, offset, n, s):
    '''Modulo elasticidad secante segun Eq B-1

    Parameters
    ----------
    E0 : float
        Modulo elasticidad inicial
    FY : float
        Tension de fluencia con una deformacion permanente de offset
    offset : float
        Valor de deformacion permanente a la que se obtuvo FY
    n : float
        Exponente de Ramberg-Osgood
    s : float
        Tension a la que se debe determinar Es

    Returns
    ----------
    float
        Modulo secante Es para la tension s

    Raises
    ------
    none

    Tests
    -----
    >>> round( B_1(344.8, 186200,  0.002, 4.58, 159.3), 2)
    174334.98

    '''
    Es = E0 / (1 + offset*E0* ( s**(n-1)/(FY**n)) )
    return Es

def B_5(sigma, FY, E0, offset, n):
    '''Coeficiente de plasticidad para pandeo de columnas o LTB de vigas, segun Eq B-5.

    Parameters
    ----------
    sigma: float,
        tension normal.
    FY : float
        Tension de fluencia con una deformacion permanente de offset
    E0 : float
        Modulo elasticidad inicial
    offset : float
        Valor de deformacion permanente a la que se obtuvo FY
    n : float
        Exponente de Ramberg-Osgood

    Returns
    ----------
    eta: float
        Coeficiente de plasticidad.

    Raises
    ------
    none

    Tests
    -----
    >>> round( B_5(), 2)
    '''
    eta = FY/(FY + offset*n*E0*(sigma/FY)**(n-1))
    return eta

def TableA12(tau):
    '''Coeficiente de plasticidad para pandeo de columnas o LTB de vigas, segun Eq B-5.

    Parameters
    ----------
    tau: float,
        tension de corte para calcular eta_shear.

    Returns
    ----------
    eta_shear: float
        Coeficiente de plasticidad por corte.

    Raises
    ------
    none

    Tests
    -----
    >>> round( B_5(), 2)

    '''
    