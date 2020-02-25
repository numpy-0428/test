# -*- coding:utf-8 -*-
# author: sdl
'''
定义对mysql数据库基本操作的函数封装
1.包括基本的单条语句操作，删除、修改、更新等
2.独立的查询单条、多条语句
3.独立地添加多条数据
'''

import logging
import pymysql
import os
from public import config


class OperationDbInterface(object):
    # 初始化数据库连接
    def __init__(self, host_db='localhost', user_db='root', passwd_db='sudonglei.1', name_db='test_interface',
                 port_db=3306, link_type=0):
        """
        :param host_db: 数据库地址
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 数据库端口号
        :param link_type: 连接类型，用于设置输出数据是元组还是字典，默认字典，link_type=0

        :return:游标
        """
        try:
            if link_type == 0:
                # 创建数据库连接，返回字典（cursor:光标）
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            else:
                # 创建数据库连接，返回元组
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8')
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print("创建数据库连接失败 | mysql error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    # 定义单条数据操作，包含删除、更新操作
    def op_sql(self, condition):
        """
        :param condition: sql语句，该通用方法可用来替代updateone，deleteone
        :return: 字典形式
        """
        try:
            results = self.cur.execute(condition)  # 执行sql语句
            self.conn.commit()  # 提交游标数据
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': f'操作行数：{results}'}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'meassage': '执行通用操作异常', 'data': []}
            print("数据库错误 | op_sql %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 查询表中单条数据
    def select_one(self, condition):
        """
        :param condition: sql语句
        :return: 字典形式的单条查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据数大于0
                results = self.cur.fetchone()  # 获取一条结果
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'meassage': '执行单条查询操作异常', 'data': []}
            print("数据库错误 | select_one %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_all(self, condition):
        """
        :param condition: sql语句
        :return: 字典形式的批量查询结果
        """
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                self.cur.scroll(0, mode='absolute') # 将鼠标光标放回初始位置
                results = self.cur.fetchall() # 返回游标中所有结果
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'meassage': '执行批量查询操作异常', 'data': []}
            print("数据库错误 | select_all %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 定义表中插入数据操作的方法
    def insert_data(self, condition, params):
        """
        :param condition: insert语句
        :param params: insert数据，列表形式[('3', 'Tom', '1 year 1 class', '6'),('3', 'Tom', '2 year 1 class', '7'),]
        :return:字典形式的批量插入数据结果
        """
        try:
            results = self.cur.executemany(condition, params)  # 返回插入的数据条数
            self.conn.commit()
            result = {'code': '0000', 'message': '执行批量插入操作成功', 'data': f'插入行数：{results}'}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行批量插入操作异常', 'data': []}
            print("数据库错误 | insert_more %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 关闭数据库
    def __del__(self):
        if self.cur is not None:
            self.cur.close()   # 关闭游标
        if self.conn is not None:
            self.conn.close()   # 释放数据库资源


if __name__ == "__main__":
    test = OperationDbInterface()   # 实例化类
    result_select_all = test.select_all("SELECT * FROM config_total")  # 查询多条数据
    result_select_one = test.select_one("SELECT * FROM config_total WHERE id=1")   # 查询单条数据
    result_op_sql = test.op_sql("update config_total set value_config='test123' WHERE id=1")  #通用操作
    result_insert = test.insert_data("INSERT INTO `config_total` ( `key_config`, `value_config`, `description`, "
                                     "`status` ) VALUES (%s, %s, %s, %s)", [('mytest1', 'my_value_test1', '测试配置1',
                                                                             1), ('mytest2', 'my_value_test2',
                                                                                  '测试配置2', 0)])
    print(result_select_all['data'], result_select_all['message'])
    print(result_select_one['data'], result_select_all['message'])
    print(result_op_sql['data'], result_op_sql['message'])
    print(result_insert['data'], result_insert['message'])
