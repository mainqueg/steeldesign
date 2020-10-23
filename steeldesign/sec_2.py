'''Ecuaciones de la seccion 2 de ASCE - 8 - 02

'''

from math import pi
import numpy as np

class  sec2_1_1():
    '''Section 2.1.1: Dimensional Limits and Considerations.

    # Parametros
    profile: Dimensiones del perfil
    stiffCondition: Rigidización de los elementos 'UNSTIFFNED' (iii) | STIFFNED_SL (i) | STIFFNED (ii)

    '''
    #valores predefinidos
    def __init__(self, member):
        self.Name = 'Sec2.1.1'
        if member.profile.type == 'c_w_lps':
            self.w = member.profile.B
            self.wf = member.profile.B-member.profile.r_out
            self.t = member.profile.t
            self.L = member.L
            # chequear cada elemento de la seccion: alma/ala/labio
        elif member.profile.type == 'cee':
            self.w = member.profile.B
            self.wf = member.profile.B-member.profile.r_out
            self.t = member.profile.t
            self.L = member.L
            # chequear cada elemento de la seccion: alma/ala
        else:
            print('Error en chequeo de',self.Name,'. El perfil tipo', member.profile.type,'no está implementado.')

    def Cl_1(self, stiffCondition = 'UNSTIFFNED'):
        ''' Determina la relación máxima entre el ancho del ala y su esperor. Los valores limites se dan para tres condiciones de rigidización
        '''
        if stiffCondition == 'UNSTIFFNED':
            ratioAdm = 50.0 # 2.1.1-1.iii
            ratio = self.w/self.t
            print ('Esbeltez =',round(ratio,2), '<','Esbeltez admisible =', ratioAdm)
            return ratio < ratioAdm
        elif stiffCondition == 'STIFFNED':
            ratioAdm = 400.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (round(ratio,2), '<', ratioAdm)
            return ratio < ratioAdm
        elif stiffCondition == 'STIFFNED_SL':
            ratioAdm = 90.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (round(ratio,2), '<', ratioAdm)
            return ratio < ratioAdm
    def Cl_2(self):
        raise 'Not implemented'
    def Cl_3(self):
        '''Especifica el ancho efectivo en el caso de vigas cortas soportando una carga puntual.
        '''
        if self.L < 30*self.wf:
            self.ratio = self.TABLE1()
        else:
            self.ratio = 1.0
        self.w_eff = self.w*self.ratio
    def TABLE1(self):
        '''TABLE 1. Short, Wide Flanges: Maximum Allowable Ratio of Effective Design Width to Actual Width

        # Tests

        >>> TABLE1()
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
        r = np.interp( table1[:,0], table1[:,1], self.L/self.wf )
        return r
########################### USO
'''#INPUT:
flangeCURLING = 'False'
shearLag = 'True'
# VERIFICACION
for member in members:
    sec2_1_1 = sec2_1_1(memberProperties(member))
    print ('Los elementos del miembro', member, 'cumplen con las dimensiones requeridas:', sec2_1_1.Cl_1())
    if flangeCURLING:
        sec2_1_1.Cl_2
    if shearLag:
        sec2_1_1.Cl_3'''