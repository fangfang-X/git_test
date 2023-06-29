# -*-coding:UTF-8-*-
#import sys, MySQLdb, traceback
#MySQLdb supports maximum version is python3.4, so we use pymysql 
import pymysql
import time
import logging

LOG_LEVEL = logging.INFO
def logger_init(LOG_LEVEL):
    logger = logging.getLogger('mylogger.c')
    #set log level WARNING
    logger.setLevel(LOG_LEVEL)
    return logger

logger = logger_init(LOG_LEVEL)

class mysql:
    def __init__(self,
                 host='',
                 user='',
                 passwd='',
                 db='',
                 port=3306,
                 charset='utf8'
                 ):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.db, port=self.port)
            return True
        except Exception as e:
            #写入日志文件
            logger.warning(e)
            return False

    def _reConn(self, num=3, stime=3):  # 重试连接总次数为3次
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping() # cping 校验连接是否异常
                _status = False
            except Exception as e:
                logger.warning('reconnecting...')
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，直到成功或重试次数结束

    def select(self, sql=''):
        try:
            #重复尝试连接一天
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.conn.commit()
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except Exception as e:
            # print "Error %d: %s" % (e.args[0], e.args[1])
            return False

    def select_limit(self, sql='', offset=0, length=20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        return self.select(sql)

    def insert(self,sql='',value=()):
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql,value)
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def query(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute("set names utf8")  # utf8 字符集
            result = self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return (True, result)
        except Exception as e:
            logger.warning(e)
            return False
    
    def update(self,sql=''):
        try:
            #重复连接5次
            self._reConn(num=5,stime=3)
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            logger.warning(e)
            return False
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    my = mysql('192.168.1.120', 'root', 'sea12345', 'sonar_database', 3306)
    #print(my.select_limit('select * from sonar_image_data', 0, 3))
    print(my.select('select * from sonar_image_data limit 1'))
    # my.close()
