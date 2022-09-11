import os,sys
import subprocess
from datetime import datetime
sys.path.insert(0, '/Users/neo/workspace/devops')

from netkiller.kubernetes import *
from netkiller.git import *
class Pipeline:
	Maven = 'maven'
	Npm = 'npm'
	Cnpm = 'cnpm'
	Yarn = 'yarn'
	Gradle = 'gradle'
	def __init__(self, workspace):
		self.workspace = workspace
		self.pipelines = {}
		os.chdir(self.workspace)
		pass
	def begin(self, project):
		self.project = project
		# os.chdir(project)
		self.pipelines['begin'] = ['pwd']
		return self
	def env(self, key,value):
		os.putenv(key,value)
		return self
	def init(self):
		self.pipelines['init'] = []
		return self
	def checkout(self, url, branch):
		# self.pipelines['checkout'] = []
		git = Git(self.workspace)
		if os.path.exists(self.project)	:
			os.chdir(self.project)
			git.fetch().checkout(branch).pull().execute()
		else:
			git.option('--branch ' +branch)
			git.clone(url, self.project).execute()
			os.chdir(self.project)
		return self
	def build(self, script):
		# if compiler == self.Maven :
		#     self.pipelines['build'] = ['maven clean package']
		# elif compiler == self.Npm :
		#     self.pipelines['build'] = ['npm install']
		if script :
			self.pipelines['build'] = script
		return self
	def package(self, script):
		self.pipelines['package'] = script
		return self
	def test(self, script):
		self.pipelines['test'] = script
		return self
	def dockerfile(self, registry = None, tag=None):
		if registry :
			image = registry+'/'+self.project
		else:
			image = self.project

		if tag :
			tag = image+':'+ tag
		else:
			tag = image+':'+ datetime.now().strftime('%Y%m%d-%H%M')
		
		self.pipelines['dockerfile']=[]
		self.pipelines['dockerfile'].append('docker build -t '+tag+' .')
		self.pipelines['dockerfile'].append('docker tag '+tag+' '+image)
		self.pipelines['dockerfile'].append('docker push '+tag)
		self.pipelines['dockerfile'].append('docker push '+image)
		return self
	def deploy(self, script):
		self.pipelines['deploy'] = script
		return self
	def startup(self, script):
		self.pipelines['startup'] = script
		return self
	def end(self):
		print(self.pipelines)
		self.pipelines['end'] = []
		for stage in ['init','build','dockerfile','deploy','startup','end'] :
			if stage in self.pipelines.keys() :
				for command in self.pipelines[stage] :
					# print(command)
					# for cmd in commands :
					rev = subprocess.call(command,shell=True)					
					print("command %s, %s" % (command, rev))
					# if rev != 0 :
						# raise Exception("{} 执行失败".format(command))

		return self.pipelines

