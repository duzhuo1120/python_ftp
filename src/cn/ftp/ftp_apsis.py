#!usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014年12月8日

@author: DuZhuo
'''
import os
import time
import logging
import datetime
from ftplib import FTP
from cn.util.log_util import logging_init
from cn.util.file_util import is_there_file
from cn.util.file_util import move_file
from cn.util.file_util import delete_file
from cn.util.file_util import init_file

logging_init()
# 初始化
def ftp_init(host,port,user,pwd):
    try:
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(host, port)
        ftp.login(user, pwd)
        logging.info(u'连接%s成功' % host)
    except BaseException,e:
        raise BaseException(u'%s连接失败：%s' % (host,e))
    return ftp

#主程序
def updo_from_ftp():
    logging.info(u'轮训任务开始')
    local_cata = '/opt/app/mongodb/ftp/fenfa/'
    #初始化目录
    init_file()
    #先下载232上面的文件
    ftp_down_rsv(local_cata)
    # 判断分发目录是否有以.dat结尾的flag文件，如果有就进行备份分发，没有不执行操作
    if is_there_file(local_cata):
        logging.info(u'发现新的数据包，开始分发备份')
        for local_file in os.listdir(local_cata):
            move_file(os.path.join(local_cata,local_file),'/opt/app/mongodb/ftp/pnrfile/pnrfile_apsis/')
        ftp_up('10.6.186.10', '21', 'ftp101', 'ftp101', local_cata, '/pnrfile/')
        ftp_up('10.6.186.33', '21', 'ftp101', 'ftp101', local_cata, '/')
        ftp_up('10.6.186.33', '21', 'ZJ_GAJ', 'ZJ_GAJ', local_cata, '/RES/')
        ftp_up('10.6.186.33', '21', 'pek06', 'ftp101', local_cata, '/pek06/')
        ftp_up('10.6.157.93', '21', 'asi', 'asi', local_cata, '/')
        logging.info(u'备份分发数据包完成')
    #分发完成后删除本地文件
    delete_file(local_cata)
    logging.info(u'轮训任务结束')

# 下载232上面的文件
# cata本地目录
def ftp_down_rsv(cata):
    try:
        ftp = ftp_init('10.6.168.232','21','apsisftp','tEx2XIF8')
    except BaseException:
        return
    today_file_name = 'FuturePNR_%s.txt.Z' % get_date()
    flag_file_name = 'FuturePNRflag_%s.dat' % get_date()
    if is_down(today_file_name):
        logging.info(u'今天的数据包已经下载')
        ftp.set_debuglevel(0)
        ftp.quit()
        return
    else:
        file_lists = ftp.nlst()
        ftp.set_debuglevel(0)
        ftp.quit()
        try:
            file_lists.index(today_file_name)
            file_lists.index(flag_file_name)
            logging.info(u'发现需要下载的数据包！等待5分钟后开始下载...')
            time.sleep(300)
            try:
                ftp_up = ftp_init('10.6.168.232','21','apsisftp','tEx2XIF8')
            except BaseException:
                return
            today_file_handle = open(os.path.join(cata,today_file_name), 'wb').write
            ftp_up.retrbinary('RETR %s' % today_file_name, today_file_handle)
            flag_file_handle = open(os.path.join(cata,flag_file_name), 'wb').write
            ftp_up.retrbinary('RETR %s' % flag_file_name, flag_file_handle)
            logging.info(u'数据包下载成功')
            #把已经下载的FLAG文件名写进记录文件
            write_into_file(today_file_name)
            #删除33服务器上民航信息中心ftp目录下和pek06 ftp目录下的文件
            del_file_tt()
        except ValueError:
            logging.info(u'数据包不存在')
            return
        except BaseException,e:
            logging.exception(u'下载出错：%s' % e)
        finally:
            ftp_up.set_debuglevel(0)
            ftp_up.quit()

#获取当前日期 如：20141112
def get_date():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')

#判断文件中是否有该名字
def is_down(file_name):
    flag = False
    try:
        f = open('/opt/app/mongodb/log/flagname.log','r')
        f_name =  f.read()
    except BaseException,e:
        logging.exception(u'读取/opt/app/mongodb/log/flagname.log失败：%s' % e)
    finally:
        f.close()
    if f_name == '':
        logging.info(u'/opt/app/mongodb/log/flagname.log中没有记录,下载今天的数据包，并往flagname.log中存入今天的记录')
    if f_name == file_name:
        flag = True
    return flag

#把已经下载的FLAG文件名写进记录文件
def write_into_file(file_name):
    flag = False
    try:
        f = open('/opt/app/mongodb/log/flagname.log','w')
        f.write(file_name)
        flag = True
    except BaseException,e:
        logging.exception(u'/opt/app/mongodb/log/flagname.log写入出错：%s' % e)
    finally:
        f.close()
    return flag

#删除33服务器上民航信息中心ftp目录下和pek06 ftp目录下的文件
def del_file_tt():
    try:
        ftp = ftp_init('10.6.186.33','21','ZJ_GAJ','ZJ_GAJ')
    except BaseException:
        return
    ftp.cwd('/RES/')
    files = ftp.nlst()
    if files != None and len(files)>0:
        for file_name in files:
            ftp.delete(file_name)
    try:
        ftp_pe = ftp_init('10.6.186.33','21','pek06','ftp101')
    except BaseException:
        return
    ftp_pe.cwd('/pek06/')
    files_pe = ftp_pe.nlst()
    if files_pe != None and len(files_pe)>0:
        for file_name in files_pe:
            ftp_pe.delete(file_name)

    
# 批量上传
# cata目录
def ftp_up(host,port,user,pwd,local_cata,ftp_cata):
    try:
        ftp = ftp_init(host,port,user,pwd)
        ftp.cwd(ftp_cata)
        for local_file in os.listdir(local_cata):
            file_handle = open(os.path.join(local_cata,local_file), 'rb')  # 读取本地文件
            ftp.storbinary('STOR %s' % os.path.basename(local_file), file_handle)  # 上传
    except IOError,e:
        logging.exception(u'文件上传失败:%s' % e)
    except BaseException:
        return
    finally:
        ftp.set_debuglevel(0)
        file_handle.close()
        ftp.quit()