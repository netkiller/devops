#-*- coding: utf-8 -*-
import os, sys
class Git():
	cmd = []
	def __init__(self, workspace = None, logging = None):
		self.logging = logging
		self.workspace = workspace
	def option(self, opt):
		if opt:
			self.opt = opt
	def clone(self, uri):
		if self.workspace :
			self.cmd.append('clone '+ uri +' '+ self.workspace)
		return(self)
	def pull(self):
		if self.workspace :
			os.chdir(self.workspace)		
		self.cmd.append('pull --progress')
		return(self)
	def reset(self):
		self.cmd.append('reset HEAD --hard')
		return(self)
	def branch(self, branchname=None, op=None):
		os.chdir(self.workspace)
		if branchname :
			if op == 'delete':
				self.cmd.append('branch -D '+branchname)
			elif op == 'new':
				self.cmd.append('checkout -fb '+branchname+' --')
			else:
				self.cmd.append('reset HEAD --hard')
				self.cmd.append('fetch origin')
				self.cmd.append('checkout -f '+branchname)
		else:
			self.cmd.append('branch')
		return(self)
	def merge(self, branchname):
		self.cmd.append('merge '+branchname)
		return(self)
	def tag(self, tagname):
		os.chdir(self.workspace)
		self.cmd.append('tag ' + tagname)
		return(self)
	def checkout(self, revision=None):
		os.chdir(self.workspace)
		if revision :
			self.cmd.append('checkout -f '+revision)
		return(self)
	def debug(self):
		cmd = ''
		for line in self.cmd:
			cmd += 'git ' + line + '; '
		return(cmd)
	def execute(self):
		for line in self.cmd:
			os.system('git '+ line)
			self.logging.debug('git '+ line)
		self.cmd = []
		print("-")