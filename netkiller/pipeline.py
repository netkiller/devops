from netkiller.git import *
from netkiller.kubernetes import *
import os
import sys
import subprocess
from datetime import datetime
import logging
import logging.handlers
from logging import basicConfig
sys.path.insert(0, '/Users/neo/workspace/devops')


class Pipeline:
    Maven = 'maven'
    Npm = 'npm'
    Cnpm = 'cnpm'
    Yarn = 'yarn'
    Gradle = 'gradle'

    def __init__(self, workspace, logfile = 'debug.log'):
        self.workspace = workspace
        self.pipelines = {}
        if not os.path.exists(self.workspace) :
            os.mkdir(self.workspace)
        self.logging = logging.getLogger()
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', filename=logfile, filemode='a')

    def begin(self, project):
        self.logging.info("%s %s %s" % ("="*20, project, "=" * 20))
        self.pipelines = {}
        os.chdir(self.workspace)
        self.project = project
        # os.chdir(project)
        self.pipelines['begin'] = []
        return self

    def env(self, key, value):
        os.putenv(key, value)
        self.logging.info("%s = %s" % (key,value))
        return self

    def init(self, script):
        self.pipelines['init'] = script
        self.logging.info("init: %s" % script)
        return self

    def checkout(self, url, branch):
        self.logging.info("%s = %s" % (url,branch))
        if os.path.exists(self.project):
            git = Git(os.path.join(self.workspace,self.project), self.logging)
            git.fetch().checkout(branch).pull().execute()
        else:
            git = Git(self.workspace, self.logging)
            git.option('--branch ' + branch)
            git.clone(url, self.project).execute()
            os.chdir(self.project)
        self.pipelines['checkout'] = ['pwd','ls']
        return self
    def build(self, script):
        # 
        # if compiler == self.Maven :
        #     self.pipelines['build'] = ['maven clean package']
        # elif compiler == self.Npm :
        #     self.pipelines['build'] = ['npm install']
        if script:
            self.pipelines['build'] = script
        self.logging.info("build: %s" % script)
        return self

    def package(self, script):
        self.pipelines['package'] = script
        self.logging.info("package: %s" % script)
        return self

    def test(self, script):
        self.pipelines['test'] = script
        self.logging.info("test: %s" % script)
        return self

    def dockerfile(self, registry=None, tag=None, dir=None):
        self.pipelines['dockerfile'] = []
        if registry:
            image = os.path.join(registry,self.project)
        else:
            image = self.project

        if tag:
            tag = image+':' + tag
        else:
            tag = image+':' + datetime.now().strftime('%Y%m%d-%H%M')

        if dir :
            os.chdir(dir)
            
        self.pipelines['dockerfile'].append('docker build -t '+tag+' .')
        self.pipelines['dockerfile'].append('docker tag '+tag+' '+image)
        self.pipelines['dockerfile'].append('docker push '+tag)
        self.pipelines['dockerfile'].append('docker push '+image)
        self.pipelines['dockerfile'].append('docker image rm '+tag)
        self.pipelines['dockerfile'].append('docker image rm '+image)
        self.logging.info("dockerfile: %s" % self.pipelines['dockerfile'])
        return self

    def deploy(self, script):
        self.pipelines['deploy'] = script
        self.logging.info("deploy: %s" % script)
        return self

    def startup(self, script):
        self.pipelines['startup'] = script
        self.logging.info("startup: %s" % script)
        return self
    def stop(self, script):
        self.pipelines['stop'] = script
        self.logging.info("stop: %s" % script)
        return self
    def end(self, script=None):
        if script:
            self.pipelines['end'] = script
        try:
            for stage in ['begin','init', 'checkout', 'build', 'dockerfile', 'deploy', 'stop', 'startup', 'end']:
                if stage in self.pipelines.keys():
                    for command in self.pipelines[stage]:
                        rev = subprocess.call(command, shell=True)
                        if rev == 0 :
                            status = 'done'
                        else:
                            status = 'error'
                        self.logging.info("command: %s, %s, status: %s" % (rev, command,status))
                        # if rev != 0 :
                        # raise Exception("{} 执行失败".format(command))
        except KeyboardInterrupt as e:
            self.logging.info(e)
        self.logging.info("="*50)
        return self

    def debug(self):
        print(self.pipelines)
        return self
