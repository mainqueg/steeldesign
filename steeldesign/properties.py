import pickle
import os
import sectionproperties.pre.sections as sections
from sectionproperties.analysis.cross_section import CrossSection
from appendix_B import B_1, B_2


class steel():
    ''' Creo un acero. 

        Métodos:

        Et(s) = Módulo elastico tangente a la tensión s
        Es(s) = Módulo elastico secante a la tensión s
        eta(s) = Factor de plasticidad a la tensión s

    # Tests
    >>> mat = steel(344.8,186200.0, 0.3, 4.58, 0.002, name = 'SA304_1_4Hard')
    >>> round(mat.E0, 2)
    186200.0
    >>> round(mat.Et(159.3),2)
    141952.2
    >>> round(mat.Es(159.3),2)
    174334.98
    >>> round(mat.eta(159.3),4)
    0.7624
    >>> mat.name
    'SA304_1_4Hard'

    '''

    def __init__(self, FY, E0, nu = 0.3, n = 1.0, offset = 0.0, name = ''):
        self.FY = FY
        self.nu = nu
        self.n = n
        self.offset = offset
        self.E0 = E0
        self.G0 = E0 / 2 / (1 + nu)
        self.name = name

    def Et(self, s):
        ''' Modulo elastico tangente. Eq B-2

        
        '''
        Et = B_2(self.FY, self.E0, self.offset, self.n, s)
        return Et
    
    def Es(self, s):
        ''' Modulo elastico secante. Eq B-1

        '''
        Es = B_1(self.FY, self.E0, self.offset, self.n, s)
        return Es

    def eta(self, s):
        ''' Factor de plasticidad. Et/E0 Eq B-5

        '''
        return self.Et(s) / self.E0

