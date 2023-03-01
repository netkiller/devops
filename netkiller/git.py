#-*- coding: utf-8 -*-
import os, sys,logging
class Git():
	def __init__(self, workspace = None, logger = None):
		self.cmd = []
		self.opt = None
		if logger :
			self.logger = logger
		else:
			self.logger = logging.getLogger()
		self.workspace = os.path.expanduser(workspace)
		if os.path.exists(self.workspace) :
			os.chdir(self.workspace)
			self.logger.info('workspace %s' % self.workspace)
		else:
			self.logger.info("directory doesn't exist %s" % self.workspace)
			exit(0)
		
	def option(self, opt):
		if opt:
			self.opt = opt
	def clone(self, uri, project = None):
		if project :
			self.cmd.append('clone '+ self.opt +' '+ uri +' '+ project)
		else:
			self.cmd.append('clone '+ self.opt +' '+ uri)
		return(self)
	def clean(self, param=''):
		#git clean -df
		self.cmd.append('clean '+param)
		return(self)
	def init(self):
		if self.workspace :
			self.cmd.append('init')
		return(self)
	def add(self, path, param=''):
		self.cmd.append('add '+path+' '+param)
		return(self)
	def commit(self, msg = '', param=''):
		self.cmd.append('commit '+param+' -m "'+msg+'"')
		return(self)
	def checkout(self, branch):
		self.cmd.append('checkout {0}'.format(branch))
		return(self)
	def status(self):
		self.cmd.append('status')
		return(self)
	def log(self, opt = None):
		if opt :
			self.cmd.append('log '+ opt)
		else:
			self.cmd.append('log')
		return(self)
	def pull(self):
		# if self.workspace :
			# os.chdir(self.workspace)
		self.cmd.append('pull --progress')
		return(self)
	def fetch(self):
		self.cmd.append('fetch')
		return(self)	
	def push(self):
		self.cmd.append('push --progress')
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
	def reset(self):
		self.cmd.append('reset HEAD .')
		return(self)
	def command(self, cmd, argument):
		self.cmd.append('%s %s' %(cmd, argument))
	def debug(self):
		cmd = ''
		for line in self.cmd:
			cmd = 'git ' + line
			self.logger.debug(cmd)
		return(cmd)
	def execute(self):
		self.logger.info('execute directory %s' % os.getcwd())
		for line in self.cmd:
			rev = os.system('git '+ line)
			self.logger.debug('git '+ line)
			# self.logger.debug(rev)
			if rev == 256 :
				return rev
			# print("-")
		self.cmd = []
		
		return 0

class GitBranch(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def show(self):
		self.cmd.append('branch --show-current')
	def list(self, pattern = None):
		if pattern :
			self.cmd.append("branch --list '%s'" % pattern)
		else:
			self.cmd.append('branch -l')
	def create(self, name, origin = None):
		if origin :
			self.cmd.append('checkout -b %s origin/%s' % (name, origin))	
		else:
			self.cmd.append('branch %s ' % name)
	def delete(self, name):	
		self.cmd.append('branch --delete %s ' % name)
	def move(self, old, new):
		self.cmd.append('checkout %s' % old)
		self.cmd.append('branch -m "%s" "%s"' % (old, new))
		self.cmd.append('push --delete origin %s' % old)
		self.cmd.append('push origin %s' % new)
		pass

class GitMerge(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def source(self, name):
		self.src = name
		self.command('fetch','origin')
		self.command('checkout', name)
		self.command('branch', '--show-current')
		self.pull()
		return(self)
	def target(self, name):
		self.tgt = name
		self.command('fetch','origin')
		self.command('checkout', name)
		self.command('branch','--show-current')
		self.pull()
		return(self)
	def merge(self):
		self.command('merge','--no-ff "%s"' % self.src)
		return(self)
	def push(self):
		self.command('push','--set-upstream origin %s' % self.tgt)
		# self.cmd.append('push origin')
		return(self)

class GitCheckout(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def checkout(self, branch):
		self.command('checkout', branch)
		return(self)
	def force(self, revision=None):
		if revision :
			self.command('checkout -f',revision)
		return(self)

class GitReset(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def hard(self, ver = None):
		if ver :
			self.command('reset', '--hard %s --' % ver)
		else:
			self.command('reset', '--hard')
		return(self)
	def mixed(self, ver):
		self.command('reset', '--mixed %s --' % ver)
		return(self)
	def head(self):
		self.command('reset','HEAD --hard')
		return(self)	
	def push(self, force = False):
		if force :
			self.command('push', 'origin --force') #--all
		else:
			self.command('push', 'origin')
		return(self)
		# git push --force --progress "origin" master:master
			

class GitUtility(Git):
	def __init__():
		pass