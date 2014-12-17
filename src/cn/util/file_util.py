#!usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014年12月9

@author: DuZhuo
'''
import os
import shutil
import logging
from cn.util.log_util import logging_init
logging_init()
# 判断分发目录是否有以.dat结尾的flag文件，如果有就进行备份分发，没有不执行操作        
def is_there_file(local_cata):
    try:
        local_files = os.listdir(local_cata)
        for local_file in local_files:
            if '.dat' in local_file:
                return True
    except BaseException,e:
        logging.exception(u'文件名读取失败：%s' % e)
    return False

#文件复制
def move_file(src,dst):
    try:
        shutil.copy(src, dst)
    except BaseException,e:
        logging.exception(u'文件备份失败：' % e)

#删除文件夹下所有文件
def delete_file(local_cata):
    shutil.rmtree(local_cata, True)
    os.mkdir(local_cata)
    
#初始化目录
def init_file():
    if not os.path.exists('/opt/app/mongodb/ftp/fenfa/'):
        os.makedirs('/opt/app/mongodb/ftp/fenfa/')
    if not os.path.exists('/opt/app/mongodb/ftp/pnrfile/pnrfile_apsis/'):
        os.makedirs('/opt/app/mongodb/ftp/pnrfile/pnrfile_apsis/')
    if not os.path.exists('/opt/app/mongodb/log/'):
        os.makedirs('/opt/app/mongodb/log/')
    if not os.path.exists('/opt/app/mongodb/log/flagname.log'):
        f = open('/opt/app/mongodb/log/flagname.log','w')
        f.close()
