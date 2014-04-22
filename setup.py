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
	name='oscm',
	version=__version__,
	description="Collection of useful functions and classes",
	long_description=readme + '\n\n' + changes,
	keywords='oscm',
	author=__author__,
	author_email='netkiller@msn.com',
	url='http://netkiller.github.io',
	license='BSD',
	#py_modules=[
	#	'library.rsync',
	#	'library.whiptail'
	#],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.3',
	],
	package_dir={ '': 'library' },
	packages=[
		''
	],
	scripts=[
		'bin/deployment',
		'bin/backup',
		'bin/mysqlshell',
		'bin/auditlog'
	],
	data_files = [
		('etc', ['etc/deployment.cfg']),
		('etc', ['etc/task.cfg']),
		('etc', ['etc/schedule.cfg']),
		('log', ['log/deployment.log']),
		('project', ['project/exclude','project/testing','project/production','project/development'])
	]
)

