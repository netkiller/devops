from netkiller.docker import Services, Composes,  Common

nginx = Services("nginx")
# 基于什么镜像
nginx.image('nginx:latest')
# 挂载卷
nginx.volumes(['/etc/nginx','/var/log/nginx','/opt'])
# 运行脚本
nginx.command('apt update -y && apt install -y procps')
# 暴漏端口
nginx.expose(['80','443'])
nginx.networks("testnet")
nginx.restart(Common.Restart.always)
# 工作目录
nginx.working_dir('/opt')
# 日志切割
nginx.logging({'options':{'max-size': "100m",'max-file': "3"}})
nginx.healthcheck(
    {
      'test': " ".join(["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://127.0.0.1:80"]),
      'interval': '10s',
      'timeout': '5s',
      'retries': 3,
      'start_period': '5s'}
)
# nginx.dump()

demo = Composes('demo')
# demo.version('3.9')
demo.services(nginx)
demo.dump()