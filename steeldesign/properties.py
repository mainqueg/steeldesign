'''Propiedades de perfiles y materiales.

    Classes and functions
    ---------------------
        c_profile : class
            Crea un perfil C y calcula propiedades geometricas.

        c_w_lps_profile : class
            Crea un perfil C reforzado con labios y calcula propiedades geometricas.

        steel : class
            Acero con un modelo de Ramberg-Osgood.
        
        Tests
        -----
        En definiciones
'''


import pickle
import os
import sectionproperties.pre.sections as sections
from sectionproperties.analysis.cross_section import CrossSection
from appendix_B import B_1, B_2


class steel():
    ''' Creo un acero. 

        Parameters
        ----------
        FY : float
            Tension de fluencia obtenida a un determinado valor de offset 
        E0 : float
            Modulo elasticidad incial
        nu : float
            Coeficiente poisson. Def: 0.3
        n : float
            Exponente del modelo de Ramberg-Osgood. Def: 1.0
        offset : float
            Valor de offset al que se obtiene FY
        name : string
            Nombre del acero definido
        
        Attibutes
        ---------
            Mismos que los parametros y se agregan:
        G0  : float
            Modulo de corte inicial
        
        Methods
        -------
        Et(s) : float
            Módulo elastico tangente a la tensión s
        Es(s) : float
            Módulo elastico secante a la tensión s
        eta(s) : float
            Factor de plasticidad a la tensión s

        Tests
        ------
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
        self.name = name
        self.G0 = E0 / 2 / (1 + nu)

    def Et(self, s):
        ''' Modulo elastico tangente a la tension s. Eq B-2
            
            Parameters
            ----------
            s : float
                Tension para el calculo

            Returns
            -------
            Et : float
                Modulo elastico tangente

            Raises
            ------
            none

            Tests
            -----
            En definicion de la clase        
        '''
        Et = B_2(self.FY, self.E0, self.offset, self.n, s)
        return Et
    
    def Es(self, s):
        ''' Modulo elastico secante a la tension s. Eq B-1

            Parameters
            ----------
            s : float
                Tension para el calculo

            Returns
            -------
            Es : float
                Modulo elastico secante

            Raises
            ------
            none

            Tests
            -----
            En definicion de la clase 
        '''
        Es = B_1(self.FY, self.E0, self.offset, self.n, s)
        return Es

    def eta(self, s):
        ''' Factor de plasticidad a la tension s. Et/E0 Eq B-5

            Parameters
            ----------
            s : float
                Tension para el calculo

            Returns
            -------
            eta : float
                Factor de plasticidad

            Raises
            ------
            none

            Tests
            -----
            En definicion de la clase
        '''
        return self.Et(s) / self.E0

class c_w_lps_profile():
    '''Perfil C con labios de refuerzos.

        Parameters
        ----------
        H : float
            Altura
        B : float
            ancho
        D : float
            largo del labio
        t : float
            espesor
        r_out : float
            Radio externo de los plegados
        name : string
            Nombre para el perfil, sino se asigna uno por defecto
        
        Attibutes
        ---------
            Mismos que los parametros y se agregan:
        type : string
            'c_w_lps'
        rx, ry : float
            radio de giro del miembro | sqrt(I/A)
        c_x, c_y : float
            coordenada del centroide de la seccion
        sc_x, sc_y : float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        J : float
            Constante de torsion de St. Venant
        
        Methods
        -------
        calculate() :
            Ejecuta el calculo de las propiedades de la seccion
        Ae(Fn) : float
            Calcula el area efectiva para la tension Fn

        Tests
        -----
            >>> p1 = c_w_lps_profile(H = 100, B = 50, D = 12, t = 1.5, r_out = 3.75)
            >>> p1.calculate()
            >>> round( p1.A, 2)
            319.04
            >>> round( p1.rx, 2)
            40.27
            >>> round( p1.c_x, 2)
            16.33
    '''

    def __init__(self, H, B, D, t, r_out, name = ''):
        self.type = 'c_w_lps'
        self.B = B
        self.D = D
        self.H = H
        self.t = t
        self.r_out= r_out
                
        defName = 'Cee_w_lps_H'+str(round(H,3))+'_D'+str(round(D,3))+'_B'+str(round(B,3))+'_t'+str(round(t,3))+'_r-out'+str(round(r_out,3))
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

            Referencia
            ----------
                rx, ry : radio de giro del miembro | sqrt(I/A)
                c_i : coordenada del centroide de la seccion
                sc_i : coordenada del centro de corte
                A : Area de la seccion
                Cw : Constante torsional de warping de la seccion
                J : Constante de torsion de St. Venant

        '''
        try:
            self.load()
        except:
            ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
            geometry = sections.CeeSection(d=self.H, b=self.B, l=self.D, t=self.t, r_out=self.r_out, n_r=8)
            # create mesh
            mesh = geometry.create_mesh(mesh_sizes=[self.t/4.0])
            # creo la seccion
            section = CrossSection(geometry, mesh)
            # calculo las propiedades
            section.calculate_geometric_properties()
            section.calculate_warping_properties()

            (self.c_x, self.c_y) = section.get_c() # centroides
            (self.sc_x, self.sc_y) = section.get_sc() # shear center
            self.Cw = section.get_gamma() # warping
            (self.rx, self.ry) = section.get_rc() # radios de giro
            self.J = section.get_j()
            self.A = section.get_area()

            self.save()

            self.section = section

    def Ae(self, Fn):
        print('Ae() NotImplementedError')
        return self.A

    def save(self):
        """save class as self.name.sp"""
        path = os.path.join(os.getcwd(), 'sectionsDB',self.name)
        if not os.path.isdir(path):
            os.makedirs(path)

        file = os.path.join(path, self.name + '.sp')
        with open(file, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        path = os.path.join(os.getcwd(), 'sectionsDB', self.name)
        file = os.path.join(path, self.name + '.sp')
        with open(file, 'rb') as input:
            """try load self.name.sp"""
            p = pickle.load(input)
            self.rx = p.rx
            self.ry = p.ry
            self.c_x = p.c_x
            self.c_y = p.c_y
            self.sc_x = p.sc_x
            self.sc_y = p.sc_y
            self.A = p.A
            self.Cw = p.Cw
            self.J = p.J

class c_profile():
    '''Perfil C.

        Parameters
        ----------
        H : float
            Altura
        B : float
            ancho
        t : float
            espesor
        r_out : float
            Radio externo de los plegados
        name : string
            Nombre para el perfil, sino se asigna uno por defecto
        
        Attibutes
        ---------
            Mismos que los parametros y se agregan:
        type : string
            'c_w_lps'
        rx, ry : float
            radio de giro del miembro | sqrt(I/A)
        c_x, c_y : float
            coordenada del centroide de la seccion
        sc_x, sc_y : float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        J : float
            Constante de torsion de St. Venant
        
        Methods
        -------
        calculate() :
            Ejecuta el calculo de las propiedades de la seccion
        Ae(Fn) : float
            Calcula el area efectiva para la tension Fn

        Tests
        -----
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
    def __init__(self, H, B, t, r_out, name = ''):
        self.type = 'cee'
        self.B = B
        self.H = H
        self.t = t
        self.r_out= r_out
                
        defName = 'Cee_H'+str(round(H,3))+'_B'+str(round(B,3))+'_t'+str(round(t,3))+'_r-out'+str(round(r_out,3))
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

        Referencia
        ----------
            rx, ry : radio de giro del miembro | sqrt(I/A)
            c_i : coordenada del centroide de la seccion
            sc_i : coordenada del centro de corte
            A : Area de la seccion
            Cw : Constante torsional de warping de la seccion
            J : Constante de torsion de St. Venant

        '''
        try:
            self.load()
        except:
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

            (self.c_x, self.c_y) = section.get_c() # centroides
            (self.sc_x, self.sc_y) = section.get_sc() # shear center
            self.Cw = section.get_gamma() # warping
            (self.rx, self.ry) = section.get_rc() # radios de giro
            self.J = section.get_j()
            self.A = section.get_area()

            self.save()

            self.section = section
 
    def Ae(self, Fn):
        print('Ae() NotImplementedError')
        # Ancho efectivo
        ## Ala
        #Beff = 1 # calculo a partir de sec_2
        #Ae = self.A - (self.B-2*self.r_out-Beff)*self.t
        ## Alma
        #Heff = 1 # calculo a partir de sec_2
        #Ae = Ae - (self.H-2*self.r_out-Heff)*self.t
        return self.A

    def save(self):
        """save class as self.name.sp"""
        path = os.path.join(os.getcwd(), 'sectionsDB',self.name)
        if not os.path.isdir(path):
            os.makedirs(path)

        file = os.path.join(path, self.name + '.sp')
        with open(file, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        path = os.path.join(os.getcwd(), 'sectionsDB', self.name)
        file = os.path.join(path, self.name + '.sp')
        with open(file, 'rb') as input:
            """try load self.name.sp"""
            p = pickle.load(input)
            self.rx = p.rx
            self.ry = p.ry
            self.c_x = p.c_x
            self.c_y = p.c_y
            self.sc_x = p.sc_x
            self.sc_y = p.sc_y
            self.A = p.A
            self.Cw = p.Cw
            self.J = p.J
class I_builtup_c_w_lps_profile():
    '''Perfil C con labios de refuerzos.

        Parameters
        ----------
        H : float
            Altura
        B : float
            ancho
        D : float
            largo del labio
        t : float
            espesor
        r_out : float
            Radio externo de los plegados
        s : float
            Gap entre almas de los perfiles
        name : string
            Nombre para el perfil, sino se asigna uno por defecto
        
        Attibutes
        ---------
            Mismos que los parametros y se agregan:
        type : string
            'I_builtup_cee_wlps'
        rx, ry : float
            radio de giro de la seccion | sqrt(I/A)
        ri : float
            radio de giro de un solo perfil c respecto de -y-
        c_x, c_y : float
            coordenada del centroide de la seccion
        sc_x, sc_y : float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        J : float
            Constante de torsion de St. Venant
        
        Methods
        -------
        calculate() :
            Ejecuta el calculo de las propiedades de la seccion
        Ae(Fn) : float
            Calcula el area efectiva para la tension Fn

        Tests
        -----
            >>> p1 = I_builtup_c_w_lps_profile(H=8*25.4, B=6*25.4/2, D=0.7*25.4, t=0.075*25.4, r_out=(3/32+0.075)*25.4)
            >>> p1.type
            'I_builtup_cee_wlps'
            >>> p1.calculate()
            >>> round( p1.A, 2)
            1438.81
            >>> round( p1.rx, 2)
            79.92
            >>> round( p1.ry, 2)
            34.83
            >>> round( p1.ri, 2)
            27.31
            >>> round( p1.J, 2)
            4404.83
            >>> round( p1.Cw, 2)
            18878923357.87
            >>> p1 = I_builtup_c_w_lps_profile(H=8*25.4, B=6*25.4/2, D=0.7*25.4, t=0.075*25.4, r_out=(3/32+0.075)*25.4, s=0.1)
            >>> p1.type
            'I_builtup_cee_wlps'
            >>> p1.name
            'I_builtup_Cee_w_lps_H203.2_D17.78_B76.2_t1.905_r-out4.286_s0.1'
            >>> p1.calculate()
            >>> round( p1.A, 2)
            1438.81
            >>> round( p1.rx, 2)
            79.92
            >>> round( p1.ry, 2)
            34.86
            >>> round( p1.ri, 2)
            27.31
            >>> round( p1.J, 2)
            1735.09
            >>> round( p1.Cw, 2)
            78155388323.49
            
    '''

    def __init__(self, H, B, D, t, r_out, s = 0.0, name = ''):
        self.type = 'I_builtup_cee_wlps'
        self.B = B
        self.D = D
        self.H = H
        self.t = t
        self.r_out= r_out
        self.s = s
                
        defName = 'I_builtup_Cee_w_lps_H'+str(round(H,3))+'_D'+str(round(D,3))+'_B'+str(round(B,3))+'_t'+str(round(t,3))+'_r-out'+str(round(r_out,3))+'_s'+str(round(s,3))
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

            Referencia
            ----------
                rx, ry : radio de giro de la seccion | sqrt(I/A)
                ri : radio de giro en -y- de un solo perfil c
                c_x, c_y : coordenada del centroide de la seccion
                sc_x, sc_y : coordenada del centro de corte
                A : Area de la seccion
                Cw : Constante torsional de warping de la seccion
                J : Constante de torsion de St. Venant

        '''
        try:
            self.load()
        except:
            ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
            c1 = sections.CeeSection(d=self.H, b=self.B, l=self.D, t=self.t, r_out=self.r_out, n_r=8)
            c2 = sections.CeeSection(d=self.H, b=self.B, l=self.D, t=self.t, r_out=self.r_out, n_r=8, shift= [0,-self.H])

            c2.rotate_section(angle=180, rot_point=[0, 0])

            if self.s:
                c1.shift = [self.s/2, 0]
                c1.shift_section()

                c2.shift = [-self.s/2, 0]
                c2.shift_section()

            geometry = sections.MergedSection([c1, c2])
            geometry.clean_geometry()

            # create mesh
            mesh_c1 = c1.create_mesh(mesh_sizes=[self.t/2.0])
            mesh = geometry.create_mesh(mesh_sizes=[self.t/2.0, self.t/2.0])
            # creo la seccion
            section_c1 = CrossSection(c1, mesh_c1)
            section = CrossSection(geometry, mesh)
            # calculo las propiedades
            section_c1.calculate_geometric_properties()
            #section_c1.calculate_warping_properties()
            section.calculate_geometric_properties()
            section.calculate_warping_properties()

            (self.c_x, self.c_y) = section.get_c() # centroides
            (self.sc_x, self.sc_y) = section.get_sc() # shear center
            self.Cw = section.get_gamma() # warping
            (self.rx, self.ry) = section.get_rc() # radios de giro
            self.J = section.get_j()
            self.A = section.get_area()
            (_, self.ri) = section_c1.get_rc() # radios de giro de c1

            self.save()

            self.section = section
            self.section_c1 = section_c1

    def Ae(self, Fn):
        print('Ae() NotImplementedError')
        return self.A

    def save(self):
        """save class as self.name.sp"""
        path = os.path.join(os.getcwd(), 'sectionsDB',self.name)
        if not os.path.isdir(path):
            os.makedirs(path)

        file = os.path.join(path, self.name + '.sp')
        with open(file, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        path = os.path.join(os.getcwd(), 'sectionsDB', self.name)
        file = os.path.join(path, self.name + '.sp')
        with open(file, 'rb') as input:
            """try load self.name.sp"""
            p = pickle.load(input)
            self.rx = p.rx
            self.ry = p.ry
            self.ri = p.ri
            self.c_x = p.c_x
            self.c_y = p.c_y
            self.sc_x = p.sc_x
            self.sc_y = p.sc_y
            self.A = p.A
            self.Cw = p.Cw
            self.J = p.J

class I_builtup_c_profile():
    '''Perfil C.

        Parameters
        ----------
        H : float
            Altura
        B : float
            ancho
        t : float
            espesor
        r_out : float
            Radio externo de los plegados
        s : float
            Gap entre almas de los perfiles
        name : string
            Nombre para el perfil, sino se asigna uno por defecto
        
        Attibutes
        ---------
            Mismos que los parametros y se agregan:
        type : string
            'I_builtup_cee'
        rx, ry : float
            radio de giro del miembro | sqrt(I/A)
        ri : float
            radio de giro de un solo perfil c respecto de -y-
        c_x, c_y : float
            coordenada del centroide de la seccion
        sc_x, sc_y : float
            coordenada del centro de corte
        A : float
            Area de la seccion
        Cw : float
            Constante torsional de warping de la seccion
        J : float
            Constante de torsion de St. Venant
        
        Methods
        -------
        calculate() :
            Ejecuta el calculo de las propiedades de la seccion
        Ae(Fn) : float
            Calcula el area efectiva para la tension Fn

        Tests
        -----
            >>> p1 = I_builtup_c_profile(H=8*25.4, B=6*25.4/2, t=0.075*25.4, r_out=(3/32+0.075)*25.4)
            >>> p1.type
            'I_builtup_cee'
            >>> p1.name
            'I_builtup_Cee_H203.2_B76.2_t1.905_r-out4.286_s0.0'
            >>> p1.calculate()
            >>> round( p1.A, 2)
            1348.87
            >>> round( p1.rx, 2)
            79.29
            >>> round( p1.ry, 2)
            30.37
            >>> round( p1.ri, 2)
            23.47
            >>> round( p1.J, 2)
            4295.84

    '''
    def __init__(self, H, B, t, r_out, s = 0.0, name = ''):
        self.type = 'I_builtup_cee'
        self.B = B
        self.H = H
        self.t = t
        self.r_out= r_out
        self.s = s
                
        defName = 'I_builtup_Cee_H'+str(round(H,3))+'_B'+str(round(B,3))+'_t'+str(round(t,3))+'_r-out'+str(round(r_out,3))+'_s'+str(round(s,3))
        # creo un nombre para la seccion
        if not name:
            self.name = defName

    def calculate(self):
        '''Se ejecuta el calculo de las propiedades de la seccion.

        Referencia
        ----------
            rx, ry : radio de giro de la seccion | sqrt(I/A)
            ri : radio de giro en -y- de un solo perfil c
            c_x, c_y : coordenada del centroide de la seccion
            sc_x, sc_y : coordenada del centro de corte
            A : Area de la seccion
            Cw : Constante torsional de warping de la seccion
            J : Constante de torsion de St. Venant

        '''
        try:
            self.load()
        except:
            ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
            c1 = sections.CeeSection(d=self.H, b=self.B+self.r_out, l=self.r_out, t=self.t, r_out=self.r_out, n_r=8)
            c2 = sections.CeeSection(d=self.H, b=self.B+self.r_out, l=self.r_out, t=self.t, r_out=self.r_out, n_r=8, shift= [0,-self.H])
        
            # corto los labios y el radio c1
            p1 = c1.add_point([self.B, 0])
            p2 = c1.add_point([self.B, self.t])
            p3 = c1.add_point([self.B, self.H])
            p4 = c1.add_point([self.B, self.H-self.t])

            c1.add_facet([p1, p2])
            c1.add_facet([p3, p4])
            c1.add_hole([self.B+self.r_out/10, self.t/2])  # add hole
            c1.add_hole([self.B+self.r_out/10, self.H-self.t/2])  # add hole
            c1.clean_geometry()  # clean the geometry

            # corto los labios y el radio c2
            p1 = c2.add_point([self.B, 0])
            p2 = c2.add_point([self.B, self.t])
            p3 = c2.add_point([self.B, self.H])
            p4 = c2.add_point([self.B, self.H-self.t])

            c2.add_facet([p1, p2])
            c2.add_facet([p3, p4])
            c2.add_hole([self.B+self.r_out/10, self.t/2])  # add hole
            c2.add_hole([self.B+self.r_out/10, self.H-self.t/2])  # add hole
            c2.clean_geometry()  # clean the geometry

            c2.rotate_section(angle=180, rot_point=[0, 0])

            if self.s:
                c1.shift = [self.s/2, 0]
                c1.shift_section()

                c2.shift = [-self.s/2, 0]
                c2.shift_section()

            geometry = sections.MergedSection([c1, c2])
            geometry.clean_geometry()
            # create mesh
            mesh_c1 = c1.create_mesh(mesh_sizes=[self.t/2.0])
            mesh = geometry.create_mesh(mesh_sizes=[self.t/2.0, self.t/2.0])
            # creo la seccion
            section_c1 = CrossSection(c1, mesh_c1)
            section = CrossSection(geometry, mesh)
            # calculo las propiedades
            # calculo las propiedades
            section_c1.calculate_geometric_properties()
            #section_c1.calculate_warping_properties()
            section.calculate_geometric_properties()
            section.calculate_warping_properties()

            (self.c_x, self.c_y) = section.get_c() # centroides
            (self.sc_x, self.sc_y) = section.get_sc() # shear center
            self.Cw = section.get_gamma() # warping
            (self.rx, self.ry) = section.get_rc() # radios de giro
            self.J = section.get_j()
            self.A = section.get_area()
            (_, self.ri) = section_c1.get_rc() # radios de giro de c1

            self.save()

            self.section = section
            self.section_c1 = section_c1
 
    def Ae(self, Fn):
        print('Ae() NotImplementedError')
        # Ancho efectivo
        ## Ala
        #Beff = 1 # calculo a partir de sec_2
        #Ae = self.A - (self.B-2*self.r_out-Beff)*self.t
        ## Alma
        #Heff = 1 # calculo a partir de sec_2
        #Ae = Ae - (self.H-2*self.r_out-Heff)*self.t
        return self.A

    def save(self):
        """save class as self.name.sp"""
        path = os.path.join(os.getcwd(), 'sectionsDB',self.name)
        if not os.path.isdir(path):
            os.makedirs(path)

        file = os.path.join(path, self.name + '.sp')
        with open(file, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        path = os.path.join(os.getcwd(), 'sectionsDB', self.name)
        file = os.path.join(path, self.name + '.sp')
        with open(file, 'rb') as input:
            """try load self.name.sp"""
            p = pickle.load(input)
            self.rx = p.rx
            self.ry = p.ry
            self.ri = p.ri
            self.c_x = p.c_x
            self.c_y = p.c_y
            self.sc_x = p.sc_x
            self.sc_y = p.sc_y
            self.A = p.A
            self.Cw = p.Cw
            self.J = p.J

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


