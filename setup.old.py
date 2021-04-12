import os,sys
from distutils.core import setup
#from setuptools import setup
sys.path.insert(0, os.path.abspath('lib'))
from library import __version__, __author__
#print (__version__)
readme = open('README.md').read()
changes = open('CHANGES.txt').read()
#version_file = 'oscm.py'
#version = re.findall("__version__ = '(.*)'", open(version_file).read())[0]
#try:
#	 version = __import__('utile').git_version(version)
#except ImportError:
#	 pass

setup(
	name='netkiller-devops',
	version=__version__,
	description="DevOps of useful deployment and automation",
	long_description=readme + '\n\n' + changes,
	keywords='devops',
	author=__author__,
	author_email='netkiller@msn.com',
	url='http://netkiller.github.io',
	license='MIT',
	#py_modules=[
	#	'library.rsync',
	#	'library.whiptail'
	#],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.4',
	],
	package_dir={ '': 'library' },
	packages=[
		''
	],
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

