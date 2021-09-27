import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0,module)

from netkiller.wework import *

cfgfile = '/tmp/wework.ini'

wework = WeWork(cfgfile)

