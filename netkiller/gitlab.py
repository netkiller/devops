###################################
# GitLab CI/CD Pipeline compose
# Author: netkiller@msn.com
# Home:	http://www.netkiller.cn
###################################
#-*- coding: utf-8 -*-
import os,time,sys
import logging, logging.handlers
from configparser import ConfigParser
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString as pss

class GitLab:
	def __init__(self):
		super().__init__()
		# self.config = ConfigParser()
		self.logging = logging.getLogger()
		self.gitlabci = {}
		self.yaml = YAML()
		self.gitlabci['stage'] = []
	def image(self, img):
		self.gitlabci['image'] = img
		return self
	def cache(self, cch):
		self.gitlabci['cache'] = cch.cache
		return self
	def stages(self, stage):
		self.gitlabci['stage'].append(stage.job[stage.name]['stage'])
		self.gitlabci[stage.name] = stage.job
		return self
	def variables(self, value):
		self.gitlabci['variables'] = value
	def print(self):
		print(self.gitlabci)
	def dump(self):
		return (self.yaml.dump(self.gitlabci, sys.stdout))

class Cache(GitLab):
	def __init__(self):
		super().__init__()
		self.cache = {}
	def paths(self, obj):
		self.cache['paths'] = []
		if type(obj) == str:
			self.cache['paths'].append(obj)
		elif type(obj) == list:
			self.cache['paths'].extend(obj)
		return self
	def key(self, key):
		self.cache['key'] = key
		return self
	def untracked(self,value):
		self.cache['untracked'] = value
		return self

class Job(GitLab):
	def __init__(self, job):
		super().__init__()
		# umask = os.umask(0o077)
		self.name = job
		self.job = {}
		self.job[self.name] = {}
	def stage(self, value):
		self.job[self.name]['stage'] = value
		return self
	def image(self, value):
		self.job[self.name]['image'] = value
		return self
	def variables(self, value):
		self.job[self.name]['variables'] = value
		return self
	def tags(self,tag):
		self.job[self.name]['tags'] = tag
		return self
	def artifacts(self, artifact):
		self.job[self.name]['artifacts'] = artifact
		return self	
	def debug(self):
		print(self.job)
	def environment(self, env):
		self.job[self.name]['environment'] = env
		return self
	def only(self, branch):
		self.job[self.name]['only'] = branch
		return self
	def excepts(self, branch):
		self.job[self.name]['except'] = branch
		return self
	def before_script(self, cmd):
		self.job[self.name]['before_script'] = cmd
		return self
	def script(self, cmd):
		self.job[self.name]['script'] = cmd
		return self
	def after_script(self, cmd):
		self.job[self.name]['after_script'] = cmd
		return self
	def when(self, value):
		self.job[self.name]['when'] = value
		return self
	def allow_failure(self, logfile):
		self.job[self.name]['allow_failure'] = value
		return self


class Stages(GitLab):
	def result_file(self, name):
		self.opts.append('--result-file='+name)
		return self
	def set_gtid_purged(self, value =  'OFF'):
		self.opts.append('--set-gtid-purged='+value)
		return self
	def default_character_set(self, value =  'utf8'):
		self.opts.append('--default-character-set='+value)
		return self	
	def cnf(self, clean = False):
		path = os.path.expanduser('~/.my.cnf')
		config = ConfigParser()
		if clean and os.path.exists(path):
			os.remove(path)
			exit()
		config['mysqldump'] = {
			'user': self.username,
			'password': self.password
		}
		config['mysql'] = {
			'user': self.username,
			'password': self.password
		}
		with open(path, 'w') as file:
			config.write(file)
		# self.opts.append('--defaults-file={0}'.format(path))
		# self.opts.append('--defaults-extra-file={0}'.format(path))
		return self
	def delete(self, day = None):
		if day :
			self.copies = day
		if self.copies :
			command = "find {directory} -type f -mtime +{copies} -delete".format(directory=self.directory, copies=self.copies)
			self.logging.debug(command)
			os.system(command)
	def Gzip(self):
		self.gpg = None
		self.gzip = True
	def GnuPG(self, recipient):
		self.gzip = False
		self.gpg = recipient
	def __command(self):
		cmd = []
		cmd.append('/usr/bin/mysqldump')
		opts = ' '.join(self.opts)
		cmd.append(opts)

		timepoint = time.strftime('%Y-%m-%d.%H:%M:%S',time.localtime(time.time()))
		output = self.directory + '/' + self.database.replace(' ','_') +'.' + timepoint

		if self.gzip :
			cmd.append('| gzip >')
			output += '.sql.gz'
			cmd.append(output)
		elif self.gpg :
			cmd.append('| gpg -r {userid} -e -o {output}.sql.gpg'.format(userid=self.gpg, output=output) )
			ext = '.sql.gpg'
		else:
			cmd.append('>')
			output += '.sql'
			cmd.append(output)

		command = ' '.join(cmd) 
		return command
	def execute(self):
		command = self.__command()
		self.logging.debug(command)
		os.system(command)
	
cache = Cache()
cache.paths('node_modules').untracked(True)

job = Job('deploy-job')
job.image('maven:3.6-jdk-11')
job.stage('deploy')
job.variables({'GIT_STRATEGY': 'none'})
job.environment({'name':'production','url':'http://www.netkiller.cn'})
job.only(['production','testing','development']).excepts(['feature','hotfix'])
job.tags(['shell'])
job.before_script(['ls -l','find .','echo "Helloworld"']).script(['touch test.txt','echo Hello > test.txt']).after_script(['echo "OK"'])
job.artifacts({'name':'$CI_PROJECT_NAME','paths':'./target/*.jar'})
job.when('manual')
job.debug()

gitlab = GitLab()
gitlab.image('maven:3.5.0-jdk-8')
gitlab.cache(cache)
gitlab.variables({'MAVEN_OPTS':'-Dmaven.repo.local=.m2/repository'})
gitlab.stages(job)
gitlab.print()
print(gitlab.dump())