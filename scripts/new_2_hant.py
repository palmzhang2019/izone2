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


def exec_cate():
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
                    r = convert_for_mw(r, 'zh-tw')
                insert_ele.append(r)
            insert_sql = "insert into blog_categoryhant (id, name, slug, description) values (%d, '%s', '%s', '%s')" % (
                insert_ele[0], insert_ele[1], insert_ele[2], insert_ele[3]
            )
            try:
                cur.execute(insert_sql)
                conn.commit()
                print("cate success")
            except:
                conn.rollback()


def exec_tag():
    sql = "select * from blog_tag"
    sql_hant = "select * from blog_taghant"
    cur.execute(sql)

    hans_cates = [c[0] for c in cur.fetchall()]
    cur.execute(sql_hant)
    hant_cates = [c[0] for c in cur.fetchall()]

    for c in hans_cates:
        if c not in hant_cates:
            sql = "select * from blog_tag where id= %d" % c
            cur.execute(sql)
            res = cur.fetchone()
            insert_ele = []
            for r in res:
                if isinstance(r, str):
                    r = convert_for_mw(r, 'zh-tw')
                insert_ele.append(r)
            insert_sql = "insert into blog_taghant (id, name, slug, description) values (%d, '%s', '%s', '%s')" % (
                insert_ele[0], insert_ele[1], insert_ele[2], insert_ele[3]
            )
            try:
                cur.execute(insert_sql)
                conn.commit()
                print("tag success")
            except:
                conn.rollback()


def exec_keyword():
    sql = "select * from blog_keyword"
    sql_hant = "select * from blog_keywordhant"
    cur.execute(sql)

    hans_cates = [c[0] for c in cur.fetchall()]
    cur.execute(sql_hant)
    hant_cates = [c[0] for c in cur.fetchall()]

    for c in hans_cates:
        if c not in hant_cates:
            sql = "select * from blog_keyword where id= %d" % c
            cur.execute(sql)
            res = cur.fetchone()
            insert_ele = []
            for r in res:
                if isinstance(r, str):
                    r = convert_for_mw(r, 'zh-tw')
                insert_ele.append(r)
            insert_sql = "insert into blog_keywordhant (id, name) values (%d, '%s')" % (
                insert_ele[0], insert_ele[1]
            )
            try:
                cur.execute(insert_sql)
                conn.commit()
                print("keyword success")
            except:
                conn.rollback()



def exec_article():
    sql = "select * from blog_article"
    sql_hant = "select * from blog_articlehant"
    cur.execute(sql)

    hans_cates = [c[0] for c in cur.fetchall()]
    cur.execute(sql_hant)
    hant_cates = [c[0] for c in cur.fetchall()]

    for c in hans_cates:
        if c not in hant_cates:
            sql = "select * from blog_article where id= %d" % c
            cur.execute(sql)
            res = cur.fetchone()
            insert_ele = []
            for r in res:
                if isinstance(r, str):
                    r = convert_for_mw(r, 'zh-tw')
                insert_ele.append(r)
            insert_sql = "insert into blog_articlehant (id, title, summary, body, img_link, create_date, update_date, views, slug, author_id, category_id)" \
                         " values (%d, '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', %d, %d)" % (
                insert_ele[0], insert_ele[1], insert_ele[2], insert_ele[3], insert_ele[4], insert_ele[5],
                insert_ele[6], insert_ele[7], insert_ele[8], insert_ele[9], insert_ele[10]
            )
            try:
                cur.execute(insert_sql)
                conn.commit()
                print("article update success")
            except:
                conn.rollback()


if __name__ == '__main__':
    exec_cate()
    exec_tag()
    exec_keyword()
    exec_article()
