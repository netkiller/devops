docker pull jenkins/jenkins:lts

#docker run -d \
#-p 8080:8080 \
#-p 50000:50000 \
#--name jenkins \
#--link gitlab:gitlab.bill.com \
#-u root \
#-v ~/jenkins:/var/jenkins_home  \
#-v /usr/share/maven:/usr/local/maven \
#-v /usr/lib/jvm/jdk1.8:/usr/local/jdk 
#jenkins/jenkins:latest

docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

docker logs -f jenkins