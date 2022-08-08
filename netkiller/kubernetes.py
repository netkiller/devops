# -*- coding: utf-8 -*-
import os,uuid
from posixpath import split
import sys
import json
from optparse import OptionParser, OptionGroup
import logging
import logging.handlers
from logging import basicConfig
from numpy import array
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as lss, PreservedScalarString as pss
from io import StringIO
from base64 import b64encode


class Logging():
    def __init__(self):

        self.logging = logging.getLogger()

class Define():
    class restartPolicy():
        Always = 'Always'
    class strategy():
        RollingUpdate = 'RollingUpdate'
    class containers():
        class imagePullPolicy():
            IfNotPresent = 'IfNotPresent'
    class dnsPolicy():
        ClusterFirst = 'ClusterFirst'
    class Service():
        ClusterIP = 'ClusterIP'
        LoadBalancer = 'LoadBalancer'
        class externalTrafficPolicy:
            Local = 'Local'
            Cluster = 'Cluster'
    class Ingress():
        class pathType():
            Prefix = 'Prefix'
            ImplementationSpecific = 'ImplementationSpecific'
        

class Common():
    commons = {}

    def __init__(self):
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.commons = {}
        pass

    def apiVersion(self, version='v1'):
        self.commons['apiVersion'] = version

    def kind(self, value):
        self.commons['kind'] = value

    def dump(self, obj):
        options = {}
        stream = StringIO()
        self.yaml.dump(obj, stream, **options)
        output = stream.getvalue()
        stream.close()
        return output

    def save(self, filename, text=''):
        path = os.path.expanduser(filename)
        # if os.path.exists(path):
        # os.remove(path)
        with open(path, 'w') as file:
            file.write(text)


class Metadata:
    __metadata = {}

    def __init__(self):
        self.__metadata = {}
        pass

    def name(self, value):
        self.__metadata['name'] = value
        return self

    def namespace(self, value):
        self.__metadata['namespace'] = value
        return self

    def labels(self, value):
        self.__metadata['labels'] = value
        return self

    def annotations(self, value):
        self.__metadata['annotations'] = value
        return self

    def metadata(self):
        return(self.__metadata)

class Containers:
    container = {}

    def __init__(self):
        self.container = {}
        pass

    def name(self, value):
        self.container['name'] = value
        return self

    def image(self, value):
        self.container['image'] = value
        return self

    def command(self, value):
        self.container['command'] = []
        self.container['command'].extend(value)
        return self

    def args(self, value):
        self.container['args'] = value
        # self.container['args'].append(value)
        return self

    def volumeMounts(self, value):
        self.container['volumeMounts'] = value
        return self

    def imagePullPolicy(self, value):
        self.container['imagePullPolicy'] = value
        return self

    def ports(self, value):
        self.container['ports'] = value
        return self

    def stdin(self, value=True):
        self.container['stdin'] = value
        return self

    def env(self, value):
        self.container['env'] = []
        self.container['env'] = value
        return self

    def resources(self, value):
        self.container['resources'] = value
        return self

    def livenessProbe(self, value):
        self.container['livenessProbe'] = value
        return self
    def readinessProbe(self, value):
        self.container['readinessProbe'] = value
        return self

class Volumes(Common):
    volumes = {}

    def __init__(self):
        self.volumes = {}

    def name(self, value):
        self.volumes['name'] = value
        return self

    def configMap(self, value):
        self.volumes['configMap'] = value
        return self

    def hostPath(self, value):
        self.volumes['hostPath'] = value
        return self

    def persistentVolumeClaim(self, claimName):
        self.volumes['persistentVolumeClaim'] = {'claimName': claimName}
        return self


class Spec:
    spec = {}

    def __init__(self):
        if not 'containers' in self.spec:
            self.spec['containers'] = []

    def hostAliases(self, value):
        self.spec['hostAliases'] = value

    def env(self, value):
        self.spec['env'] = value

    def securityContext(self, value):
        self.spec['securityContext'] = value

    class containers(Containers):
        def __init__(self):
            super().__init__()
            Spec.spec['containers'] = []

        def __del__(self):
            Spec.spec['containers'].append(self.container)

    class volumes(Volumes):
        def __init__(self):
            super().__init__()
            Spec.spec['volumes'] = []

        def __del__(self):
            Spec.spec['volumes'].append(self.volumes)


