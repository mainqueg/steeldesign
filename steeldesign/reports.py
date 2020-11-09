''' Genera la salida en formato legible.
Genera un reporte segun configuracion en archivo de input.

'''

from design import ASCE_8_02

'''
member = member(dfajlf)
member.analysis.s3_LTB

con un diccionario que se va cargando y despues se imprime como

Reporte es por miembro.
Reporte:
    - Resumen de estados limites.
    - Envolvente de cargas, min-max.
    - Propiedades de seccion
    - Resultados de estados limites
        - Aeff y calc intermedios

'''
reports = {
    1: {'name': 'Flexural buckling X', 'capacity': 257.4, 'demand': 200.3, 'ratio': 0.778,
        'intermediate':{
            1: {'name': 'Euler stress', 'value': 783.5},
            2: {'name': 'Nominal stress', 'value': 430.4},
            3: {'name': 'Nominal capacity', 'value': 300.4},
                }
        },
    2: {'name': 'Flexural buckling Y', 'capacity': 257.4, 'demand': 200.3, 'ratio': 0.778,
        'intermediate':{
            1: {'name': 'Euler stress:', 'value': 783.5},
            2: {'name': 'Nominal stress:', 'value': 430.4},
            3: {'name': 'Nominal capacity:', 'value': 300.4},
            4: {'name': 'Effective Area:', 'value': 31.4},
                }
        },
    }



keys = ['capacity','demand','ratio']

sep = '\n###################################################################'

for _, limState in reports.items():
    
    print(sep)
    print('>>>>>>  ',limState['name'], '   <<<<<<\n')
    print('\tCapacity:', limState['capacity'], '| Demand', limState['demand'],'| Ratio:', limState['ratio'])
    
    if limState['intermediate']:
        print('\n\t Intermediate Results:')
        for _, intermediate in limState['intermediate'].items():
            print('\t\t *', intermediate['name'], intermediate['value'])