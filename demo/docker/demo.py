from netkiller.docker import *
import os
import sys

module = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, module)


dockerfile = Dockerfile()
dockerfile.image('alpine:8').volume(['/srv']).run(
    'apt update -y && apt install -y procps net-tools iputils-ping iproute2 telnet'
).expose(['80', '443']).workdir('/srv')

image = Services('image')
image.build(dockerfile)
image.image('netkiller-devops:latest')

compose = Composes('demo')
compose.version('3.9')
compose.services(image)

if __name__ == '__main__':
    try:
        docker = Docker()
        docker.environment(compose)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
