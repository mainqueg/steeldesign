'''Funciones comunes al analisis segun ASCE 8.

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