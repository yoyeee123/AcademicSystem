# 配置

import pymysql


# 数据库连接
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='wyg123..',
    database='academicsystem'
)
cursor = conn.cursor()


