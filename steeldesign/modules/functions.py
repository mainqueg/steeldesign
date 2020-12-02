'''Funciones comunes al analisis segun ASCE 8.

    eta_iter : 
        esquema de newton-rapson f(s): s- FF*eta(s) = 0
    adjustNeutralAxis : 
        busca el eje neutro de la seccion


'''

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

def adjustNeutralAxis(Ix, A, t, b_, cy_):
    '''Se calculan las nuevas propiedades de area Ixx, A, cx respecto de un nuevo eje neutro x'-x', a partir de quitar un area con propiedades Ixx_, A_, cx_

    Parameters
    ----------
        Ix : float
            Segundo momento de area de la seccion
        A : float
            Area de la seccion
        t : float
            espesor del segmento no-efectivo
        b_ : float
            Longitud del segmento no-efectivo (= w-b)
        cy_ : float
            Coordenada -y- al eje x-x original del centroide del segmento no-efectivo 
    Returns
    -------
        cy : float
            Distancia del nuevo eje neutro x'-x' al eje x-x original
    Tests
    -----
        # Ex. 1.1 Illustrative examples C-section: H= 6, t= 0.06, w= 1.471, b= 0.806
        >>> cy, Ixx= adjustNeutralAxis(2.68, 0.541, 0.06, 1.471 - 0.806, (6-0.06)/2)
        >>> print( '{:{fmt}}, {:{fmt}}'.format(cy, Ixx, fmt='.3f') )
        0.236, 2.300
    '''
    A_ = b_*t # area del segmento no-efectivo
    Ae = A - A_
    cy = cy_*A_/Ae

    Ixx_ = t**3*b_/12 + (cy_+cy)**2*A_
    Ixx = Ix + A*cy**2 - Ixx_

    return cy, Ixx