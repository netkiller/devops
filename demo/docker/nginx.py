import os,  sys
module = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0,module)

from netkiller.docker import *

nginx = Dockerfile() 
nginx.image('nginx:latest').volume(['/etc/nginx','/var/log/nginx','/opt']).run('apt update -y && apt install -y procps').expose(['80','443']).workdir('/opt')
nginx.show()

print("-" * 50)

redis = Dockerfile() 
redis.image('redis:latest').volume(['/var/lib/redis']).run('apt update -y && apt install -y procps iproute2').expose('6379').workdir('/var/lib/redis').entrypoint('redis-server').show()