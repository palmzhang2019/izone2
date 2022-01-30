# -*- coding:UTF-8 -*-
# @Time : 2022/1/30 15:08
# @Author : Palm
# @Remark :
from zhconv import convert_for_mw
from izone.database_config import data_config
import pymysql


conn = pymysql.Connect(
    host=data_config['DATAHOST'],
    port=data_config['DATAPORT'],
    user=data_config['DATAUSER'],
    passwd=data_config['DATAPASS'],
    db=data_config['DATANAME'],
    charset='utf8'
)

cur = conn.cursor()

sql = "select * from blog_category"
sql_hant = "select * from blog_categoryhant"
cur.execute(sql)

hans_cates = [c[0] for c in cur.fetchall()]
cur.execute(sql_hant)
hant_cates = [c[0] for c in cur.fetchall()]

for c in hans_cates:
    if c not in hant_cates:
        sql = "select * from blog_category where id= %d" % c
        cur.execute(sql)
        res = cur.fetchone()
        insert_ele = []
        for r in res:
            if isinstance(r, str):
                r = fanti_slug = convert_for_mw(r, 'zh-tw')
            insert_ele.append(r)
        insert_sql = "insert into blog_categoryhant (id, name, slug, description) values (%d, '%s', '%s', '%s')" % (
            insert_ele[0], insert_ele[1], insert_ele[2], insert_ele[3]
        )
        try:
            cur.execute(insert_sql)
            conn.commit()
            print("成功")
        except:
            conn.rollback()
