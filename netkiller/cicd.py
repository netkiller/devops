#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-24
##############################################
import sys
sys.path.insert(0, '/Users/neo/workspace/Github/devops')
sys.path.insert(1, '../devops')
try:
    from netkiller.kubernetes import *
    from netkiller.git import *
    from netkiller.pipeline import *
    from datetime import datetime
    from optparse import OptionParser, OptionGroup
    from string import Template
    import logging
    # import logging.handlers
    from logging import basicConfig
except ImportError as err:
    print("Error: %s" % (err))


class CICD:

    basedir = os.getcwd()
    skip = []
    template = {}

    def __init__(self) -> None:

        self.parser = OptionParser("usage: %prog [options] <project>")
        self.parser.add_option("-n",
                               "--namespace",
                               dest="namespace",
                               help="命名空间",
                               default='dev',
                               metavar="dev")
        self.parser.add_option('-w',
                               '--workspace',
                               dest='workspace',
                               help='工作空间',
                               default='/var/tmp/workspace',
                               metavar='/var/tmp/workspace')
        self.parser.add_option('-r',
                               '--registry',
                               dest='registry',
                               help='容器镜像库',
                               default=None,
                               metavar='docker.io/netkiller')
        self.parser.add_option('-u',
                               '--username',
                               dest='username',
                               default=None,
                               metavar='',
                               help='用户名')
        self.parser.add_option('-p',
                               '--password',
                               dest='password',
                               default=None,
                               metavar='',
                               help='密码')
        self.parser.add_option("-b",
                               "--branch",
                               dest="branch",
                               help="分支",
                               default='master',
                               metavar="master")
        self.parser.add_option("-g",
                               "--group",
                               dest="group",
                               help="部署组",
                               default=None,
                               metavar='')
        self.parser.add_option('',
                               "--skip",
                               dest="skip",
                               help="跳过步骤",
                               default=None,
                               metavar="build|image|nacos|deploy")
        self.parser.add_option('',
                               "--logfile",
                               dest="logfile",
                               help="日志文件",
                               default='/tmp/debug.log',
                               metavar="/tmp/debug.log")
        self.parser.add_option('-l',
                               "--list",
                               action='store_true',
                               dest="list",
                               help="项目列表")
        self.parser.add_option('-a',
                               "--all",
                               action='store_true',
                               dest="all",
                               default=True,
                               help="部署所有项目")
        self.parser.add_option('-c',
                               "--clean",
                               action='store_true',
                               dest="clean",
                               help="清理构建环境")
        self.parser.add_option('-s',
                               '--silent',
                               action='store_true',
                               dest="silent",
                               default=False,
                               help="安静模式")
        self.parser.add_option('',
                               "--destroy",
                               action='store_true',
                               dest="destroy",
                               help="销毁环境")
        self.parser.add_option('-d',
                               "--daemon",
                               action='store_true',
                               dest="daemon",
                               help="后台运行")
        self.parser.add_option('',
                               "--debug",
                               action='store_true',
                               dest="debug",
                               help="debug mode")
        (self.options, self.args) = self.parser.parse_args()

        self.logging = logging.getLogger()
        if self.options.debug:
            logging.basicConfig(level=logging.NOTSET, format='[%(levelname)-5s] %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S', filename=None, filemode='a')
        else:
            logging.basicConfig(level=logging.NOTSET, format='%(asctime)s [%(levelname)-5s] %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S', filename=self.options.logfile, filemode='a')

    def usage(self):
        self.parser.print_help()
        print(
            "\nHomepage: https://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>"
        )
        print(
            "Help: https://github.com/netkiller/devops/blob/master/doc/index.md"
        )
        exit()

    def list(self):
        lists = {}
        for name, item in self.config.items():
            if not item['deployment']['group'] in lists:
                lists[item['deployment']['group']] = []
            lists[item['deployment']['group']].append(name)
        print("组\t项目")
        print("=" * 50)
        for group, projects in lists.items():
            print("{}:".format(group))
            for project in projects:
                print("\t{}".format(project))
        exit()

    def build(self, name):

        if not name in self.config.keys():
            print("%s 项目不存在" % name)
            return
        # else:
            # print("==================== {} ====================".format(name))
        project = self.config[name]

        ci = project['ci']
        module = None
        if 'module' in ci:
            module = ci['module']

        time = datetime.now().strftime('%Y%m%d-%H%M')
        registry = self.registry+'/' + self.namespace
        image = registry + '/' + name + ':' + time
        tag = time

        # package = ['mvn -U -T 1C clean package']
        # package = 'mvn -U -T 1C clean package -Dautoconfig.skip=true -Dmaven.test.skip=true -Dmaven.test.failure.ignore=true'
        package = ci['build']
        # package = ['ls']

        dataid = project['deployment']['name']
        group = 'DEFAULT_GROUP'
        template = self.basedir + '/template/' + \
            group + '/' + project['deployment']['name']
        filepath = self.basedir + '/nacos/' + group + '/' + project[
            'deployment']['name']

        deploy = []
        deploy.append(
            "kubectl set image deployment/{project} {project}={image} -n {namespace}"
            .format(project=name, image=image, namespace=self.namespace))
        deploy.append(
            "kubectl -n {namespace} get deployment/{project} -o wide".format(
                namespace=self.namespace, project=name))
        deploy.append(
            "kubectl -n {namespace} get pod -o wide | grep {project}".format(
                project=name, namespace=self.namespace))
        try:
            pipeline = Pipeline(self.workspace, self.logging)
            pipeline.image('docker.io/netkiller/maven:3-openjdk-18')
            # pipeline.env('JAVA_HOME','/Library/Java/JavaVirtualMachines/jdk1.8.0_341.jdk/Contents/Home')
            pipeline.env(
                'JAVA_HOME',
                '/Users/neo/Library/Java/JavaVirtualMachines/corretto-1.8.0_362/Contents/Home'
            )
            # self.pipeline.env('KUBECONFIG','/Users/neo/workspace/ops/k3s.yaml')
            pipeline.env('KUBECONFIG', '/root/ops/k3s.yaml')
            # ["docker images | grep none | awk '{ print $3; }' | xargs docker rmi"]
            # self.pipeline.begin(name).init(['alias docker=podman']).checkout(ci['url'],self.branch).build(package).podman(registry).dockerfile(tag=tag, dir=module).deploy(deploy).startup(['ls']).end().debug()
            pipeline.begin(name).init(['alias docker=podman'])
            if not 'build' in self.skip:
                pipeline.checkout(ci['url'], self.branch).build(package)
            if not 'image' in self.skip:
                pipeline.docker(registry).dockerfile(tag=tag, dir=module)
            if not 'nacos' in self.skip:
                if self.template:
                    pipeline.template(template, self.template, filepath)
                if os.path.exists(filepath):
                    pipeline.nacos(self.nacos['server'], self.nacos['username'], self.nacos['password'], self.namespace,
                                   dataid, group, filepath)
            if not 'deploy' in self.skip:
                pipeline.deploy(deploy)
            # .startup(['ls'])
            if self.options.silent:
                pipeline.log(
                    '{workspace}/{project}.log'.format(workspace=self.workspace, project=name))
            pipeline.end()
            # pipeline.debug()
            # print(project)
        except Exception as err:
            print(err)
        exit()

    def config(self, cfg):
        self.config = cfg

    def registry(self, url):
        self.registry = url

    def nacos(self, server, username, password):
        self.nacos = {}
        self.nacos['server'] = server
        self.nacos['username'] = username
        self.nacos['password'] = password

    def template(self, map):
        self.template = map

    def test(self, x):
        return x*x

    def group(self, name):
        projects = []
        for project, item in self.config.items():
            if item['deployment']['group'] == name:
                projects.append(project)

        # for project in projects:
            # self.build(project)

        from multiprocessing import Pool
        with Pool(5) as p:
            self.logging.info(p.map(self.build, projects))
    def all(self):
        projects = self.config.keys()
        from multiprocessing import Pool
        with Pool(10) as pool:
            for name, item in self.config.items():
                self.logging.info(pool.map(self.build, projects))

    def daemon(self):
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    def main(self):
        (options, args) = self.parser.parse_args()
        if options.debug:
            self.logging.debug("options: %s" % options)
            self.logging.debug("args: %s" % args)
        if options.namespace:
            self.namespace = options.namespace

        if options.destroy:
            user_input = input(
                "你确认要销毁 {namespace} 环境吗？请输入(yes/no): ".format(namespace=self.namespace)).lower()
            if user_input == 'yes':
                cmd = "kubectl delete namespace {namespace}".format(
                    namespace=self.namespace)
                os.system(cmd)
            exit()

        if options.workspace:
            self.workspace = options.workspace
        if options.branch:
            self.branch = options.branch
        if options.username and options.password:
            cmd = "docker login -u {username} -p{password} {registry}".format(
                username=options.username,
                password=options.password,
                registry=options.registry)
            os.system(cmd)
        if options.list:
            self.list()
        if options.all:
            if options.daemon:
                self.daemon()
            self.all()
            exit()
        if options.group:
            if options.daemon:
                self.daemon()
            self.group(options.group)
            exit()

        if args:
            if options.daemon:
                self.daemon()
            if options.skip:
                self.skip = options.skip.split(',')
            for project in args:
                if options.clean and os.path.exists(self.workspace + '/' +
                                                    project):
                    os.removedirs(self.workspace + '/' + project)
                self.build(project)

        self.usage()