class Namespace(Common):
    components = None
    namespace = {}

    def __init__(self, components = None):
        super().__init__()
        self.apiVersion()
        self.kind('Namespace')
        if not components :
            self.components = uuid.uuid4().hex
        else:
            self.components = components
        Namespace.components  = self.components
        self.namespace[self.components] = {}
        self.namespace[self.components]['metadata'] = {}

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            # if not 'metadata' in Namespace.namespace:
                # Namespace.namespace['metadata'] = {}
        def __del__(self):
            Namespace.namespace[Namespace.components]['metadata'].update(self.metadata())
    def name(self):
        return self.namespace[self.components]['metadata']['name']
    def dump(self):
        self.namespace[self.components].update(self.commons)
        return super().dump(self.namespace[self.components])

    def debug(self):
        print(self.dump())


class ConfigMap(Common):
    components = ''
    config = {}

    def __init__(self, components = None):
        super().__init__()
        self.apiVersion()
        self.kind('ConfigMap')
        if not components :
            self.components = uuid.uuid4().hex
        else:
            self.components = components
        ConfigMap.components = self.components
        ConfigMap.config[self.components] = {}
        self.config[self.components]['metadata'] = {}

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            # ConfigMap.config[ConfigMap.components]['metadata'] = {}

        def __del__(self):
            ConfigMap.config[ConfigMap.components]['metadata'].update(
                self.metadata())

    def data(self, value):
        if 'data' in self.config[self.components]:
            self.config[self.components]['data'].update(value)
        else:
            self.config[self.components]['data'] = value
        return(self)

    def from_file(self, name, path):
        with open(path, 'r') as file:
            text = file.read()
            self.data({name: lss(text)})
        return(self)

    def from_env_file(self, path):
        env = {}
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.split('=')
                env[key] = value.replace('\n', '')
        self.data(env)
        return(self)

    def dump(self):
        self.config[self.components].update(self.commons)
        return super().dump(self.config[self.components])

    def json(self):
        print(self.config[self.components])

    def debug(self):
        print(self.dump())

    def save(self, filename=None):
        if not filename:
            filename = self.components + '.yaml'
        super().save(filename, self.dump())

class Secret(ConfigMap):
    def __init__(self, name = None):
        super().__init__(name)
        self.apiVersion()
        self.kind('Secret')

    def type(self, value):
        self.config['type'] = value

    def key(self, path):
        with open(path, 'r') as file:
            text = file.read()
            self.data({'tls.key': pss(b64encode(text.encode()).decode())})
        return(self)

    def cert(self, path):
        with open(path, 'r') as file:
            text = file.read()
            self.data({'tls.crt': pss(b64encode(text.encode()).decode())})
        return(self)


class ServiceAccount(Common):
    account = {}

    def __init__(self):
        super().__init__()
        self.apiVersion()
        self.kind('ServiceAccount')
        # self.metadata = Metadata()
        self.account['metadata'] = {}

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            ServiceAccount.account['metadata'] = {}

        def __del__(self):
            ServiceAccount.account['metadata'].update(self.metadata)

    def dump(self):
        self.account.update(self.commons)
        self.account['metadata'].update(self.metadata.metadata())
        return self.yaml.dump(self.account)

    def debug(self):
        print(self.dump())


