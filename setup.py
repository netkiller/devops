import os,sys
from setuptools import setup,find_packages
sys.path.insert(0, os.path.abspath('lib'))
from netkiller import __version__, __author__

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
	name="netkiller-devops",
	version="0.1.2",
	author="Neo Chen",
	author_email="netkiller@msn.com",
	description="DevOps of useful deployment and automation",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/oscm/devops",
	license='BSD',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',      
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires = ['pyyaml'],
  	# package_dir={ '': 'library' },
	packages=find_packages(),

	scripts=[
		'bin/deployment',
		'bin/backup',
		'bin/osconf',
		'bin/mysqlshell',
		'bin/chpasswd.sh',
		'bin/gitsync'
	],
	data_files = [
		('etc', ['etc/deployment.cfg']),
		('etc', ['etc/task.cfg']),
		('etc', ['etc/schedule.cfg']),
		('etc', ['etc/os.ini']),
		#('log', ['log/deployment.log']),
		('share', ['share/example/testing/example.com.ini']),
		('share', ['share/profile.d/devops.sh'])
		#('example/testing', ['example/testing/example.com.ini']),
		#('example/config/testing', ['example/config/testing/www.example.com.ini']),
		#('example/exclude/testing', ['example/exclude/testing/www.example.com.lst'])
		
	]
)