'''Funciones comunes al analisis segun ASCE 8.

    eta_iter : 
        esquema de newton-rapson f(s): s- FF*eta(s) = 0
    adjustNeutralAxis : 
        busca el eje neutro de la seccion
    get_linear_stress :
        Devuelve el valor de tension en la coordenada indicada para una variacion lineal de tension

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
    ds = mat.FY/5000 # delta s para calcular la derivada
    err = 0.1 # error tolerado porcentual
    iterr = 0 #inicializo el contador de iteraciones
    eta = mat.eta(s) #inicializo eta
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

def adjustNeutralAxis(Ix, A, nEffAreas):
    '''Se calculan las nuevas propiedades efectivas (Ixx, cy) de la seccion  respecto de un nuevo eje neutro x'-x', a partir de quitar areas con propiedades Ixx_, A_, cx_

    Parameters
    ----------
        Ix : float
            Segundo momento de area de la seccion
        A : float
            Area de la seccion
        nEffAreas : dict {1:{}, 2:{}, }
            Propiedades geometricas de los segmentos con areas no-efectivas:
            t : float
                espesor del segmento no-efectivo
            b_ : float
                Longitud del segmento no-efectivo (= w-b)
            cy_ : float
                Coordenada -y- al eje x-x original del centroide del segmento no-efectivo 
            paralel : bool
                orientacion del segmento no efectivo
                True: b_ paralelo a x-x (e.g. flange)
                False: b_ perpendicular a x-x (e.g. web)
    Returns
    -------
        cy : float
            Distancia del nuevo eje neutro x'-x' al eje x-x original
    Tests
    -----
        # Ex. 1.1 Illustrative examples C-section: H= 6, t= 0.06, w= 1.471, b= 0.806
        >>> cy, Ixx= adjustNeutralAxis(2.68, 0.541, {1: {'t': 0.06, 'b_':1.471 - 0.806, 'cy_': (6-0.06)/2, 'paralel': True}})
        >>> print( '{:{fmt}}, {:{fmt}}'.format(cy, Ixx, fmt='.3f') )
        0.236, 2.300
        # Ex. 4.5 Cold-Formed Steel Design
        >>> nEffAreas= {1: {'b_': 1.0180380857045028, 'cy_': 4.9625, 'paralel': True, 't': 0.075},
        ... 2: {'b_': 0.6166109036450154, 'cy_': 1.7408312699259814, 'paralel': False, 't': 0.075},
        ... 3: {'b_': 0.44269505865706416, 'cy_': 4.501347529328532, 'paralel': False, 't': 0.075}}
        >>> cy, Ixx= adjustNeutralAxis(20.5216, 1.3431, nEffAreas)
        0.51, 17.51
    '''
    sumA_ = 0 # areas de los segmentos no efectivos
    sumQ_ = 0 # primer momento de area de los sementos no efectivos
    for nAreas in nEffAreas.values():
        t, b_, cy_, paralel = nAreas.values()
        A_ = b_*t
        sumA_ = sumA_ + A_ # area del segmento no-efectivo
        sumQ_ = sumQ_ + cy_*A_ # primer momento de area
    Ae = A - sumA_
    cy = sumQ_/Ae

    sumIxx_ = 0 # segundos momentos negativos de los segmentos no efectivos
    for nAreas in nEffAreas.values():
        t, b_, cy_, paralel = nAreas.values()
        if paralel:
            sumIxx_ = sumIxx_ + t**3*b_/12 + (cy_+cy)**2*b_*t
        else:
            sumIxx_ = sumIxx_ + t*b_**3/12 + (cy_+cy)**2*b_*t
    Ixx = Ix + A*cy**2 - sumIxx_

    return cy, Ixx

def get_linear_stress(fFlange, yCG, y):
    '''Tension s en la coordenada y considerando una distribucion lineal con una tension de compresion fFlange.
    Parameters
    ----------
        fFlange : float
            Tension de compresion en el ala (compresion +)
        yCG : float
            distancia desde el ala al eje neutro
        y : float
            coordenada desde el ala a compresion donde calcular la tension
    Returns
    -------
        s : float
            Tension en el punto y
    Tests
    -----
        # Ex. 1.1 Illustrative examples C-section: H= 6, r_out= 0.154, yCG= 3.236
        >>> round(get_linear_stress(fFlange= 50, yCG= 3.236, y= 0.154), 2)
        47.62
        >>> round(get_linear_stress(fFlange= 50, yCG= 3.236, y= 6-0.154), 2)
        -40.33
    '''
    s= fFlange- fFlange/yCG*y
    return s