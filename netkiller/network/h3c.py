class H3C():
    TERMINAL = 'terminal'
    ios = []

    def __init__(self):
        # self.ios = []
        pass

    def system_view(self):
        self.ios.append('system-view')

    def configure(self, value):
        self.ios.append('configure %s' % value)

    class Display():
        def __init__(self):
            super().__init__()
            pass
        # def __del__(self):

        def current(self):
            H3C.ios.append('current-configuration')
        def saved(self):
            H3C.ios.append('saved-configuration')
    class Interface():
        def __init__(self):
            pass
        def ethernet(self,value):
            H3C.ios.append('interface Ethernet %s' % value)
        def GigabitEthernet(self,value):
            H3C.ios.append('interface GigabitEthernet%s' % value)
        def description(self,value):
            H3C.ios.append('description %s' % value)
    def save(self):
        self.ios.append('save')

    def debug(self):
        # print(self.ios)
        print('\n'.join(self.ios))


class Switch(H3C):
    def __init__(self):
        pass


class Route(H3C):
    def __init__(self):
        pass


h3c = H3C()
h3c.system_view()
h3c.configure(h3c.TERMINAL)
h3c.Display.current('')
h3c.Interface().ethernet('1/0/3')
h3c.Interface().GigabitEthernet('1/0/21')
h3c.Interface().description('Wifi Network')
h3c.save()
h3c.debug()
