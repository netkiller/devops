import telnetlib
import time,string
class Terminal():
    def __init__(self):
        self.telnet = telnetlib.Telnet()
        self.screen = ''
    def connect(self,host,username,password):
        try:
            self.telnet.open(host,port=23)
        except:
            # logging.warning('%s网络连接失败'%host)
            return False
        self.telnet.read_until(b'Username:',timeout=1)
        self.telnet.write(username.encode('ascii') + b'\n')
        self.telnet.read_until(b'Password:',timeout=1)
        self.telnet.write(password.encode('ascii') + b'\n')
        time.sleep(1)
        screen = self.telnet.read_very_eager().decode('ascii')
        # print(screen)
        if '<MSR2610>' not in screen:
            # logging.warning('%s登录成功'%host)
            return True
        else:
            # logging.warning('%s登录失败，用户名或密码错误'%host)
            return False

    def command(self,command):
        self.telnet.write(command.encode('ascii')+b'\n')
        time.sleep(2)
        screen = self.telnet.read_very_eager().decode('ascii')
        print(screen)
        # logging.warning('命令执行结果：\n%s' % command_result)
    def more(self,command):
        self.telnet.write(command.encode('ascii'))
        time.sleep(0.5)
        current = self.telnet.read_very_eager().decode('ascii')
        print(current)
        if current :
            self.screen += current
        if current.find('---- More ----') :
            print('*' * 50)
            self.more(string.whitespace)

        print(self.screen)
        
        

    def logout(self):
        self.telnet.write(b"exit\n")

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
# h3c.system_view()
# h3c.configure(h3c.TERMINAL)
h3c.Display.current('')
# h3c.Interface().ethernet('1/0/3')
# h3c.Interface().GigabitEthernet('1/0/21')
# h3c.Interface().description('Wifi Network')
# h3c.save()
h3c.debug()

terminal = Terminal()
terminal.connect('192.168.30.1','admin','admin')
# terminal.command('display current-configuration')
terminal.more('display current-configuration\n')