class Cisco():
    TERMINAL = 'terminal'
    ios = []

    def __init__(self):
        self.ios = []
        pass

    def enanble(self):
        self.ios.append('enable')

    def configure(self, value):
        self.ios.append('configure %s' % value)
    
    def interface(self, value):
        self.ios.append('interface %s' % value)
    def write(self):
        self.ios.append('write')
    def debug(self):
        # print(self.ios)
        print('\n'.join(self.ios))

class Switch(Cisco):
    def __init__(self):
        pass
class Route(Cisco):
    def __init__(self):
        pass

cisco = Cisco()
cisco.enanble()
cisco.configure(cisco.TERMINAL)
cisco.interface('fastethernet0/3')
cisco.write()
cisco.debug()