class c_w_lps_profile():
    '''Perfil C con labios de refuerzos.

    # Parametros
    H: altura
    B: ancho
    D: largo del labio
    t: espesor
    r_out: Radio externo de los plegados
    name: Nombre para el perfil, sino se asigna uno por defecto
    plot: Grafica el perfil, centro de corte y centroide
    
    # Tests
    >>> p1 = c_w_lps_profile(H = 100, B = 50, D = 12, t = 1.5, r_out = 3.75)
    >>> p1.calculate()
    >>> round( p1.A, 2)
    319.04
    >>> round( p1.rx, 2)
    40.27
    >>> round( p1.c_x, 2)
    16.33
    '''

    def __init__(self, H, B, D, t, r_out, name = '', load = 'True'):
        self.type = 'c_w_lps'
        self.B = B
        self.D = D
        self.H = H
        self.t = t
        self.r_out= r_out
                
        defName = 'Cee_w_lps_H'+str(H)+str(D)+'_B'+str(B)+'_t'+str(t)+'_r-out'+str(r_out)
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

        # Propiedades:
        rx, ry: radio de giro del miembro | sqrt(I/A)
        c_i: coordenada del centroide de la seccion
        sc_i: coordenada del centro de corte
        A: Area de la seccion
        Cw: Constante torsional de warping de la seccion
        J: Constante de torsion de St. Venant

        '''

        ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
        geometry = sections.CeeSection(d=self.H, b=self.B, l=self.D, t=self.t, r_out=self.r_out, n_r=8)
        # create mesh
        mesh = geometry.create_mesh(mesh_sizes=[self.t/4.0])
        # creo la seccion
        section = CrossSection(geometry, mesh)
        # calculo las propiedades
        section.calculate_geometric_properties()
        section.calculate_warping_properties()

        (c_x, c_y) = section.get_c() # centroides
        (sc_x, sc_y) = section.get_sc() # shear center
        Cw = section.get_gamma() # warping
        (rx, ry) = section.get_rc() # radios de giro
        J = section.get_j()
        A = section.get_area()

        self.section = section
        
        self.rx = rx
        self.ry = ry
        self.c_x = c_x
        self.sc_x = sc_x
        self.A = A
        self.Cw = Cw
        self.J = J

    def effective(self):
        raise NotImplementedError

class c_profile():
    '''Perfil C.

    # Parametros
    H: altura
    B: ancho
    t: espesor
    r_out: Radio externo de los plegados
    name: Nombre para el perfil, sino se asigna uno por defecto
    plot: Grafica el perfil, centro de corte y centroide
    load: Cargar desde un archivo la seccion. Solo si name=''

    # Tests
    >>> p1 = c_profile(H = 100, B = 50, t = 1.5, r_out = 6+1.5)
    >>> p1.calculate()
    >>> round( p1.A, 2)
    286.54
    >>> round( p1.rx, 2)
    39.86
    >>> round( p1.c_x, 2)
    13.48
    >>> round( p1.Cw, 2)
    116369116.59
    >>> round( p1.J, 2)
    213.66

    '''

    def __init__(self, H, B, t, r_out, name = '', load = 'True'):
        self.type = 'cee'
        self.B = B
        self.H = H
        self.t = t
        self.r_out= r_out
                
        defName = 'Cee_H'+str(H)+'_B'+str(B)+'_t'+str(t)+'_r-out'+str(r_out)
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

        # Propiedades:
        rx, ry: radio de giro del miembro | sqrt(I/A)
        c_i: coordenada del centroide de la seccion
        sc_i: coordenada del centro de corte
        A: Area de la seccion
        Cw: Constante torsional de warping de la seccion
        J: Constante de torsion de St. Venant

        '''

        ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
        geometry = sections.CeeSection(d=self.H, b=self.B+self.r_out, l=self.r_out, t=self.t, r_out=self.r_out, n_r=8)
        # corto los labios y el radio
        p1 = geometry.add_point([self.B, 0])
        p2 = geometry.add_point([self.B, self.t])
        p3 = geometry.add_point([self.B, self.H])
        p4 = geometry.add_point([self.B, self.H-self.t])

        geometry.add_facet([p1, p2])
        geometry.add_facet([p3, p4])
        geometry.add_hole([self.B+self.r_out/10, self.t/2])  # add hole
        geometry.add_hole([self.B+self.r_out/10, self.H-self.t/2])  # add hole
        geometry.clean_geometry()  # clean the geometry
        # create mesh
        mesh = geometry.create_mesh(mesh_sizes=[self.t/4.0])
        # creo la seccion
        section = CrossSection(geometry, mesh)
        # calculo las propiedades
        section.calculate_geometric_properties()
        section.calculate_warping_properties()

        (c_x, c_y) = section.get_c() # centroides
        (sc_x, sc_y) = section.get_sc() # shear center
        Cw = section.get_gamma() # warping
        (rx, ry) = section.get_rc()
        J = section.get_j()
        A = section.get_area()

        self.section = section
        
        self.rx = rx
        self.ry = ry
        self.c_x = c_x
        self.sc_x = sc_x
        self.A = A
        self.Cw = Cw
        self.J = J
 
    def effective(self):
        raise NotImplementedError

def saveItem(item, fileName, mode = 'o'):
    '''Guarda en un archivo binario de nombre file la variable item.

    Por default hace un chequeo de existencia del archivo y solicita la confirmacion de sobreescritura.
    Si se desea sobreescribir directamenete, incluir una tercera variable con el caracter 'o'

    Requiere importar el paquete pickle

    Ejemplos:

    -------------------------------------------
    import pickle

    a = ['a','b', 'c']
    saveItem(a, 'aList.f')

    La variable -a- se puede recuperar con:
    file = open("aList.f", "rb")
    a = pickle.load(file)
    file.close()

    -------------------------------------------

    #Los items se pueden cargar con:
    file = open("item_0.dict", "rb")
    item = pickle.load(file)
    -------------------------------------------

    '''
    # modo de confirmacion para reemplazar archivos
    if mode == 'r':            
        nFile = fileName
        while os.path.isfile(nFile):
            print('File ' + nFile + ' already exist. Enter a new name or press Enter to replace.')
            nFile = input('')
            # En caso de que se quiera reemplazar otro archivo, guardo el nuevo nombre:
            if nFile: fileName = fileName
        if nFile: fileName = nFile

    with open(fileName, "wb") as file:
        pickle.dump(item, file)

