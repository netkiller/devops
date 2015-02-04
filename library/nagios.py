#!/usr/bin/python3
#-*- coding: utf-8 -*-
import os, sys
class Template():
	lines = []
	def __init__(self, lines, define): 
		self.lines = lines
		self.lines.append("define "+define+"{")
	def use(self,val):
		self.lines.append("\tuse\t\t\t"+val)
		return(self)
	def host_name(self,val):
		self.lines.append("\thost_name\t\t"+val)
		return(self)
	def alias(self,val):
		self.lines.append("\talias\t\t\t"+val)
		return(self)	
	def address(self,val):
		self.lines.append("\taddress\t\t\t"+val)
		return(self)
	def end(self):
		self.lines.append("}")
	def to_string(self):
		return("\n".join(self.lines))	
class Host(Template):
	lines = []
	def __init__(self): 
		super(Host, self).__init__(self.lines, 'host')
	def makeline(self):
		print(self.to_string())

class Service(Template):
	lines = []
	def __init__(self): 
		super(Service, self).__init__(self.lines, 'service')
	def service_description(self, val):
		self.lines.append("\tservice_description\t"+val)
		return(self)
	def check_command(self, val):
		self.lines.append("\tcheck_command\t\t"+val)
		return(self)
	def makeline(self):
		print(self.to_string())		
		
class Nagios():
	def __init__(self, mode=None): 
		self.mode = mode
		self.cmd = {}
		self.cfg = []
	def attach(self, obj):
		self.cfg.append(obj)
		return(self)

	def save(self, filename):
		with open(filename, 'w') as f:
			for obj in self.cfg:
				f.write(obj.to_string())
				f.write("\n")
			f.closed
	def makecfg(self):
		for obj in self.cfg:
			print(obj.to_string())
	def debug(self):
		pass


host = Host()
host.use('flexible-host').host_name('www.example.com').alias('www.example.com').address('192.168.2.1').end()
#host.makeline()

service = Service()
service.use('flexible-server').host_name('www.example.com').service_description('www.example.com').check_command('check_http').end()
#service.makeline()

nagios = Nagios()
nagios.attach(host)
nagios.attach(service)
nagios.makecfg()
nagios.save('/tmp/host.cfg')

""" 
define host{
	use			flexible-host
	host_name		www.example.com
	alias			www.example.com
	address			192.168.2.1
}
define service{
	use			flexible-server
	host_name		www.example.com
	service_description	www.example.com
	check_command		check_http
}
"""