#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-09
##############################################

from netkiller.git import *
from netkiller.kubernetes import *
import os
import sys
import tempfile
import subprocess
from datetime import datetime
from string import Template
sys.path.insert(0, '/Users/neo/workspace/devops')
sys.path.insert(0, '../devops')


class Stage:
    def __init__(self) -> None:
        pass


class Pipeline:
    Maven = 'maven'
    Npm = 'npm'
    Cnpm = 'cnpm'
    Yarn = 'yarn'
    Gradle = 'gradle'
    logfile = None
    image = None

    def __init__(self, workspace, logging):
        self.container = 'docker'
        self.registry = None
        self.image = None
        self.workspace = workspace
        self.logging = logging
        self.pipelines = {}
        if not os.path.exists(self.workspace):
            os.mkdir(self.workspace)
            self.logging.info("make directory: {}".format(self.workspace))

    # def image(self, name):
    #     self.image = name
    #     self.logging.info("image: {}".format(self.image))
    #     return self

    def begin(self, project):
        self.logging.info("%s %s %s" % ("="*20, project, "=" * 20))
        self.pipelines = {}
        os.chdir(self.workspace)
        self.project = project
        # os.chdir(project)
        self.pipelines['begin'] = []
        self.logging.info("change directory: {}".format(self.workspace))
        return self

    def env(self, key, value):
        os.putenv(key, value)
        # os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_341.jdk/Contents/Home'
        self.logging.info("env: %s = %s" % (key, value))
        return self

    def init(self, script):
        self.pipelines['init'] = script
        self.logging.info("init: %s" % script)
        return self

    def checkout(self, url, branch):
        self.logging.info("checkout: %s, branch: %s" % (url, branch))
        if os.path.exists(self.project):
            git = Git(os.path.join(self.workspace, self.project), self.logging)
            git.fetch().checkout(branch).pull().execute()
        else:
            git = Git(self.workspace, self.logging)
            git.option('--branch ' + branch)
            git.clone(url, self.project).execute()
            os.chdir(self.project)
        self.pipelines['checkout'] = ['ls']
        return self

    def build(self, script, image=None):
        #
        # if compiler == self.Maven :
        #     self.pipelines['build'] = ['maven clean package']
        # elif compiler == self.Npm :
        #     self.pipelines['build'] = ['npm install']
        if image:
            self.logging.info("image: {}".format(self.image))
            self.image = image

        if script:
            if self.image:
                scripts = []
                scripts.append('#!/bin/bash')
                scripts.extend(script)
                tmp = tempfile.NamedTemporaryFile(
                    mode='w+', delete=False)
                # suffix='.sh', prefix='tmp', dir=self.workspace
                tmp.writelines([line+'\n' for line in scripts])
                tmp.close()

                command = "{container} run -it --rm --name pipeline -v ~/.m2:/root/.m2 -v ~/.gradle:/root/.gradle -v {project}:/root/project -v {script}:/root/script.sh -w /root/project {image} /bin/sh /root/script.sh".format(
                    container=self.container, project=self.workspace+'/'+self.project, image=self.image, script=tmp.name)

                # print(command)
                self.pipelines['build'] = []
                self.pipelines['build'].append(command)
                self.logging.info("build: %s" % command)

            else:
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

    def docker(self, registry, username=None, password=None):
        self.pipelines['container'] = []
        self.registry = registry
        self.container = 'docker'
        if username:
            self.pipelines['container'].append(self.container + " login -u {username} -p{password} {registry}".format(
                username=username, password=password, registry=self.registry))
            self.logging.info("%s: %s, %s, %s" %
                              (self.container, registry, username, password))
        self.logging.info("container: %s" % self.container)
        return self

    def podman(self, registry, username=None, password=None):
        self.pipelines['container'] = []
        self.registry = registry
        self.container = 'podman'
        if username:
            self.pipelines['container'].append(self.container + " login -u {username} -p{password} {registry}".format(
                username=username, password=password, registry=self.registry))
            self.logging.info("%s: %s, %s, %s" %
                              (self.container, registry, username, password))
        self.logging.info("container: %s" % self.container)
        return self

    def dockerfile(self, tag=None, dir=None, latest=False):
        self.pipelines['dockerfile'] = []
        if self.registry:
            image = os.path.join(self.registry, self.project)
        else:
            image = self.project

        if tag:
            tag = image+':' + tag
        else:
            tag = image+':' + datetime.now().strftime('%Y%m%d-%H%M')

        if dir:
            os.chdir(dir)

        self.pipelines['dockerfile'].append(self.container + ' build -t '+tag+' .')
        self.pipelines['dockerfile'].append(self.container + ' push '+tag)
        self.pipelines['dockerfile'].append(self.container + ' image rm '+tag)

        if latest :
            self.pipelines['dockerfile'].append(self.container + ' tag '+tag+' '+image+':latest')
            self.pipelines['dockerfile'].append(self.container + ' push '+image+':latest')
            self.pipelines['dockerfile'].append(self.container + ' image rm '+image+':latest')

        self.logging.info("dockerfile: %s" % self.pipelines['dockerfile'])
        return self

    def template(self, tpl, variable, filepath):
        if os.path.exists(tpl):
            file = open(tpl, 'r')
            temp = Template(file.read())
            file.close()

            file = open(filepath, 'w')
            file.write(temp.safe_substitute(variable))
            file.close()
            self.logging.info("template: %s, %s, %s" %
                              (tpl, variable, filepath))
        return self

    def nacos(self, server, username, password, namespace, dataid, group, filepath):
        self.pipelines['nacos'] = []
        self.pipelines['nacos'].append("nacos -s {server} -u {username} -p {password} -n {namespace} -d {dataid} -g {group} --push -f {filepath}".format(
            server=server, username=username, password=password, namespace=namespace, dataid=dataid, group=group, filepath=filepath))
        # self.pipelines['nacos'].append("nacos -s {server} -u {username} -p {password} -n {namespace} -d {dataid} --show".format(
        #     server=server, username=username, password=password, namespace=namespace, dataid=dataid))
        self.logging.info("nacos: %s, %s, %s, %s, %s, %s, %s" % (
                          server, username, password, namespace, dataid, group, filepath))
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

    def log(self, file):
        self.logfile = file
        self.logging.info("logfile: %s" % file)
        return self

    def end(self, script=None):

        if self.logfile:
            stdout = open(self.logfile, 'w+')
        else:
            stdout = None

        if script:
            self.pipelines['end'] = script
            self.logging.info("end: %s" % self.pipelines['end'])

        self.logging.info("-"*50)
        try:
            for stage in ['begin', 'init', 'checkout', 'build', 'container', 'dockerfile', 'nacos', 'deploy', 'stop', 'startup', 'end']:
                if stage in self.pipelines.keys():
                    for command in self.pipelines[stage]:
                        rev = subprocess.call(
                            command, shell=True, stdout=stdout, stderr=stdout)
                        # rev = subprocess.call(command, shell=True,executable='/bin/bash', env=dict(ENV='/User/neo/.zprofile'))
                        self.logging.info(
                            "command: %s, status: %s" % (command, rev))
                        if rev != 0:
                            raise Exception("{} 执行失败".format(command))
        except KeyboardInterrupt as e:
            self.logging.info(e)
        self.logging.info("="*50)
        return self

    def debug(self):
        self.logging.debug(self.pipelines)
        return self
