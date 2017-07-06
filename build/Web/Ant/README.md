# build.xml

This is an ant build.xml.

## Workflow

	git ---> clone | pull ---> branch ---> local ---> build ---> config ---> deploy ---> remote
	local ---> start | stop | kill | status ---> remote

## Download Script

	wget https://raw.githubusercontent.com/oscm/build/master/Web/Ant/build.xml
	wget https://raw.githubusercontent.com/oscm/build/master/Web/Ant/build.properties
	
## Setup and config

	<property name="git.repository" value="git@git.netkiller.cn:example.com/admin.example.com.git" />
	<property name="git.branch" value="master" />
	<property name="git.merge" value="development" />

	<property name="remote" value="www@172.16.0.1" />
	<property name="destination" value="/www/example.com/admin.example.com" />
	
## Deploy

### trial
	$ ant pull trial
	
### Deploy

	$ ant pull deploy

### merge and push 

	$ ant merge
	$ ant push
	
	or 
	
	$ ant push

### revert to reversion

	$ vim build.xml 
	<property name="git.revert" value="your version" />
	
	$ ant revert
	$ ant deploy

### Only compile, not deploy

	$ ant compile
	
### package
	$ ant package

	
	
## Other 

### Clone 

	$ ant clone
	
### Pull
	$ ant pull 

### backup
	$ ant backup
	
### reset / clean

	$ ant clean
	$ ant reset




