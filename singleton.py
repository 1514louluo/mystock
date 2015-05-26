# -*- coding:utf-8 -*-
#!/bin/python

'''
	author: manialuo
	单例模式
'''
class singleton(type):  
    def __init__(cls, name, bases, dict):  
        super(singleton, cls).__init__(name, bases, dict)  
        cls._instance = None  
    def __call__(cls, *args, **kw):  
        if cls._instance is None:  
            cls._instance = super(singleton, cls).__call__(*args, **kw)  
        return cls._instance  
