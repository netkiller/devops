###################################
# MongoDB Backup & Restore
# Author: netkiller@msn.com
# Home:	http://www.netkiller.cn
###################################
#-*- coding: utf-8 -*-
import os,time
import logging, logging.handlers
from configparser import ConfigParser
from logging import getLogger

class Mongo:
	def __init__(self):
		super().__init__()
		self.logging = getLogger()
		self.port = 27017

	def host(self, host = 'localhost'):
		self.host = host
		return self
	def port(self,port = 27017):
		self.port = port
		return self
	def username(self, value):
		self.username = value
		return self
	def password(self, value):
		self.password = value
		return self
	def authenticationDatabase(self, value):
		self.authenticationDatabase = value
		return self
	def db(self, db):
		self.db = db
		return self
	def collection(self, value):
		self.collection = value
		return self
	def uri(self):
		# uri = "mongodb://{username}:{password}@{host}:{port}/{db}".format(username=self.username,password=self.password,host=self.host,port=self.port,db=self.db)
		uri = "mongodb://{username}@{host}:{port}/{db}".format(username=self.username,host=self.host,port=self.port,db=self.db)
		return uri

class MongoDump(Mongo):
	def __init__(self):
		super().__init__()
		umask = os.umask(0o077)
		self.opts = []
		
	def out(self, directory):
		self.directory = directory
		if not os.path.isdir(self.directory) :
			os.makedirs(self.directory)
		self.opts.append('--out={0}'.format(self.directory))
		self.logging.info('Backup directory %s', self.directory)
		return self
	def archive(self, archive):
		if archive :
			self.archive = archive
			if archive == '-' :
				self.opts.append('--archive')
			else:	
				self.opts.append('--archive=%s' % self.archive)
		else:
			self.archive = self.db + '-' +time.strftime('%Y-%m-%d.%H:%M:%S',time.localtime(time.time()))
		self.logging.info('Archive directory %s', self.archive)
		return self
	# def databases(self, database):
	# 	self.database = database
	# 	if '--all-databases' in self.opts :
	# 		self.opts.remove('--all-databases')
	# 	if database.find(',') :
	# 		self.opts.append('--databases '+self.database.replace(',',' '))
	# 	else:	
	# 		self.opts.append(self.database)
	# 	return self
	# def tables(self, database, table):
	# 	# if database.find(' ') or database.find(','):
	# 	# 	exit()
	# 	# else:
	# 	self.opts.append(databases+' '+table)
	# 	return self
	def quiet(self):
		self.opts.append('--quiet')
		return self
	def dumpDbUsersAndRoles(self):
		self.opts.append('--dumpDbUsersAndRoles')
		return self
	def excludeCollection(self, value):
		self.opts.append('--excludeCollection='+value)
		return self
	def collection(self, value):
		self.opts.append('--collection='+value)
		return self	
	def config(self, clean = False):
		path = os.path.expanduser('~/.mongo.yaml')
		if clean and os.path.exists(path):
			os.remove(path)
			exit()
		with open(path, 'w') as file:
			file.write('password: %s\n' % self.password)
		self.opts.append('--config={0}'.format(path))
		return self
	def copies(self, day):
		self.copies = day
		return self
	def delete(self, day = None):
		if day :
			self.copies = day
		if self.copies :
			command = "find {directory} -type f -mtime +{copies} -delete".format(directory=self.directory, copies=self.copies)
			self.logging.debug(command)
			os.system(command)

	def gzip(self, status = True):
		if status :
			self.opts.append('--gzip')
	def GnuPG(self, recipient, output):
		if not os.path.isdir(os.path.dirname(output)) :
			os.makedirs(os.path.dirname(output))
		self.opts.append('--archive')
		self.opts.append('| gpg -r {recipient} -e -o {output}.mongo.gpg'.format(recipient=recipient, output=output) )
		self.logging.info('GnuPG output %s', output)
		return self
	def __command(self):
		cmd = []
		cmd.append('mongodump')
		cmd.append('--uri="%s"' % self.uri())
		opts = ' '.join(self.opts)
		cmd.append(opts)
		command = ' '.join(cmd) 
		return command
	def execute(self):
		command = self.__command()
		self.logging.debug(command)
		os.system(command)

# dump = MongoDump()
# dump.host('192.168.30.5').username('sfzito').password('sfzito').authenticationDatabase('sfzito').db('sfzito')
# print(dump.uri())	