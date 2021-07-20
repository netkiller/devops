# INSTALL

## Download Script

	wget https://raw.githubusercontent.com/oscm/build/master/Web/Ant/build.xml
	wget https://raw.githubusercontent.com/oscm/build/master/Web/Ant/build.properties
	wget https://raw.githubusercontent.com/oscm/build/master/Web/Ant/deployment
	chmod +x deployment

## Common config (Global config)

	$ cat build.properties
	git.repository=git@git.netkiller.cn:netkiller.cn/www.netkiller.cn.git
	remote.host=www@www.netkiller.cn
	remote.destination=/srv/www/netkiller.cn/www.netkiller.cn
	catalina.home=/srv/apache-tomcat/www.netkiller.cn

	or

	<property name="git.repository" value="git@git.netkiller.cn:netkiller.cn/www.netkiller.cn.git" />
	<property name="destination" value="/www/netkiller.cn/www.netkiller.cn" />
	<property name="catalina.home" value="/srv/apache-tomcat/www.netkiller.cn" />

## branch config
	
	$ touch development.properties
	$ vim development.properties

	```
git.branch=development
git.merge=
remote.host=www@www.netkiller.cn
	```

## Deploy

### trial
	$ deployment development pull trial
	
### Deploy

	$ deployment development pull deploy

### merge and push 

	$ deployment development merge
	$ deployment development push
	
	or 
	
	$ deployment development push

### revert to reversion

	$ vim build.xml
	<property name="git.revert" value="your version" />
	
	$ deployment development revert
	$ deployment development deploy

### Only compile, not deploy

	$ deployment development compile
	
### package
	$ deployment development package

	
	
## Other 

### Clone 

	$ deployment development clone
	
### Pull
	$ deployment development pull 

### backup
	$ deployment development backup
	
### reset / clean

	$ deployment development clean
	$ deployment development reset




