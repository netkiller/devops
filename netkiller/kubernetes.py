# -*- coding: utf-8 -*-
try:
	from email.mime import image
	import os,uuid
	from pickle import TRUE
	from posixpath import split
	import sys
	import json
	from optparse import OptionParser, OptionGroup
	import logging
	import logging.handlers
	from logging import basicConfig
	from ruamel.yaml import YAML
	from ruamel.yaml.scalarstring import LiteralScalarString as lss, PreservedScalarString as pss
	from io import StringIO
	from base64 import b64encode

except ModuleNotFoundError as err:
	print(err)

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
			Always = 'Always'
			Never ='Never'
	class dnsPolicy():
		ClusterFirst = 'ClusterFirst'
	class Service():
		ClusterIP = 'ClusterIP'
		LoadBalancer = 'LoadBalancer'
		ExternalName = 'ExternalName'
		NodePort = 'NodePort'
		class externalTrafficPolicy:
			Local = 'Local'
			Cluster = 'Cluster'
	class Ingress():
		class pathType():
			Prefix = 'Prefix'
			ImplementationSpecific = 'ImplementationSpecific'
	class PersistentVolume():
		class accessModes():
			ReadWriteOnce = 'ReadWriteOnce'


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
		if value :
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
		if value :
			if not 'env' in self.container :
				self.container['env'] = []
			self.container['env'] = value
		return self

	def resources(self, value = None):
		if value :
			self.container['resources'] = value
		return self

	def livenessProbe(self, value = None):
		if value :
			self.container['livenessProbe'] = value
		return self
	def readinessProbe(self, value = None):
		if value :
			self.container['readinessProbe'] = value
		return self
	def securityContext(self, value):
		if value :
			self.container['securityContext'] = value
		return self
	def command(self, value):
		if value :
			self.container['command'] = value
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
		self.config[self.components]['type'] = value

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
			ServiceAccount.account['metadata'].update(self.metadata())

	def dump(self):
		self.account.update(self.commons)
		self.account['metadata'].update(self.metadata.metadata())
		return self.yaml.dump(self.account)

	def debug(self):
		print(self.dump())

class StorageClass(Common):
	components = ''
	storageClass = {}

	WaitForFirstConsumer = 'WaitForFirstConsumer'

	def __init__(self, components = None):
		super().__init__()
		self.apiVersion('storage.k8s.io/v1')
		self.kind('StorageClass')
		if not components :
			self.components = uuid.uuid4().hex
		else:
			self.components = components
		StorageClass.components = self.components
		StorageClass.storageClass[StorageClass.components] = {}
	class metadata(Metadata):
		def __init__(self):
			super().__init__()
			if not 'metadata' in StorageClass.storageClass[StorageClass.components]:
				StorageClass.storageClass[StorageClass.components]['metadata'] = {}
		def __del__(self):
			StorageClass.storageClass[StorageClass.components]['metadata'].update(
				self.metadata())
	def provisioner(self, value):
		StorageClass.storageClass[StorageClass.components]['provisioner'] = value
	def volumeBindingMode(self, value):
		StorageClass.storageClass[StorageClass.components]['volumeBindingMode'] = value
	def dump(self):
		self.storageClass[self.components].update(self.commons)
		return super().dump(self.storageClass[self.components])
	def json(self):
		print(self.storageClass)

	def debug(self):
		print(self.dump())