class PersistentVolume(Common):
    name = ''
    persistentVolume = {}

    def __init__(self, name):
        super().__init__()
        self.apiVersion()
        self.kind('PersistentVolume')
        PersistentVolume.name = name
        PersistentVolume.persistentVolume[PersistentVolume.name] = {}

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in PersistentVolume.persistentVolume[PersistentVolume.name]:
                PersistentVolume.persistentVolume[PersistentVolume.name]['metadata'] = {
                }

        def __del__(self):
            PersistentVolume.persistentVolume[PersistentVolume.name]['metadata'].update(
                self.metadata())

    class spec(Spec):
        def __init__(self):
            super().__init__()
            if not 'spec' in PersistentVolume.persistentVolume[PersistentVolume.name]:
                PersistentVolume.persistentVolume[PersistentVolume.name]['spec'] = {
                }

        def storageClassName(self, value):
            PersistentVolume.persistentVolume[PersistentVolume.name]['spec']['storageClassName'] = value
            return(self)

        def capacity(self, value):
            PersistentVolume.persistentVolume[PersistentVolume.name]['spec']['capacity'] = value
            return(self)

        def accessModes(self, value):
            PersistentVolume.persistentVolume[PersistentVolume.name]['spec']['accessModes'] = [
            ]
            PersistentVolume.persistentVolume[PersistentVolume.name]['spec']['accessModes'] = value
            return(self)

        def hostPath(self, value):
            PersistentVolume.persistentVolume[PersistentVolume.name]['spec']['hostPath'] = value
            return(self)

    def dump(self):
        self.persistentVolume[self.name].update(self.commons)
        # self.pod['metadata'].update(self.metadata.metadata())
        # self.persistentVolume['spec'].update(self.spec.spec)
        # self.pod['spec']['containers'].append(self.spec.containers.container)
        return super().dump(self.persistentVolume[self.name])

    def json(self):
        print(self.persistentVolume)

    def debug(self):
        print(self.dump())


class PersistentVolumeClaim(Common):
    persistentVolumeClaim = {}

    def __init__(self, name):
        super().__init__()
        self.apiVersion()
        self.kind('PersistentVolumeClaim')
        PersistentVolumeClaim.name = name
        PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name] = {
        }

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]:
                PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['metadata'] = {
                }

        def __del__(self):
            PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['metadata'].update(
                self.metadata())

    class spec(Spec):
        def __init__(self):
            super().__init__()
            if not 'spec' in PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]:
                PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['spec'] = {
                }

        def storageClassName(self, value):
            PersistentVolumeClaim.persistentVolumeClaim[
                PersistentVolumeClaim.name]['spec']['storageClassName'] = value
            return(self)

        def accessModes(self, value):
            PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['spec']['accessModes'] = [
            ]
            PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['spec']['accessModes'] = value
            return(self)

        def hostPath(self, value):
            PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['spec']['hostPath'] = value
            return(self)

        def resources(self, value):
            PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.name]['spec']['resources'] = value
            return(self)

    def dump(self):
        self.persistentVolumeClaim[self.name].update(self.commons)
        # self.pod['metadata'].update(self.metadata.metadata())
        # self.persistentVolume['spec'].update(self.spec.spec)
        # self.pod['spec']['containers'].append(self.spec.containers.container)
        return super().dump(self.persistentVolumeClaim[self.name])

    def json(self):
        print(self.persistentVolume)

    def debug(self):
        print(self.dump())


class Pod(Common):
    pod = {}

    def __init__(self):
        super().__init__()
        self.apiVersion()
        self.kind('Pod')
        self.pod['metadata'] = {}
        self.pod['spec'] = {}
        self.pod['spec']['containers'] = []

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in Pod.pod:
                Pod.pod['metadata'] = {}

        def __del__(self):
            Pod.pod['metadata'].update(self.metadata())

    class spec(Spec):
        # containers = Containers()
        def __init__(self):
            super().__init__()
            if not 'spec' in Pod.pod:
                Pod.pod['spec'] = {}
    # 	def restartPolicy(self, value):
    # 		Pod.pod['spec']['restartPolicy'] = value
    # 	def hostAliases(self, value):
    # 		Pod.pod['spec']['hostAliases'] = value
    # 	def env(self, value):
    # 		Pod.pod['spec']['env'] = value
    # 	def securityContext(self,value):
    # 		Pod.pod['spec']['securityContext'] = value
        # class containers(Containers):
            # def __init__(self):
                # super().__init__()
                # Pod.pod['spec']['containers'] = []
            # def __del__(self):
                # Pod.pod['spec']['containers'].append(self.containers.container)
                # print(self.containers.container)

        class volumes(Volumes):
            def __init__(self):
                Pod.pod['spec']['volumes'] = []

            def __del__(self):
                Pod.pod['spec']['volumes'].append(self.volumes)

    def dump(self):
        self.pod.update(self.commons)
        # self.pod['metadata'].update(self.metadata.metadata())
        self.pod['spec'].update(self.spec.spec)
        # self.pod['spec']['containers'].append(self.spec.containers.container)
        return super().dump(self.pod)

    def json(self):
        print(self.pod)

    def debug(self):
        print(self.dump())


