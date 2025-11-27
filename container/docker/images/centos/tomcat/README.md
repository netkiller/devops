# Centos 7 + Server Jre + Tomcat 8.5.15

## for testing

	docker build -t "centos:tomcat" .

	docker run --name my-centos-tomcat -d centos:tomcat
	
	docker exec -it my-centos-tomcat /bin/bash
	
## for production

	instance=www.netkiller.cn
	mkdir -p /var/log/tomcat/${instance}
	docker image rm -f centos:tomcat
	docker build -t "centos:tomcat" .
	docker rm ${instance} -f
	docker run --rm --name ${instance} \
	-v /var/log/tomcat/${instance}:/srv/tomcat/logs:rw \
	-v /www/${instance}:/srv/tomcat/webapps/ROOT:ro \
	-p 8080:8080 -d centos:tomcat
	docker exec -it ${instance} /bin/bash