Spring boot
=====

spring boot 1.5.6

## Install build.xml

    mkdir deployment
    cd deployment
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/build.xml -O /usr/local/etc/build.xml
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/build.properties -O /usr/local/etc/build.properties
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/deployment -O /usr/local/bin/deployment

	chmod +x /usr/local/bin/deployment
	
## Common config
    cd 
	cat common.properties
	git.repository=git@58.96.11.168:netkiller.cn/api.netkiller.cn.git
	remote.java.home=/srv/java
	remote.host=www@www.netkiller.cn
	remote.destination=/www/netkiller.cn/www.netkiller.cn

## Stage config

	cat development.properties
	git.branch=testing
	git.merge=development
	
## Deploy

	./deployment <stage> <target>
	
	for example:
	./deployment development deploy start
