
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString as pss

x = pss("""\
external_url 'https://gitlab.example.com'
gitlab_rails['time_zone'] = 'Asia/Shanghai'
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.aliyun.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "netkiller@msn.com" 
gitlab_rails['smtp_password'] = "******"
gitlab_rails['smtp_domain'] = "aliyun.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = true
gitlab_rails['gitlab_email_from'] = 'netkiller@msn.com'
gitlab_rails['gitlab_shell_ssh_port'] = 22
""")

yaml = YAML()

yaml.dump(dict(a=1, b='hello world', c=x), sys.stdout)