class PersistentVolume(Common):

	components = ''
	persistentVolume = {}

	def __init__(self, components = None):
		super().__init__()
		self.apiVersion()
		self.kind('PersistentVolume')
		if not components :
			self.components = uuid.uuid4().hex
		else:
			self.components = components
		PersistentVolume.components = self.components
		PersistentVolume.persistentVolume[PersistentVolume.components] = {}

	class metadata(Metadata):
		def __init__(self):
			super().__init__()
			if not 'metadata' in PersistentVolume.persistentVolume[PersistentVolume.components]:
				PersistentVolume.persistentVolume[PersistentVolume.components]['metadata'] = {
				}

		def __del__(self):
			PersistentVolume.persistentVolume[PersistentVolume.components]['metadata'].update(
				self.metadata())

	class spec(Spec):
		def __init__(self):
			super().__init__()
			if not 'spec' in PersistentVolume.persistentVolume[PersistentVolume.components]:
				PersistentVolume.persistentVolume[PersistentVolume.components]['spec'] = {}
		def storageClassName(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['storageClassName'] = value
			return(self)
		def capacity(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['capacity'] = value
			return(self)
		def accessModes(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['accessModes'] = []
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['accessModes'] = value
			return(self)
		def persistentVolumeReclaimPolicy(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['persistentVolumeReclaimPolicy'] = value
			return(self)
		def local(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['local'] = {'path':value}
			return(self)
		def hostPath(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['hostPath'] = value
			return(self)
		def nodeAffinity(self, value):
			PersistentVolume.persistentVolume[PersistentVolume.components]['spec']['nodeAffinity'] = value
			return(self)

	def dump(self):
		self.persistentVolume[self.components].update(self.commons)
		# self.pod['metadata'].update(self.metadata.metadata())
		# self.persistentVolume['spec'].update(self.spec.spec)
		# self.pod['spec']['containers'].append(self.spec.containers.container)
		return super().dump(self.persistentVolume[self.components])

	def json(self):
		print(self.persistentVolume)

	def debug(self):
		print(self.dump())


class PersistentVolumeClaim(Common):
	components = ''
	persistentVolumeClaim = {}

	def __init__(self, components = None):
		super().__init__()
		self.apiVersion()
		self.kind('PersistentVolumeClaim')
		if not components :
			self.components = uuid.uuid4().hex
		else:
			self.components = components
		PersistentVolumeClaim.components = self.components
		PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components] = {
		}

	class metadata(Metadata):
		def __init__(self):
			super().__init__()
			if not 'metadata' in PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]:
				PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['metadata'] = {
				}

		def __del__(self):
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['metadata'].update(
				self.metadata())

	class spec(Spec):
		def __init__(self):
			super().__init__()
			if not 'spec' in PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]:
				PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec'] = {
				}

		def storageClassName(self, value):
			PersistentVolumeClaim.persistentVolumeClaim[
				PersistentVolumeClaim.components]['spec']['storageClassName'] = value
			return(self)

		def accessModes(self, value):
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec']['accessModes'] = [
			]
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec']['accessModes'] = value
			return(self)

		def hostPath(self, value):
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec']['hostPath'] = value
			return(self)

		def resources(self, value):
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec']['resources'] = value
			return(self)
		def selector(self, value):
			PersistentVolumeClaim.persistentVolumeClaim[PersistentVolumeClaim.components]['spec']['selector'] = value
			return(self)

	def dump(self):
		self.persistentVolumeClaim[self.components].update(self.commons)
		# self.pod['metadata'].update(self.metadata.metadata())
		# self.persistentVolume['spec'].update(self.spec.spec)
		# self.pod['spec']['containers'].append(self.spec.containers.container)
		return super().dump(self.persistentVolumeClaim[self.components])

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
		def externalName(self, value):
			Service.service[Service.components]['spec']['externalName'] = value
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
		def volumeClaimTemplates(self, value):
			Deployment.deployment[Deployment.components]['spec']['volumeClaimTemplates'] = value
			return self
		class template():
			def __init__(self):
				# super().__init__()
				if not 'template' in Deployment.deployment[Deployment.components]['spec']:
					Deployment.deployment[Deployment.components]['spec']['template'] = {}

			class metadata(Metadata):
				def __init__(self):
					super().__init__()
					if not 'metadata' in Deployment.deployment[Deployment.components]['spec']['template'] :
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
				def nodeSelector(self, value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['nodeSelector'] = value
				def nodeName(self, value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['nodeName'] = value
				def restartPolicy(self, value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['restartPolicy'] = value
				def dnsPolicy(self, value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['dnsPolicy'] = value
				def volumes(self, value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['volumes'] = value
				def tolerations(self,value):
					Deployment.deployment[Deployment.components]['spec']['template']['spec']['tolerations'] = value
				# class volumes(Volumes):
					# def __init__(self):
					#     super().__init__()
					#     if not 'volumes' in Deployment.deployment[Deployment.components]['spec']['template']['spec']:
					#         Deployment.deployment[Deployment.components]['spec']['template']['spec']['volumes'] = []
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


class DaemonSet(Deployment):
	def __init__(self):
		super().__init__()
		self.kind('DaemonSet')

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
	def __init__(self, environment, kubeconfig = None):
		super().__init__()
		self.compose = []
		self.environment = environment
		self.kubeconfig = kubeconfig
	def add(self, object):
		self.compose.append(object.dump())
		return(self)
	def workload(self, compose):
		self.compose.append(compose.dump())
	#     self.logging.info("kubernetes : %s" % (compose.workload))
		return(self)
	def configmap(self, config):
		self.compose.append(config.dump())
	#     self.logging.info("kubernetes : %s" % (compose.workload))
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
		directory = os.path.dirname(path)
		if not os.path.exists(directory):
			os.makedirs(directory,exist_ok=True)
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
	def __init__(self, kubeconfig = None):
		super().__init__()
		self.environments = {}
		self.kubernetes = {}
		self.workspace = '~/.netkiller'
		if kubeconfig :
			self.kubeconfig(kubeconfig) 

		self.parser = OptionParser("usage: %prog [options] <command>")
		self.parser.add_option("-e", "--environment", dest="environment",
							   help="environment", metavar="development|testing|production")
		self.parser.add_option("", "--kubeconfig", dest="kubeconfig",
							   help="~/.kube/config", metavar="~/.kube/config")                       
		self.parser.add_option('-l', '--list', dest='list',
							   action='store_true', help='print service of workloads')

		group = OptionGroup(self.parser, "Namespace")
		group.add_option('-n', '--namespace', dest='namespace', metavar='default', help='Set namespace')
		self.parser.add_option_group(group)

		group = OptionGroup(self.parser, "Cluster Management Commands")
		group.add_option('-g', '--get', dest='get', action='store_true', help='Display one or many resources')
		group.add_option('-s', '--set', dest='set', action='store_true', help='Display service')                 
		group.add_option('-c', '--create', dest='create', action='store_true',
						 help='Create a resource from a file or from stdin')
		group.add_option('-d', '--delete', dest='delete', action='store_true',
						 help='Delete resources by filenames, stdin, resources and names, or by resources and label selector')
		group.add_option('-r', '--replace', dest='replace', action='store_true',
						 help='Replace a resource by filename or stdin')
		group.add_option('-u', '--upgrade', dest='upgrade', metavar="latest", help='upgrade version of image.')
		
		self.parser.add_option_group(group)

		group = OptionGroup(self.parser, "Others")
		group.add_option('', '--logfile', dest='logfile',
						 help='logs file.', default='debug.log')
		group.add_option('-y', '--yaml', dest='yaml',
						 action='store_true', help='show yaml compose')
		group.add_option('', '--export', dest='export', metavar="~/.kube/config",help='export yaml files')
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

	def compose(self, compose):
		self.kubernetes[compose.environment] = compose
		if compose.kubeconfig :
			self.environments[compose.environment] = compose.kubeconfig
		self.logging.info("kubernetes : %s" % (compose.environment))
		return self
	def environment(self, name, kubeconfig = None):
		if type(name) == dict :
			self.environments = name
		else:	
			self.environments[name] = kubeconfig
		self.logging.info("kubeconfig : %s => %s" % (name,kubeconfig))
		return self
	def save(self, item):
		directory = self.workspace
		if self.options.environment:
			directory = self.workspace + '/' + self.options.environment

		if not os.path.exists(directory):
			os.makedirs(directory)

		if item in self.kubernetes.keys():
			path = os.path.expanduser(directory + '/' + item + '.yaml')
			if os.path.exists(path):
				os.remove(path)
			self.logging.info('save as %s' % path)
			self.kubernetes[item].save(path)
			return path
		return None

	def yaml(self, project):
		if project :
			compose = self.kubernetes[project]
			print(compose.yaml())
		else:
			for name, compose in self.kubernetes.items() :
				print(compose.yaml())
	def export(self, path, workloads = None):
		if workloads :
			for workload in workloads:
				if workload in self.kubernetes :
					file = path+ '/' + workload + '.yaml'
					if not os.path.exists(path) :
						os.mkdir(path)
					self.kubernetes[workload].save(file)
					msg = "export {0} {1}".format(workload, file)
					self.logging.info(msg)
					print(msg)
		else:
			for name, compose in self.kubernetes.items() :
				self.export(path, [name])
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
		# exit()

	def delete(self, env):
		path = self.save(env)
		if path:
			cmd = "{command} -f {yamlfile}".format(
				command="delete", yamlfile=path)
			self.logging.info('delete %s ' % path)
			self.execute(cmd)
		# exit()

	def replace(self, env):
		path = self.save(env)
		if path:
			cmd = "{command} -f {yamlfile}".format(
				command="replace", yamlfile=path)
			self.logging.info('replace %s ' % path)
			self.execute(cmd)
		# exit()

	def upgrade(self, namespace, project, image):
		cmd = "set image deployment/{project} {project}={image} -n {namespace}".format(namespace=namespace, project=project, image=image)
		self.logging.info("namespace={namespace}, {project}={image}".format(namespace=namespace, project=project, image=image))
		self.logging.debug('upgrade %s ' % cmd)
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
	def kubeconfig(self, kubeconfig):
		os.environ['KUBECONFIG']=kubeconfig
		self.logging.info('KUBECONFIG=%s ' % kubeconfig)
	def main(self):

		if self.options.kubeconfig :
			self.kubeconfig(self.options.kubeconfig)
		elif self.options.environment and self.options.environment in self.environments:
			self.kubeconfig(self.environments[self.options.environment])
		else:
			for key,value in self.environments.items():
				print( "%s => %s" % (key,value) )

		if self.options.list:
			self.list()
			return
		elif self.options.get:
			self.get(' '.join(self.args))
		elif self.options.set :
			self.set()
		elif self.options.yaml:
			if self.args :
				project = self.args[0]
			else:
				project = None
			self.yaml(project)
			return
		elif self.options.version:
			self.version()

		# if self.options.namespace:
		#     self.kubeNamespace()

		elif self.options.create:
			if self.args:
				if self.args[0] in self.kubernetes.keys() :
					self.create(self.args[0])
				else:
					self.logging.error("The {0} isn't found!".format(self.args[0]))
					self.list()
			else:
				for env in self.kubernetes.keys():
					# print(env)
					self.create(env)
		elif self.options.delete:
			if self.args:
				if self.args[0] in self.kubernetes.keys() :
					self.delete(self.args[0])
				else:
					self.logging.error("The {0} isn't found!".format(self.args[0]))
					self.list()
			else:
				for env in self.kubernetes.keys():
					self.delete(env)
		elif self.options.replace:
			if self.args:
				if self.args[0] in self.kubernetes.keys() :
					self.replace(self.args[0])
			else:
				for env in self.kubernetes.keys():
					self.replace(env)
		elif self.options.upgrade:
			namespace = 'default'
			if self.options.namespace :
				namespace = self.options.namespace
			if self.args:
				project = self.args[0]
				image = self.options.upgrade
				self.upgrade(namespace,project,image)
			else:
				self.usage()
		elif self.options.export:
			self.export(self.options.export, self.args)
		else:
			if not self.args:
				self.usage()
