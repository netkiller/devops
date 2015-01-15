#-*- coding: utf-8 -*-
import os, sys
class Rsync():
	def __init__(self, mode=None): 
		self.mode = mode
		self.cmd = {}
		self.opt = []
	def option(self, opt):
		self.opt.append(opt)
	def delete(self):
		self.opt.append('--delete')
	def backup(self, dir):
		self.opt.append('--backup --backup-dir='+dir)
	def logfile(self, log):
		self.opt.append('--log-file='+log)
	def exclude(self,exc):
		if exc.find('/') or exc.find('.'):
			self.opt.append('--exclude-from='+exc)
		else:
			self.opt.append('--exclude='+exc)
	def include(self,exc):
		if exc.find('/') or exc.find('.'):
			self.opt.append('--include-from='+exc)
		else:
			self.opt.append('--include='+exc)
	def password(self, file):
		self.opt.append('--password-file='+file)	
	def source(self,src):
		self.cmd['src'] = src
	def destination(self,dest):
		self.cmd['dest'] = dest
	def execute(self):
		os.system(self.__to_string())
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