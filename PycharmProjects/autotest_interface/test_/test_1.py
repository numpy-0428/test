# -*- coding:utf-8 -*-
# author: sdl
import logging
import pymysql
import os
from public import config

host_db = 'localhost'
user_db = 'root'
passwd_db = 'sudonglei.1'
name_db = 'test_interface'
port_db = 3306
link_type = 0

conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                       charset='utf8', cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

condition1 = "update config_total set value_config='test123' WHERE id=1"

cur = cur.execute(condition1)
result = cur.fetchall()
conn.commit()


print(result)
cur.close()
conn.close()