class Service(Common):
    components = None
    service = {}

    def __init__(self):
        super().__init__()
        self.apiVersion()
        self.kind('Service')
        self.components = uuid.uuid4().hex
        self.service[self.components] = {}
        Service.components = self.components

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in Service.service[Service.components]:
                Service.service[Service.components]['metadata'] = {}
        def __del__(self):
            Service.service[Service.components]['metadata'].update(self.metadata())

    class spec:
        def __init__(self):
            if not 'spec' in Service.service[Service.components]:
                Service.service[Service.components]['spec'] = {}
                Service.service[Service.components]['spec']['ports'] = [] 

        def selector(self, value):
            Service.service[Service.components]['spec']['selector'] = value
            return self

        def type(self, value):
            Service.service[Service.components]['spec']['type'] = value
            return self

        def ports(self, value):
            if type(value) == dict :
                Service.service[Service.components]['spec']['ports'].append(value)
            elif type(value) == list :
                Service.service[Service.components]['spec']['ports'] = value
                # for v in value :
                    # Service.service[Service.components]['spec']['ports'].append(v)
            return self

        def externalIPs(self, value):
            Service.service[Service.components]['spec']['externalIPs'] = value
            return self

        def clusterIP(self, value):
            Service.service[Service.components]['spec']['clusterIP'] = value
            return self
        def externalTrafficPolicy(self, value):
            Service.service[Service.components]['spec']['externalTrafficPolicy'] = value
            return self

    class status:
        def __init__(self):
            if not 'status' in Service.service[Service.components]:
                Service.service[Service.components]['status'] = {}

        def loadBalancer(self, value):
            Service.service[Service.components]['status']['loadBalancer'] = value
            return self

    def dump(self):
        self.service[self.components].update(self.commons)
        return super().dump(self.service[self.components])

    def debug(self):
        print(self.dump())


