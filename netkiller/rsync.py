#-*- coding: utf-8 -*-
import os, sys
class Rsync():
	def __init__(self, mode=None): 
		self.mode = mode
		self.cmd = {}
		self.opt = []
	def option(self, opt):
		self.opt.append(opt)
		return(self)
	def verbose(self):
		self.opt.append('--verbose')
		return(self)
	def quiet(self):
		self.opt.append('--quiet')
		return(self)
	def delete(self):
		self.opt.append('--delete')
		return(self)
	def update(self):
		self.opt.append('--update')
		return(self)
	def backup(self, dir):
		self.opt.append('--backup --backup-dir='+dir)
		return(self)
	def compress(self, num = None):
		self.opt.append("--compress")
		if num :
			self.opt.append("--compress-level={num}".format(num=num))
		return(self)
	def logfile(self, log):
		self.opt.append('--log-file='+log)
		return(self)
	def exclude(self,exc):
		if type(exc) == 'str':
			#exc.find('/') or exc.find('.')
			self.opt.append('--exclude-from='+exc)
		else:
			for item in exc :
				self.opt.append('--exclude='+item)
		return(self)
	def include(self,inc):
		if type(inc) == 'str':
			self.opt.append('--include-from='+inc)
		else:
			for item in inc :
				self.opt.append('--include='+item)
		return(self)
	def password(self, file):
		self.opt.append('--password-file='+file)
		return(self)
	def source(self,src):
		self.cmd['src'] = src
		return(self)
	def destination(self,dest):
		self.cmd['dest'] = dest
		return(self)
	def execute(self):
		rev = os.system(self.__to_string())
		return(rev)
	def __to_string(self):
		return('rsync '+' '.join(self.opt)+' '+self.cmd['src']+' '+ self.cmd['dest'])
	def debug(self):
		return(self.__to_string())

""" 
rsync = Rsync()
rsync.option('auzvP')
rsync.source('/etc/')
rsync.destination('/tmp')
rsync.execute()
"""