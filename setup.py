from distutils.core import setup

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
  name = 'steeldesign',         
  packages = ['steeldesign','steeldesign/modules'],  
  version = '0.1.0',     
  license='MIT',       
  description = 'ASCE-8 steeldesign',
  #long_description = long_description ,
  #long_description_content_type='text/markdown',
  author = 'mainqueg',  
  author_email = 'mainquegreen@gmail.com',   
  url = 'https://github.com/mainqueg/steeldesign',  
  download_url = 'https://github.com/mainqueg/steeldesign', 
  keywords = ['steeldesign'],  
  install_requires=[        
          'MathPy',
          'sectionproperties',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: End Users/Desktop',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
  ],
)