class Deployment(Common):
    components = None
    deployment = {}

    def __init__(self, components = None):
        super().__init__()
        self.apiVersion('apps/v1')
        self.kind('Deployment')
        if not components :
            self.components = uuid.uuid4().hex
        else:
            self.components = components

        Deployment.components = self.components
        self.deployment[self.components] = {}
        self.deployment[self.components]['metadata'] = {}
        # self.deployment['apiVersion'] = 'apps/v1'
        # self.deployment['kind'] = 'Deployment'

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in Deployment.deployment[Deployment.components] :
                Deployment.deployment[Deployment.components]['metadata'] = {}

        def __del__(self):
            Deployment.deployment[Deployment.components]['metadata'].update(self.metadata())

    class spec(Spec):
        def __init__(self):
            if not 'spec' in Deployment.deployment[Deployment.components]:
                Deployment.deployment[Deployment.components]['spec'] = {}

        def selector(self, value):
            Deployment.deployment[Deployment.components]['spec']['selector'] = value
            return self
        def progressDeadlineSeconds(self, value):
            if type(value) == int :
                Deployment.deployment[Deployment.components]['spec']['progressDeadlineSeconds'] = value
            return self
        def revisionHistoryLimit(self, value):
            if type(value) == int :
                Deployment.deployment[Deployment.components]['spec']['revisionHistoryLimit'] = value
            return self
        def replicas(self, value):
            Deployment.deployment[Deployment.components]['spec']['replicas'] = value
            return self

        def serviceName(self, value):
            # self.spec['serviceName'] = value
            Deployment.deployment[Deployment.components]['spec']['serviceName'] = value
            return self

        class template():
            def __init__(self):
                # super().__init__()
                if not 'template' in Deployment.deployment[Deployment.components]['spec']:
                    Deployment.deployment[Deployment.components]['spec']['template'] = {}

            class metadata(Metadata):
                def __init__(self):
                    super().__init__()
                    Deployment.deployment[Deployment.components]['spec']['template']['metadata'] = {}

                def __del__(self):
                    Deployment.deployment[Deployment.components]['spec']['template']['metadata'].update(
                        self.metadata())

            class spec(Spec):
                def __init__(self):
                    if not 'spec' in Deployment.deployment[Deployment.components]['spec']['template']:
                        Deployment.deployment[Deployment.components]['spec']['template']['spec'] = {}
                class affinity():
                    def __init__(self):
                        if not 'affinity' in Deployment.deployment[Deployment.components]['spec']['template']['spec']:
                            Deployment.deployment[Deployment.components]['spec']['template']['spec']['affinity'] = {}
                            Deployment.deployment[Deployment.components]['spec']['template']['spec']['affinity']['nodeAffinity'] = {}
                    def nodeAffinity(self, value):
                        Deployment.deployment[Deployment.components]['spec']['template']['spec']['affinity']['nodeAffinity'] = value    
                def securityContext(self, value):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['securityContext'] = value

                def hostAliases(self, value):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['hostAliases'] = value

                class initContainers(Containers):
                    def __init__(self):
                        super().__init__()
                        Deployment.deployment[Deployment.components]['spec']['template']['spec']['initContainers'] = []

                    def __del__(self):
                        Deployment.deployment[Deployment.components]['spec']['template']['spec']['initContainers'].append(
                            self.container)

                class containers(Containers):
                    def __init__(self, name = None):
                        super().__init__()
                        if not 'containers' in Deployment.deployment[Deployment.components]['spec']['template']['spec'] :
                            Deployment.deployment[Deployment.components]['spec']['template']['spec']['containers'] = []

                    def __del__(self):
                        Deployment.deployment[Deployment.components]['spec']['template']['spec']['containers'].append(
                            self.container)
                def imagePullSecrets(self, secret):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['imagePullSecrets'] = secret
                def nodeSelector(self, group):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['nodeSelector'] = group
                def restartPolicy(self, value):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['restartPolicy'] = value
                def dnsPolicy(self, value):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['dnsPolicy'] = value
                def volumes(self, value):
                    Deployment.deployment[Deployment.components]['spec']['template']['spec']['volumes'] = value
                # class volumes(Volumes):
                    # def __init__(self):
                    #     super().__init__()
                    #     if not 'volumes' in Deployment.deployment[Deployment.components]['spec']['template']['spec']:
                    #         Deployment.deployment[Deployment.components]['spec']['template']['spec']['volumes'] = []

                    # def __del__(self):
                    #     Deployment.deployment[Deployment.components]['spec']['template']['spec']['volumes'].append(
                    #         self.volumes)

                # def __del__(self):
                    # print('debug', self)
    
        class strategy():
            def __init__(self):
                Deployment.deployment[Deployment.components]['spec']['strategy'] = {}

            def type(self, name):
                Deployment.deployment[Deployment.components]['spec']['strategy']['type'] = name
                return self
            def rollingUpdate(self, maxSurge, maxUnavailable):
                Deployment.deployment[Deployment.components]['spec']['strategy']['rollingUpdate'] = {}
                Deployment.deployment[Deployment.components]['spec']['strategy']['rollingUpdate']['maxSurge'] = maxSurge
                Deployment.deployment[Deployment.components]['spec']['strategy']['rollingUpdate']['maxUnavailable'] = maxUnavailable
            # def __del__(self):
            #     Deployment.deployment['spec']['template']['spec']['containers'].append(
            #         self.container)
        
    def dump(self):
        self.deployment[self.components].update(self.commons)
        return super().dump(self.deployment[self.components])

    def debug(self):
        print(self.dump())

    def json(self):
        print(self.deployment)


class StatefulSet(Deployment):
    def __init__(self):
        super().__init__()
        self.kind('StatefulSet')


class Ingress(Common):
    components = None
    ingress = {}

    def __init__(self, components = None):
        super().__init__()
        self.apiVersion('networking.k8s.io/v1')
        self.kind('Ingress')
        if not components :
            self.components = uuid.uuid4().hex
        else:
            self.components = components
        Ingress.components =  self.components
        self.ingress[self.components] = {}

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in Ingress.ingress[Ingress.components]:
                Ingress.ingress[Ingress.components]['metadata'] = {}

        def __del__(self):
            Ingress.ingress[Ingress.components]['metadata'].update(self.metadata())

    class spec:
        def __init__(self):
            if not 'spec' in Ingress.ingress[Ingress.components]:
                Ingress.ingress[Ingress.components]['spec'] = {}

        def rules(self, value):
            if not 'rules' in Ingress.ingress[Ingress.components]['spec']:
                Ingress.ingress[Ingress.components]['spec']['rules'] = []
            Ingress.ingress[Ingress.components]['spec']['rules'].extend(value)

        def tls(self, value):
            if not 'tls' in Ingress.ingress[Ingress.components]['spec']:
                Ingress.ingress[Ingress.components]['spec']['tls'] = []
            Ingress.ingress[Ingress.components]['spec']['tls'].extend(value)

    def dump(self):
        self.ingress[self.components].update(self.commons)
        return super().dump(self.ingress[self.components])

    def debug(self):
        print(self.dump())

    def json(self):
        print(self.ingress[self.components])


