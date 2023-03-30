import subprocess
# command = "docker run -it --rm --name pipeline -v ~/.m2:/root/.m2 -v /root/project:/tmp -w /root/project nginx:latext /bin/bash"
command = "/bin/ls"
p = subprocess.call(command, shell=True, stdin = subprocess.PIPE, stdout= subprocess.PIPE)
p.communicate()
# p.wait()
print(p.stdout.read())
p.stdin.write("echo Hello".encode('utf-8'))
p.stdin.flush()
print(p.stdout.read())