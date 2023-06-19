# coding:utf-8
import sys
import time

from config import DB_CONFIG
from util.exception import Con_DB_Fail

import config


try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from db.MongoHelper import MongoHelper as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
        from db.RedisHelper import RedisHelper as SqlHelper
    else:
        from db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception as e:
    raise Con_DB_Fail


def store_data(queue2, db_proxy_num):
    '''
    读取队列中的数据，写入数据库中
    :param queue2:
    :return:
    '''
    successNum = 0
    failNum = 0
    while True:
        try:
            proxy = queue2.get(timeout=300)
            if proxy:
                # print(f'store_data 检测speed:{proxy},{proxy['speed']}', )
                flag = False
                if proxy['area'].strip()[:2] in config.CHINA_AREA:
                    flag = True if proxy['speed'] < config.FILTER_SPEED else False
                else:
                    flag = True if proxy['speed'] < config.FOREIGN_FILTER_SPEED else False

                if flag:
                    proxy['lasttime'] = int(time.time())
                    sqlhelper.insert(proxy)
                    successNum += 1
            else:
                failNum += 1
            str = 'IPProxyPool-----> Success ip num :{}, Fail ip num:{}'.format(successNum, failNum)
            sys.stdout.write(str + "\r")
            sys.stdout.flush()
        except BaseException as e:
            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value = 0
                print('store_data e:',e)
                str = '1 IPProxyPool-----> eSuccess ip num :%d, Fail ip num:%d' % (successNum,failNum)
                sys.stdout.write(str + "\r")
                sys.stdout.flush()
                successNum = 0
                failNum = 0
