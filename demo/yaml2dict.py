import yaml

yamlText ='''
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user  
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system'''

yamlText ='''
volumes:
  redis: 
  mysql:
'''
print(yamlText)
print(type(yamlText))
# Yaml -> Dict
dictText = yaml.load(yamlText,Loader=yaml.FullLoader)
print(dictText)
print(type(dictText))