class IngressRouteTCP(Ingress):
    ingress = {}

    def __init__(self):
        super().__init__()
        self.apiVersion('traefik.containo.us/v1alpha1')
        self.kind('IngressRouteTCP')

    class metadata(Metadata):
        def __init__(self):
            super().__init__()
            if not 'metadata' in IngressRouteTCP.ingress:
                IngressRouteTCP.ingress['metadata'] = {}

        def __del__(self):
            IngressRouteTCP.ingress['metadata'].update(self.metadata())

    class spec:
        def entryPoints(self, value):
            IngressRouteTCP.ingress['entryPoints'] = value

        def routes(self, value):
            IngressRouteTCP.ingress['routes'] = value


class Compose(Logging):
    def __init__(self, workload):
        super().__init__()
        self.compose = []
        self.workload = workload
    # def __del__(self):
        # Kubernetes.composes.update(self.metadata)
        # print(self.compose)

    def add(self, object):
        self.compose.append(object.dump())
        return(self)

    def debug(self):
        print(self.yaml())

    def json(self):
        print(self.compose)

    def yaml(self):
        return('---\n'.join(self.compose))

    def save(self, path=None):
        if not path:
            path = self.workload + '.yaml'
        path = os.path.expanduser(path)
        # if os.path.exists(path):
        # os.remove(path)
        with open(path, 'w') as file:
            file.write('---\n'.join(self.compose))

    def execute(self, command, text):
        shell = """cat <<'EOF' | kubectl {command} -f -
{stdin}
EOF""".format(command=command, stdin=text)
        self.logging.debug(shell)
        # print(shell)
        os.system(shell)

    def create(self):
        self.execute('create', self.yaml())

    def delete(self):
        self.execute('delete', self.yaml())

    def replace(self):
        self.execute('replace', self.yaml())


