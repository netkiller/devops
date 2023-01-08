#-*- coding: utf-8 -*-
import os

class Command():
    options = []
    image = ""
    podman = "podman"

    def __init__(self):
        pass


class Machine(Command):
    commands = []
    command = 'machine'
    options = {}

    def __init__(self, options=None):
        pass

    def init(self):
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='init'))
        help = 'Initialize a virtual machine'
        # print(self.commands)
        return self

    def inspect(self):
        help = 'Inspect an existing machine'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='inspect'))
        return self

    def list(self):
        help = 'List machines'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='list'))
        return self

    def rm(self):
        help = 'Remove an existing machine'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='rm'))
        return self

    def set(self):
        help = 'Sets a virtual machine setting'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='set'))
        return self

    def ssh(self):
        help = 'SSH into an existing machine'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='ssh'))
        return self

    def start(self):
        help = 'Start an existing machine'
        self.commands.append("{podman} {command} {cmd}".format(
            podman=self.podman, command=self.command, cmd='start'))
        return self

    def stop(self, switch=True):
        help = 'Stop an existing machine'
        if switch:
            self.commands.append("{podman} {command} {cmd}".format(
                podman=self.podman, command=self.command, cmd='stop'))
        return self

    def execute(self):
        for command in self.commands:
            os.system(command)

    def debug(self):
        for command in self.commands:
            print(command)
        return self

class Run(Command):
    command = 'run'

    def __init__(self, options=None):
        self.options = options

    def rm(self):
        self.options.append("--rm")
        return self

    def detach(self):
        self.options.append("--detach")
        return self

    def image(self, value):
        self.image = value
        return self

    def network(self, value):
        self.options.append("--network={value}".format(value=value))
        return self

    def publish(self, value):
        self.options.append("--publish={value}".format(value=value))
        return self

    def volume(self, value):
        self.options.append("--volume={value}".format(value=value))
        return self

    def entrypoint(self, value):
        self.options.append("--entrypoint={value}".format(value=value))
        return self

    def name(self, value):
        self.options.append("--name={value}".format(value=value))
        return self

    def env(self, value):
        self.options.append("--env={value}".format(value=value))
        return self

    def cmdline(self):
        return "{podman} {command} {options} {image}".format(podman=self.podman, command=self.command, options=' '.join(self.options), image=self.image)

    def execute(self):
        os.system(self.cmdline())

    def debug(self):
        print(self.cmdline())
        return self


class Ps(Command):
    command = 'ps'

    def __init__(self, options=None):
        for option in options:
            self.options.append(option)
        pass

    def all(self):
        self.options.append("--all")
        return self

    def format(self, value):
        self.options.append('--format="{value}"'.format(value=value))
        return self

    def cmdline(self):
        return "{podman} {command} {options}".format(podman=self.podman, command=self.command, options=' '.join(self.options))

    def execute(self):
        os.system(self.cmdline())

    def debug(self):
        print(self.cmdline())
        return self


class Podman():
    machine = Machine()
    run = Run()

    def __init__(self, workspace=None, logger=None):
        pass

    class Machine(Machine):
        def __init__(self, options=None):
            super().__init__(options)
            pass

    class Run(Run):
        def __init__(self, options=None):
            super().__init__(options)

    class Ps(Ps):
        def __init__(self, options=None):
            super().__init__(options)


podman = Podman()
# podman.Machine().init()
# podman.machine.start().list().inspect().stop(False).debug().execute()
# podman.run.name('mysql').image('mysql:latest').network('host').publish('3306:3306').env('MYSQL_ROOT_PASSWORD=chen').volume('mysql:/var/lib/mysql:rw').volume('/etc/localtime:/etc/localtime:ro').detach().debug().execute()
podman.Machine().list().execute()
podman.Ps(options=['--no-trunc']).all().format(
    '{{.ID}}  {{.Image}}  {{.Labels}}  {{.Mounts}}').debug().execute()
podman.Machine().stop().execute()
