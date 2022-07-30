from netkiller.docker import *

dockerfile = Dockerfile()
dockerfile.image('openjdk:8').volume(['/srv']).run(
    'apt update -y && apt install -y procps net-tools iputils-ping iproute2 telnet'
).expose(['80', '443']).workdir('/srv')

image = Services('image')
image.build(dockerfile)
image.image('netkiller:openjdk8')


demo = Composes('demo')
demo.version('3.9')
demo.services(image)
# demo.build('')

if __name__ == "__main__":
    try:
        docker = Docker()
        # docker.env({'DOCKER_HOST':'ssh://root@192.168.30.13','COMPOSE_PROJECT_NAME':'experiment'}) 
        docker.environment(demo)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")