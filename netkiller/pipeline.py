from netkiller.git import *
from netkiller.kubernetes import *
import os
import sys
import subprocess
from datetime import datetime
sys.path.insert(0, '/Users/neo/workspace/devops')


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

    def env(self, key, value):
        os.putenv(key, value)
        return self

    def init(self, script):
        self.pipelines['init'] = script
        return self

    def checkout(self, url, branch):
        if os.path.exists(self.project):
            git = Git(self.workspace+'/'+self.project)
            git.fetch().checkout(branch).pull().execute()
        else:
            git = Git(self.workspace)
            git.option('--branch ' + branch)
            git.clone(url, self.project).execute()
            os.chdir(self.project)
        os.system('pwd')
        self.pipelines['checkout'] = ['ls']
        return self
    def build(self, script):
        # 
        # if compiler == self.Maven :
        #     self.pipelines['build'] = ['maven clean package']
        # elif compiler == self.Npm :
        #     self.pipelines['build'] = ['npm install']
        if script:
            self.pipelines['build'] = script
        return self

    def package(self, script):
        self.pipelines['package'] = script
        return self

    def test(self, script):
        self.pipelines['test'] = script
        return self

    def dockerfile(self, registry=None, tag=None):
        if registry:
            image = registry+'/'+self.project
        else:
            image = self.project

        if tag:
            tag = image+':' + tag
        else:
            tag = image+':' + datetime.now().strftime('%Y%m%d-%H%M')

        self.pipelines['dockerfile'] = []
        self.pipelines['dockerfile'].append('docker build -t '+tag+' .')
        self.pipelines['dockerfile'].append('docker tag '+tag+' '+image)
        self.pipelines['dockerfile'].append('docker push '+tag)
        self.pipelines['dockerfile'].append('docker push '+image)
        self.pipelines['dockerfile'].append('docker image rm '+image)
        return self

    def deploy(self, script):
        self.pipelines['deploy'] = script
        return self

    def startup(self, script):
        self.pipelines['startup'] = script
        return self

    def end(self, script=None):
        if script:
            self.pipelines['end'] = script
        for stage in ['init', 'checkout', 'build', 'dockerfile', 'deploy', 'startup', 'end']:
            if stage in self.pipelines.keys():
                for command in self.pipelines[stage]:
                    rev = subprocess.call(command, shell=True)
                    print("command: %s, %s" % (rev, command))
                    # if rev != 0 :
                    # raise Exception("{} 执行失败".format(command))
        return self

    def debug(self):
        print(self.pipelines)
        return self
