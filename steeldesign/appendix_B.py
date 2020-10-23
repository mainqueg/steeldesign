'''Ecuaciones del Apéndice B de ASCE - 8 - 02

'''

def B_1(FY, E0, offset, n, s):
    '''Modulo elasticidad secante segun Eq B-1

    # Parametros
    E0: Modulo elasticidad inicial
    FY: Tension de fluencia con una deformacion permanente de offset
    offset: Valor de deformacion permanente a la que se obtuvo FY
    n: Exponente de Ramberg-Osgood
    s: Tension a la que se debe determinar Et

    # Tests
    >>> round( B_1(344.8, 186200,  0.002, 4.58, 159.3), 2)
    174334.98

    '''
    Es = E0 / (1 + offset*E0* ( s**(n-1)/(FY**n)) )
    return Es

def B_2(FY, E0, offset, n, s):
    '''Modulo elasticidad tangente segun Eq B-2

    # Parametros
    E0: Modulo elasticidad inicial
    FY: Tension de fluencia con una deformacion permanente de offset
    offset: Valor de deformacion permanente a la que se obtuvo FY
    n: Exponente de Ramberg-Osgood
    s: Tension a la que se debe determinar Et

    # Tests
    >>> round( B_2(344.8, 186200,  0.002, 4.58, 159.3), 2)
    141952.2

    '''
    Et = E0*FY/(FY+offset*n*E0* (s/FY)**(n-1))
    return Et    