Spring boot
=====

spring boot 1.5.6

## Install build.xml

    mkdir deployment
    cd deployment
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/build.xml
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/build.properties
	wget https://raw.githubusercontent.com/oscm/devops/master/build/Application/Springboot/deployment
	
	chmod +x deployment
	
## Common config

	cat build.properties
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
