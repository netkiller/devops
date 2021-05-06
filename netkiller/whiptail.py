#-*- coding: utf-8 -*-
import os,subprocess

class Whiptail():
	
	def __init__(self,title = None, backtitle = ""):
		if title :
			self.t = '"'+ title +'"'
		if backtitle :
			self.backtitle = '"'+ backtitle +'"'
		else:
			backtitle = ""
		self.ismenu = False
	def title(self, tmp):
		self.t = tmp
		return(self)
	def inputbox(self, label, hight, width, init = ""):
		self.form = '--inputbox' + ' "'+label+'" ' +  str(hight) + ' ' + str(width) + ' '+init
		return(self)
	def passwordbox(self, label, hight, width):
		self.form = '--passwordbox' + ' "'+label+'" ' +  str(hight) + ' ' + str(width)
		return(self)
	def menu(self,lable, item, hight, width, listheight):
		menuitem = ''
		for i in item:
			key,value = i
			menuitem = menuitem + '"'+key + '" "' + value + '" '
		self.form = '--menu' + ' "'+lable+'" ' +  str(hight) + ' ' + str(width) + ' ' + str(listheight) +' '+ menuitem
		self.ismenu = True
		return(self)
	def yesno(self, text, hight, width):
		self.form = '--yesno' + ' "'+text+'" ' +  str(hight) + ' ' + str(width)
		return(self)
	def radiolist(self, text, height, width, listheight, item):
		radioitem = ''
		for i in item:
			tag, item, status = i
			radioitem = radioitem + '"'+tag + '" "' + item + '" "' + status + '" '
		self.radiolist = '--yesno' + ' "'+text+'" ' +  str(height) + ' ' + str(width) + ' ' + str(listheight) + ' ' + radioitem
		return(self)
	def run(self):
		screen = None
		#whiptail = 'whiptail ' + ' --title ' + self.t + ' ' + self.form + ' 3>&1 1>&2 2>&3'
		#screen = os.system(whiptail)
		whiptail = 'whiptail ' + ' --title ' + self.t + ' --backtitle ' + self.backtitle +' ' + self.form + ' 3>&2 2>&1 1>&3 | tee /tmp/.whiptail'
		#screen = subprocess.getoutput(whiptail)
		try:
			#screen = subprocess.call('/usr/bin/whiptail', whiptail, shell=True)
			#p = subprocess.check_output(['/usr/bin/whiptail',whiptail], stderr = subprocess.PIPE, shell=False, universal_newlines=True)
			
			#p = subprocess.Popen('/usr/bin/whiptail', whiptail, stderr = subprocess.PIPE, shell = False)   
			#p.stdin.write('3\n')   
			#p.stdin.write('4\n')   
			#screen = p.stdout.read() 
			#print(p)
			#screen = p.stderr.read() 	
			os.system(whiptail)
			f = open('/tmp/.whiptail','r')
			screen = f.read()
			f.close()
		except OSError as e:
			print(e)

		#print(whiptail)

		return(screen)
