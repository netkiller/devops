# Service 编排演示

```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

dockerfile = Dockerfile("neo")
dockerfile.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.show()
print('-'*60)

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")
neo.show()
print('-'*60)

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()

print('-'*60)
development.debug()
development.save('/tmp/neo.yaml')
```

输出演示

```text
FROM nginx:latest
VOLUME ["/etc/nginx","/var/log/nginx"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
------------------------------------------------------------
container_name: netkiller
build:
  context: .
  dockerfile: Dockerfile
image: netkiller:1.3.0

------------------------------------------------------------
services:
  netkiller:
    container_name: netkiller
    build:
      context: /Users/neo/GitHub/devops/doc/docker
      dockerfile: ./development/netkiller/Dockerfile
    image: netkiller:1.3.0
version: '3.9'

------------------------------------------------------------
{'services': {'netkiller': {'container_name': 'netkiller', 'build': {'context': '/Users/neo/GitHub/devops/doc/docker', 'dockerfile': './development/netkiller/Dockerfile'}, 'image': 'netkiller:1.3.0'}}, 'version': '3.9'}
```

## target 演示

设置 target 名称 init

```text
FROM nginx:latest AS init
COPY --from=init index.html /var/www
```

代码

```python
#!/usr/bin/python3
#-*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-07-24
##############################################
import os, sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module)
from netkiller.docker import *

target = 'init'

dockerfile = Dockerfile("neo",None,target)
dockerfile.image('nginx:latest',target).volume(['/etc/nginx','/var/log/nginx']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
dockerfile.copy('index.html','/var/www',target)
dockerfile.show()
print('-'*60)

neo = Services('netkiller')
neo.build(dockerfile)
neo.image("netkiller:1.3.0")
neo.show()
print('-'*60)

development = Composes('development')
development.version('3.9')
development.services(neo)
development.show()

print('-'*60)
development.debug()
# development.save('/tmp/neo.yaml')
```

输出演示

```text
FROM nginx:latest AS init
VOLUME ["/etc/nginx","/var/log/nginx"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
COPY --from=init index.html /var/www
------------------------------------------------------------
container_name: netkiller
build:
  context: .
  dockerfile: Dockerfile
  target: init
image: netkiller:1.3.0

------------------------------------------------------------
services:
  netkiller:
    container_name: netkiller
    build:
      context: /Users/neo/GitHub/devops/doc/docker
      dockerfile: ./development/netkiller/Dockerfile
    image: netkiller:1.3.0
version: '3.9'

------------------------------------------------------------
{'services': {'netkiller': {'container_name': 'netkiller', 'build': {'context': '/Users/neo/GitHub/devops/doc/docker', 'dockerfile': './development/netkiller/Dockerfile'}, 'image': 'netkiller:1.3.0'}}, 'version': '3.9'}

```