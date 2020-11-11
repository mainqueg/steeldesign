#!/usr/bin/env python2.7

'''Script para Abaqus CAE que genera profiles a partir los parametros definidos en un archivo *.pf

Perfiles implementados:

c_profile : 
    Crea un perfil C, con sistema de coordenadas en el centroide de la sección
c_profile_w_lps : 
    Crea un perfil C con refuerzo de labios, con sistema de coordenadas en el centroide de la sección

Se debe indicar el archivo *.pf desde donde se crean los perfiles. Tiene que estar en el cwd donde se corre el script.

Se debe indicar el Model donde se crean los perfiles.

sample.pf :
    {
        "1": {
            "B": 50, 
            "name": "Cee100", 
            "H": 100, 
            "r_out": 7.5, 
            "t": 1.5, 
            "type": "c_profile"
        }, 
        "2": {
            "B": 50, 
            "name": "Cee70", 
            "H": 70, 
            "r_out": 7.5, 
            "t": 1.5, 
            "type": "c_profile"
        }, 
        "3": {
            "B": 50, 
            "name": "Cee70_w_lps", 
            "H": 70, 
            "r_out": 3.75, 
            "t": 1.5, 
            "type": "c_profile_w_lps", 
            "D": 12
        }
    }

'''

from abaqus import *
from abaqusConstants import *
from caeModules import *
from glob import glob
import json
from os import getcwd, path

pfFile = ''
while not pfFile:
    pfFile = glob('*.pf')
    if pfFile:
        pfFile = getInput('Archivo con perfiles:', pfFile[0])
        file = path.join(getcwd(), pfFile)
        if not path.isfile(file):
            print 'El archivo', pfFile,'no existe. Ingrese otro nombre.'
            pfFile = ''
    else:
        pfFile = getInput('Archivo con perfiles:')
        file = path.join(getcwd(), pfFile)
        if not path.isfile(file):
            print 'El archivo', pfFile,'no existe. Ingrese otro nombre.'
            pfFile = ''
        
    
with open(pfFile, 'r') as openfile: 
    profiles = json.load(openfile)

def c_profile(mdb, model, H, B, t, name):
    cgY = H/2.0
    b = B - t/2.0
    h = H - t
    A = t*(h + 2*b)
    cgX = 2*t/A*(b*b/2.0) # AISI Manual r=0
    cgY = h/2.0
    mdb.models[model].ArbitraryProfile( name=name,
    table=((b-cgX, 0.0-cgY, t), (0.0-cgX, 0.0-cgY, t),
           (0.0-cgX, h-cgY, t), (b-cgX, h-cgY, t)
           )
    )
        
def c_profile_w_lps(mdb, model, H, B, D, t, name):
    cgY = H/2.0
    b = B - t/2.0
    h = H - t
    d = D - t/2.0
    A = t*(h + 2*b + 2*d)
    cgX = 2*t/A*(b*(b/2.0) + d*b) # AISI Manual r=0
    cgY = h/2.0
    mdb.models[model].ArbitraryProfile( name=name, 
        table=((b-cgX, d-cgY), (b-cgX, 0.0-cgY, t), (0.0-cgX, 0.0-cgY, t),
            (0.0-cgX, h-cgY, t), (b-cgX, h-cgY, t), (b-cgX, h-d-cgY, t)
            )
        )

model= ''
while not model:
    defModel= mdb.models.keys()[0]
    model = getInput('Nombre del modelo:', defModel)
    if mdb.models.has_key(model):
        pass
    else:
        print 'El modelo', model,'no existe. Ingrese otro nombre.'
        model = ''

for profile in profiles.items():
    profile = profile[1]
    if profile['type'] == 'c_profile':
        c_profile(mdb, model, profile['H'], profile['B'], profile['t'], str(profile['name']))
    if profile['type'] == 'c_profile_w_lps':
        c_profile_w_lps(mdb, model, profile['H'], profile['B'], profile['D'], profile['t'], str(profile['name']))