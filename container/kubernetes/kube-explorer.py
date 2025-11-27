import os
import sys
import time

sys.path.insert(0, '/Users/neo/workspace/devops')

from netkiller.kubernetes import *

namespace = 'default'
name = 'kube-explorer'
labels = {'app': name}
annotations = {}
replicas = 1
containerPort = 80
image = 'cnrancher/kube-explorer:latest'
monitor = '/dashboard'
livenessProbe = {}
readinessProbe = {}
limits = {}

compose = Compose('test', 'k3s.yaml')

config = ConfigMap()
config.metadata().name(name).namespace(namespace)
config.from_file('k3s.yaml', 'k3s.yaml')
compose.add(config)

deployment = Deployment()
deployment.metadata().name(name).labels(labels).namespace(namespace)
deployment.metadata().annotations(annotations)
deployment.spec().replicas(replicas)
deployment.spec().progressDeadlineSeconds(10)
deployment.spec().revisionHistoryLimit(10)
deployment.spec().selector({'matchLabels': {'app': name}})
# deployment.spec().strategy().type('RollingUpdate').rollingUpdate(1, 0)
deployment.spec().template().metadata().labels({'app': name})

livenessProbe = {
    'failureThreshold': 3,
    'httpGet': {
        'path': monitor,
        'port': containerPort,
        'scheme': 'HTTP'
    },
    'initialDelaySeconds': 60,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}
readinessProbe = {
    'failureThreshold': 3,
    'httpGet': {
        'path': monitor,
        'port': containerPort,
        'scheme': 'HTTP'
    },
    'initialDelaySeconds': 30,
    'periodSeconds': 10,
    'successThreshold': 1,
    'timeoutSeconds': 5
}

# limits = {'limits': {
# 	# 'cpu': '500m',
# 	'memory': '1Gi'}, 'requests': {
# 		# 'cpu': '500m',
# 	'memory': '1Gi'}}

deployment.spec().template().spec().containers().name(name).image(image).ports(
    [{
        'containerPort': containerPort
    }]).imagePullPolicy('IfNotPresent').volumeMounts([
        {
            'name': 'config',
            'mountPath': '/etc/rancher/k3s/k3s.yaml',
            'subPath': 'k3s.yaml'
        },
    ]).resources(limits).livenessProbe(livenessProbe).readinessProbe(
        readinessProbe).env([
            # {
            #     'name': 'CONTEXT',
            #     'value': '/dashboard'
            # },
            {
                'name': 'KUBECONFIG',
                'value': '/etc/rancher/k3s/k3s.yaml'
            },
        ]).command([
            'kube-explorer', '--kubeconfig=/etc/rancher/k3s/k3s.yaml',
            '--http-listen-port=80', '--https-listen-port=0'
        ])
# ,'--ui-path=/dashboard'
# --context value              [$CONTEXT]
deployment.spec().template().spec().restartPolicy(Define.restartPolicy.Always)
# deployment.spec().template().spec().nodeSelector({'group': 'backup'})
# deployment.spec().template().spec().dnsPolicy(Define.dnsPolicy.ClusterFirst)
deployment.spec().template().spec().volumes([{
    'name': 'config',
    'configMap': {
        'name': name
    }
}])
compose.add(deployment)

service = Service()
service.metadata().namespace(namespace)
service.spec().selector({'app': name})
service.metadata().name(name)
service.spec().type(Define.Service.ClusterIP)
service.spec().ports({
    'name': 'http',
    'protocol': 'TCP',
    'port': 80,
    'targetPort': containerPort
})
compose.add(service)

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name(name)
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
pathType = Define.Ingress.pathType.Prefix

ingress.spec().rules([{
    # 'host': vhost['host'],
    'http': {
        'paths': [{
            'path': '/dashboard/',
            'pathType': pathType,
            'backend': {
                'service': {
                    'name': name,
                    'port': {
                        'number': 80
                    }
                }
            }
        }, {
            'path': '/v1/',
            'pathType': pathType,
            'backend': {
                'service': {
                    'name': name,
                    'port': {
                        'number': 80
                    }
                }
            }
        }, {
            'path': '/k8s/',
            'pathType': pathType,
            'backend': {
                'service': {
                    'name': name,
                    'port': {
                        'number': 80
                    }
                }
            }
        }, {
            'path': '/apis/',
            'pathType': pathType,
            'backend': {
                'service': {
                    'name': name,
                    'port': {
                        'number': 80
                    }
                }
            }
        }, {
            'path': '/api/',
            'pathType': pathType,
            'backend': {
                'service': {
                    'name': name,
                    'port': {
                        'number': 80
                    }
                }
            }
        }]
    }
}])

compose.add(ingress)

kubernetes = Kubernetes()
kubernetes.compose(compose)

# kubernetes.debug()
# kubernetes.environment({'test': 'k3s.yaml', 'pre': 'abgrey.yaml'})
kubernetes.main()
