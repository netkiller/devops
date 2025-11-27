from netkiller.docker import *

minio = Services('minio')
minio.image('minio/minio:latest')
minio.container_name('minio')
minio.restart('always')
minio.hostname('minio.netkiller.cn')
minio.environment([
    'TZ=Asia/Shanghai', 'MINIO_ROOT_USER=admin', 'MINIO_ROOT_PASSWORD=123456',
    'MINIO_ACCESS_KEY=minio', 'MINIO_SECRET_KEY=minio123456'
])
minio.ports(['9000:9000', '9090:9090'])
minio.volumes([
    # '/opt/minio/data:/data',
    # '/opt/minio/config:/root/.minio'
    '/tmp/minio:/data'
])
# minio.command("server --console-address ':9090' /data")
minio.command("server /data")
minio.privileged()

compose = Composes('storage')
compose.version('3.9')
compose.services(minio)

if __name__ == "__main__":
    try:
        docker = Docker()
        docker.environment(compose)
        docker.main()
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")

# runner = Services('gitlab-runner')
# runner.image('gitlab/gitlab-runner:alpine')
# runner.container_name('gitlab-runner')
# runner.restart('always')
# runner.hostname('gitlabrunner.netkiller.cn')
# # runner.extra_hosts(extra_hosts)
# runner.environment(['TA=Asia/Shanghai'])
# # runner.ports(['80:80','443:443'])
# runner.volumes(['./gitlab/config:/etc/gitlab-runner','/var/run/docker.sock:/var/run/docker.sock','/usr/bin/docker:/usr/bin/docker'])
# runner.privileged(True)