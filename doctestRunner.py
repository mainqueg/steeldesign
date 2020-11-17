if __name__ == "__main__":
    import doctest
    import steeldesign
    import sys
    test = input('Archivo a testear:')
    module = sys.modules['steeldesign.modules.'+test]
    doctest.testmod(module, verbose= True)