#-*- coding: utf-8 -*-
import curses
import select
import os
import sys
import urllib2
import locale  
from config import *

locale.setlocale(locale.LC_ALL, 'zh_CN.utf8')

def init_env():
    return curses.initscr()

def display_info(stdscr, str, x, y, colorpair=1):
    '''使用指定的colorpair显示文字'''
    stdscr.addstr(x, y, '                                                                 ', curses.color_pair(colorpair))
    stdscr.refresh()
    stdscr.addstr(x, y, str, curses.color_pair(colorpair))
    stdscr.refresh()

def get_ch_and_continue(stdscr):
    '''演示press any key to continue'''
    #设置nodelay，为0时会变成阻塞式等待
    stdscr.nodelay(0)
    #输入一个字符
    ch=stdscr.getch()
    #重置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)
    return True

def set_win(stdscr):
    '''控制台设置'''
    #使用颜色首先需要调用这个方法
    curses.start_color()
    #文字和背景色设置，设置了两个color pair，分别为1和2
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #关闭屏幕回显
    curses.noecho()
    #输入时不需要回车确认
    curses.cbreak()
    #设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)

def unset_win(stdscr):
    '''控制台重置'''
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    curses.echo()
    #结束窗口
    curses.endwin()

def getreply(url):
	
	response = urllib2.urlopen(url)
	html = response.read().decode('gb2312').encode('utf-8')
	return html


def getkey(mytuple):
	return mytuple[2]

def print_stock(stdscr,stocklist):
#    stocklist=['sz002276','sz000656','sh601166']
#    stocks=','.join(stocklist)
    url = 'http://hq.sinajs.cn/list='+stocklist

    html = getreply(url)
    #print html
    linelist=html.split(';')
    #print linelist
	
    stockinfolist=[]
    for line in linelist:
    	line=line[4:-1]
    	kvlist=line.split('=')
    	if len(kvlist)<2:
    		continue
    	#print kvlist
    	dataline=kvlist[1]
    	datalist=dataline.split(',')
    	name=datalist[0][1:100]
    	current=datalist[3]
    	percent=(float(datalist[3])-float(datalist[2]))/float(datalist[2])*100
    	stockinfolist.append((name,current,percent))

#    print '  name     current     percent'
    display_info(stdscr, '  name     current     percent', 0, 0)

    linenb = 1
    sortedstock=sorted(stockinfolist,None,getkey,True)
    for info in sortedstock:
	    name=info[0]
	    current=info[1]
	    percent=info[2]
	    if len(name)==3:
	        name=name+'  '
	    if percent<0:
	        strpercent=str(percent)[0:5]+'%'
			
	    else:
	        strpercent=' '+str(percent)[0:4]+'%'

#	    print name,'  ',current, '   ',strpercent
	    mystockinfo = name+'  '+current+ '   '+strpercent
	    if '-' == strpercent[0]:
                display_info(stdscr, mystockinfo, linenb, 0, 1)
            else:
                display_info(stdscr, mystockinfo, linenb, 0, 2)
            linenb+=1


if __name__=='__main__':
    path = './mystock.conf'
    if 1 >= len(sys.argv):
        print 'use default conf!'
    else:
        path = sys.argv[1]
    if 0 == len(path) or False == os.path.isfile(path):
        print 'wrong conf path!'
        sys.exit(0)
    myconfig=config_module(path)
    stocklist = myconfig.get_string("stock", "stockid", '')
    if 0 == len(stocklist):
        print 'empty stockid'
        sys.exit(0)

    pertime = myconfig.get_int("stock", "pertime", 1)

    stdscr = init_env()
    set_win(stdscr)
    i = 0
    while 1:
        infds,outfds,errfds = select.select([0,],[],[],pertime) 
        if 0 < len(infds):
            break
#        display_info(stdscr, 'Hola, curses!'+str(i), 0, 0)
        print_stock(stdscr, stocklist)
        i+=1
    get_ch_and_continue(stdscr)
    unset_win(stdscr)


