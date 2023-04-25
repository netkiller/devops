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
    env = {}
    workspace = os.path.expanduser("~/.netkiller/project")

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
                               default=self.workspace,
                               metavar=self.workspace)
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
                               help="跳过部署项目",
                               default=None,
                               metavar="project1,project2")
        self.parser.add_option('-o',
                               "--only",
                               dest="only",
                               help="指定步骤",
                               default=None,
                               metavar="checkout|build|images|nacos")
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
                               help="查看项目列表")
        self.parser.add_option('-a',
                               "--all",
                               action='store_true',
                               dest="all",
                               default=False,
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
                               "--parallel",
                               dest="parallel",
                               help="并行部署",
                               default=None,
                               metavar="5")
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

    def env(self, variable):
        self.env = variable

    def build(self, name):

        if not name in self.config.keys():
            print("%s 项目不存在" % name)
            self.logging.info("%s 项目不存在" % name)
            return
        # else:
            # print("==================== {} ====================".format(name))
        if name in self.skip:
            self.logging.info("skip ".format(name))
            return
        project = self.config[name]

        ci = project['ci']
        module = None
        if 'module' in ci:
            module = ci['module']

        tag = self.options.branch + '-' + datetime.now().strftime('%Y%m%d-%H%M')

        # package = ['mvn -U -T 1C clean package']
        # package = 'mvn -U -T 1C clean package -Dautoconfig.skip=true -Dmaven.test.skip=true -Dmaven.test.failure.ignore=true'
        package = ci['build']

        dataid = project['deployment']['name']
        group = 'DEFAULT_GROUP'
        template = self.basedir + '/template/' + \
            group + '/' + project['deployment']['name']
        filepath = self.basedir + '/nacos/' + group + '/' + project[
            'deployment']['name']

        image = self.registry + '/' + name + ':' + tag
        deploy = []
        deploy.append(
            "kubectl set image deployment/{project} {project}={image} -n {namespace}"
            .format(project=name, image=image, namespace=self.options.namespace))
        deploy.append(
            "kubectl -n {namespace} get deployment/{project} -o wide".format(
                namespace=self.options.namespace, project=name))
        deploy.append(
            "kubectl -n {namespace} get pod -o wide | grep {project}".format(
                project=name, namespace=self.options.namespace))

        image = None
        if 'image' in project['ci']:
            image = project['ci']['image']

        try:
            pipeline = Pipeline(self.options.workspace, self.logging)
            # pipeline.env('JAVA_HOME','/Library/Java/JavaVirtualMachines/jdk1.8.0_341.jdk/Contents/Home')
            # self.pipeline.env('KUBECONFIG','/Users/neo/workspace/ops/k3s.yaml')
            if self.env:
                for key, value in self.env.items():
                    pipeline.env(key, value)
            # pipeline.env('KUBECONFIG', '/root/ops/k3s.yaml')
            # ["docker images | grep none | awk '{ print $3; }' | xargs docker rmi"]
            # self.pipeline.begin(name).init(['alias docker=podman']).checkout(ci['url'],self.options.branch).build(package).podman(self.registry).dockerfile(tag=tag, dir=module).deploy(deploy).startup(['ls']).end().debug()
            pipeline.begin(name).init(
                ['alias docker=podman', 'echo $JAVA_HOME'])
            if self.options.silent:
                pipeline.log(
                    '{workspace}/{project}.log'.format(workspace=self.options.workspace, project=name))

            if self.options.only:
                if 'checkout' == self.options.only:
                    pipeline.checkout(ci['url'], self.options.branch)
                elif 'build' == self.options.only:
                    pipeline.build(package, image)
                elif 'image' == self.options.only:
                    pipeline.docker(self.registry).dockerfile(
                        tag=tag, dir=module, latest=True)
                elif 'nacos' == self.options.only:
                    if self.template:
                        pipeline.template(template, self.template, filepath)
                    if os.path.exists(filepath):
                        pipeline.nacos(self.nacos['server'], self.nacos['username'], self.nacos['password'], self.options.namespace,
                                       dataid, group, filepath)
                        pipeline.startup(
                            ['kubectl rollout restart deployment {project} -n {namespace} '.format(project=name, namespace=self.options.namespace)])
                pipeline.end()
                return

            pipeline.checkout(ci['url'], self.options.branch)
            pipeline.build(package, image)
            pipeline.docker(self.registry).dockerfile(tag=tag, dir=module)
            if self.template:
                pipeline.template(template, self.template, filepath)
                if os.path.exists(filepath):
                    pipeline.nacos(self.nacos['server'], self.nacos['username'], self.nacos['password'], self.options.namespace,
                                   dataid, group, filepath)

            pipeline.deploy(deploy)
            pipeline.end()
            # pipeline.debug()

        except Exception as err:
            print(err)

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

        if self.options.parallel:
            from multiprocessing import Pool
            with Pool(self.options.parallel) as p:
                self.logging.info(p.map(self.build, projects))
        else:
            for project in projects:
                self.build(project)

    def all(self):
        projects = self.config.keys()
        from multiprocessing import Pool
        with Pool(10) as pool:
            self.logging.info(pool.map(self.build, projects))

    def daemon(self):
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

    def main(self):

        if self.options.debug:
            self.logging.debug("options: %s" % self.options)
            self.logging.debug("args: %s" % self.args)

        if self.options.destroy:
            user_input = input(
                "你确认要销毁 {namespace} 环境吗？请输入(yes/no): ".format(namespace=self.options.namespace)).lower()
            if user_input == 'yes':
                cmd = "kubectl delete namespace {namespace}".format(
                    namespace=self.options.namespace)
                os.system(cmd)
            exit()

        if self.options.username and self.options.password:
            cmd = "docker login -u {username} -p{password} {registry}".format(
                username=self.options.username,
                password=self.options.password,
                registry=self.options.registry)
            os.system(cmd)
        if self.options.list:
            self.list()
        if self.options.all:
            if self.options.daemon:
                self.daemon()
            self.all()
            exit()
        if self.options.group:
            if self.options.daemon:
                self.daemon()
            self.group(self.options.group)
            exit()

        if self.args:
            if self.options.daemon:
                self.daemon()
            if self.options.skip:
                self.skip = self.options.skip.split(',')
            for project in self.args:
                if self.options.clean and os.path.exists(self.options.workspace + '/' +
                                                         project):
                    # os.removedirs(self.options.workspace + '/' + project)
                    os.system(
                        "rm -rf {}".format(self.options.workspace + '/' + project))
                self.build(project)
            exit()

        self.usage()
