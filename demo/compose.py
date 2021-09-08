#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Upgrade: 2021-09-05
##############################################
try:
	import os,  sys
	# sys.path.append('/usr/local/lib/python3.9/site-packages')
	module_path = '/'.join(os.path.abspath(__file__).split('/')[:-3])
	print(module_path)
	sys.path.append(module_path)
	# for module in sys.modules:
	# 	print(module)
	from netkiller.docker.volumes import *
	# from netkiller.docker import Services
	# from netkiller import *
	# from netkiller.docker import *
	# from netkiller.docker import volumes
	# import netkiller
	

except ImportError as err:
	print("%s" %(err))

# from netkiller.docker.Volumes import Volumes


