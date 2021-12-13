###################################
# MySQL Backup & Restore
# Author: netkiller@msn.com
# Home:	http://www.netkiller.cn
###################################
#-*- coding: utf-8 -*-
import os,time
import logging, logging.handlers
from configparser import ConfigParser

class MySQL:
	def __init__(self):
		super().__init__()
		# self.config = ConfigParser()
		self.logging = logging.getLogger()

	def host(self, host):
		self.host = host
	def username(self, value):
		self.username = value
	def password(self, value):
		self.password = value
	def dbname(self, dbname):
		self.dbname = dbname

class MySQLDump(MySQL):
	def __init__(self, directory = None):
		super().__init__()
		umask = os.umask(0o077)
		if directory :
			self.directory(directory)
		self.opts = []
		self.gpg = None 
		self.gzip = False
	def directory(self, dir):
		if not os.path.isdir(dir) :
			os.makedirs(dir)
		self.directory = dir
		return self
	def host(self, host):
		super().host(host)
		self.opts.append('--host='+host)
		return self
	def databases(self, database):
		self.database = database
		if '--all-databases' in self.opts :
			self.opts.remove('--all-databases')
		if database.find(',') :
			self.opts.append('--databases '+self.database.replace(',',' '))
		else:	
			self.opts.append(self.database)
		return self
	def tables(self, database, table):
		# if database.find(' ') or database.find(','):
		# 	exit()
		# else:
		self.opts.append(databases+' '+table)
		return self
	def copies(self, day):
		self.copies = day
		return self
	def compress(self):
		self.opts.append('--compress')
		return self
	def events(self):
		self.opts.append('--events')
		return self
	def triggers(self):
		self.opts.append('--triggers')
		return self
	def routines(self):
		self.opts.append('--routines')
		return self
	def all_databases(self):
		self.opts.append('--all-databases')
		return self
	def single_transaction(self):
		self.opts.append('--single-transaction')
		return self
	def log_error(self, logfile):
		self.opts.append('--log-error='+logfile)
		return self
	def result_file(self, name):
		self.opts.append('--result-file='+name)
		return self
	def skip_lock_tables(self):
		self.opts.append('--skip-lock-tables')
		return self
	def column_statistics(self):
		self.opts.append('--column-statistics=0')
		return self
	def set_gtid_purged(self, value =  'OFF'):
		self.opts.append('--set-gtid-purged='+value)
		return self
	def default_character_set(self, value =  'utf8'):
		self.opts.append('--default-character-set='+value)
		return self	
	def no_data(self):
		self.opts.append('--no-data')
		return self	
	def cnf(self, clean = False):
		path = os.path.expanduser('~/.my.cnf')
		config = ConfigParser()
		if clean and os.path.exists(path):
			os.remove(path)
			exit()
		config['mysqldump'] = {
			'user': self.username,
			'password': self.password
		}
		config['mysql'] = {
			'user': self.username,
			'password': self.password
		}
		with open(path, 'w') as file:
			config.write(file)
		# self.opts.append('--defaults-file={0}'.format(path))
		# self.opts.append('--defaults-extra-file={0}'.format(path))
		return self
	def delete(self, day = None):
		if day :
			self.copies = day
		if self.copies :
			command = "find {directory} -type f -mtime +{copies} -delete".format(directory=self.directory, copies=self.copies)
			self.logging.debug(command)
			os.system(command)
	def Gzip(self):
		self.gpg = None
		self.gzip = True
	def GnuPG(self, recipient):
		self.gzip = False
		self.gpg = recipient
	def __command(self):
		cmd = []
		cmd.append('/usr/bin/mysqldump')
		opts = ' '.join(self.opts)
		cmd.append(opts)

		timepoint = time.strftime('%Y-%m-%d.%H:%M:%S',time.localtime(time.time()))
		output = self.directory + '/' + self.database.replace(' ','_') +'.' + timepoint

		if self.gzip :
			cmd.append('| gzip >')
			output += '.sql.gz'
			cmd.append(output)
		elif self.gpg :
			cmd.append('| gpg -r {userid} -e -o {output}.sql.gpg'.format(userid=self.gpg, output=output) )
			ext = '.sql.gpg'
		else:
			cmd.append('>')
			output += '.sql'
			cmd.append(output)

		command = ' '.join(cmd) 
		return command
	def execute(self):
		command = self.__command()
		self.logging.debug(command)
		os.system(command)
	