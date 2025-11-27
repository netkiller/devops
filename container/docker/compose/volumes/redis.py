try:
    from netkiller.docker import *

    redis = Volumes("redis")
except ImportError as err:
    print("%s" % (err))
