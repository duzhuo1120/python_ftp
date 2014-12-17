__author__ = 'Chris'

import logging
import os

def logging_init():
    #logging.basicConfig(filename=os.path.join(get_log_path(), 'log.txt'), level=logging.DEBUG)
    if not os.path.exists('/bko/log/'):
        os.makedirs('/bko/log/')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s]: %(message)s',
                        datefmt='"%Y-%m-%d %H:%M:%S"',
                        filename=os.path.join('/bko/log/', 'ftpwork.log'),
                        #filemode='w'
                        )