class Kubernetes(Logging):
    def __init__(self):
        super().__init__()
        self.kubernetes = {}
        # self.kubernetes['namespace'] = []
        # self.kubernetes['config'] = []
        # self.kubernetes['workload'] = []
        self.namespaces = []
        self.workspace = '/tmp'

        self.parser = OptionParser("usage: %prog [options] <command>")
        self.parser.add_option("-e", "--environment", dest="environment",
                               help="environment", metavar="development|testing|production")
        self.parser.add_option("", "--config", dest="config",
                               help="~/.kube/config", metavar="~/.kube/config")                       
        self.parser.add_option('-l', '--list', dest='list',
                               action='store_true', help='print service of workloads')

        group = OptionGroup(self.parser, "Cluster Management Commands")
        group.add_option('-g', '--get', dest='get',
                         action='store_true', help='Display one or many resources')
        # group.add_option('-s', '--set', dest='set',
        #                  action='store_true', help='Display one or many resources')
        group.add_option('-c', '--create', dest='create', action='store_true',
                         help='Create a resource from a file or from stdin')
        group.add_option('-d', '--delete', dest='delete', action='store_true',
                         help='Delete resources by filenames, stdin, resources and names, or by resources and label selector')
        group.add_option('-r', '--replace', dest='replace', action='store_true',
                         help='Replace a resource by filename or stdin')
        self.parser.add_option_group(group)

        group = OptionGroup(self.parser, "Namespace")
        group.add_option('-n', '--namespace', dest='namespace',
                         action='store_true', help='Display namespace')
        group.add_option('-s', '--service', dest='service',
                         action='store_true', help='Display service')
        self.parser.add_option_group(group)

        group = OptionGroup(self.parser, "Others")
        group.add_option('', '--logfile', dest='logfile',
                         help='logs file.', default='debug.log')
        group.add_option('-y', '--yaml', dest='yaml',
                         action='store_true', help='show yaml compose')
        group.add_option('', '--export', dest='export',
                         action='store_true', help='export docker compose')
        # group.add_option('-d','--daemon', dest='daemon', action='store_true', help='run as daemon')
        group.add_option("", "--debug", action="store_true",
                         dest="debug", help="debug mode")
        group.add_option('-v', '--version', dest='version',
                         action='store_true', help='print version information')
        self.parser.add_option_group(group)

        (self.options, self.args) = self.parser.parse_args()
        if self.options.debug:
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                                format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        elif self.options.logfile:
            logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)-8s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S', filename=self.options.logfile, filemode='a')

        if self.options.debug:
            self.logging.debug("="*50)
            self.logging.debug(self.options)
            self.logging.debug(self.args)
            self.logging.debug("="*50)

    def usage(self):
        print("Python controls the Kubernetes cluster manager.\n")
        self.parser.print_help()
        print("\nHomepage: http://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
        exit()

    def namespace(self, ns):
        if type(ns) == str :
            self.namespaces.append(ns)
        else:
            self.namespaces = ns
    def compose(self, compose):
        self.kubernetes[compose.workload] = compose
        self.logging.info("kubernetes : %s" % (compose.workload))

    def workload(self, compose):
        self.kubernetes[compose.workload] = compose
        self.logging.info("kubernetes : %s" % (compose.workload))
    def configmap(self, config):
        self.kubernetes['config'] = compose
        self.logging.info("kubernetes : %s" % (compose.workload))
    def save(self, env):
        if env in self.kubernetes.keys():
            path = os.path.expanduser(self.workspace + '/' + env + '.yaml')
            self.kubernetes[env].save(path)
            if os.path.exists(path):
                # os.remove(path)
                self.logging.info('save as %s' % path)
                return path
            else:
                return None

    def yaml(self):
        print(self.composes)
        print('---\n'.join(self.composes))

    def debug(self):
        self.logging.debug(self.kubernetes)

    def execute(self, cmd):
        command = "kubectl {cmd}".format(cmd=cmd)
        self.logging.debug(command)
        os.system(command)
        return(self)

    def version(self):
        self.execute('version')
        self.execute('api-resources')
        self.execute('api-versions')
        exit()

    def create(self, env):
        path = self.save(env)
        if path:
            cmd = "{command} -f {yamlfile}".format(
                command="create", yamlfile=path)
            self.logging.info('create %s' % path)
            self.execute(cmd)
        exit()

    def delete(self, env):
        path = self.save(env)
        if path:
            cmd = "{command} -f {yamlfile}".format(
                command="delete", yamlfile=path)
            self.logging.info('delete %s ' % path)
            self.execute(cmd)
        exit()

    def replace(self, env):
        path = self.save(env)
        if path:
            cmd = "{command} -f {yamlfile}".format(
                command="replace", yamlfile=path)
            self.logging.info('replace %s ' % path)
            self.execute(cmd)
        exit()

    def kubeNamespace(self):
        cmd = "get namespace"
        self.logging.info(cmd)
        self.execute(cmd)

    def service(self):
        cmd = "get service"
        self.logging.info(cmd)
        self.execute(cmd)

    def describe(self):
        pass

    def edit(self):
        pass

    def get(self, args):
        cmd = "get {args}".format(args=args)
        self.logging.info('%s ' % cmd)
        self.execute(cmd)

    def list(self):
        for item in self.kubernetes:
            print(item)

    def main(self):

        if self.options.list:
            self.list()
        elif self.options.get:
            self.get(' '.join(self.args))
        elif self.options.yaml:
            self.yaml()
        elif self.options.version:
            self.version()

        if self.options.namespace:
            self.kubeNamespace()
        elif self.options.service:
            self.service()

        elif self.options.create:
            if self.options.environment:
                self.create(self.options.environment)
            else:
                for env in self.kubernetes.keys():
                    self.create(env)
        elif self.options.delete:
            if self.options.environment:
                self.delete(self.options.environment)
            else:
                for env in self.kubernetes.keys():
                    self.delete(env)
        elif self.options.replace:
            if self.options.environment:
                self.replace(self.options.environment)
            else:
                for env in self.kubernetes.keys():
                    self.replace(env)
        else:
            if not self.args:
                self.usage()
