#-*-coding:UTF-8-*-
#!/bin/python
'''
	abcauthor: manialuo
	desc:   配置文件解析
'''

import singleton
import ConfigParser
#import singleton

class config_module(object):
	__metaclass__ = singleton.singleton	

	def __init__(self, conf_path):
		self.config_dict={}
		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(conf_path,"rb"))
	
	def get_string(self, section, field, default):
		if False == self.config.has_option(section, field):
			return default
		key = '_'.join((section, field))
		if False == self.config_dict.has_key(key):
			value = self.config.get(section,field)
			self.config_dict[key]=value
			return value
		else:
			return self.config_dict[key]
		
	def get_int(self, section, field, default):
		if False == self.config.has_option(section, field):
			return default
		key = '_'.join((section, field))
		if False == self.config_dict.has_key(key):
			value = int(self.config.get(section,field))
			self.config_dict[key] = value
			return value
		else:
			return self.config_dict[key]
		
	def get_long(self, section, field, default):
		if False == self.config.has_option(section, field):
			return default
		key = '_'.join((section, field))
		if False == self.config_dict.has_key(key):
			value = long(self.config.get(section,field))
			self.config_dict[key] = value
			return value
		else:
			return self.config_dict[key]

	def get_float(self, section, field, default):
		if False == self.config.has_option(section, field):
			return default
		key = '_'.join((section, field))
		if False == self.config_dict.has_key(key):
			value = float(self.config.get(section,field))
			self.config_dict[key] = value
			return value
		else:
			return self.config_dict[key]


if __name__=='__main__':
	myconfig=config_module("./1")
	print myconfig.get_int("my", "love", -32)
	print myconfig.get_long("my", "love2", 32323232233)
	print myconfig.get_float("my", "love3", 3232.4343)
	print myconfig.get_string("my", "love1", "jfjdsf")















