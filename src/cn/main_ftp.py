#!usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014年12月8日

@author: DuZhuo
'''
from cn.ftp.ftp_apsis import updo_from_ftp
import time
if __name__ == '__main__':
    time.sleep(30)
    while True:
        updo_from_ftp()
        time.sleep(300)