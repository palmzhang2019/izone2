from zhconv import convert_for_mw
from izone.database_config import data_config
import pymysql


conn = pymysql.Connect(
    host = data_config['DATAHOST'],
    port = data_config['DATAPORT'],
    user = data_config['DATAUSER'],
    passwd = data_config['DATAPASS'],
    db = data_config['DATANAME'],
    charset='utf8'
)

cur = conn.cursor()

def update_sql(table_name):
    column_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % table_name
    cur.execute(column_sql)
    columns = [c[0] for c in cur.fetchall()]

    sql = "select * from %s" % table_name
    cur.execute(sql)
    for row in cur.fetchall():
        new_row = []
        for slug in row:
            if isinstance(slug, str):
                fanti_slug = convert_for_mw(slug, 'zh-tw')
            else:
                fanti_slug = slug
            new_row.append(fanti_slug)

        new_dict = concat_dict(columns, new_row)
        update_state = "update %s set " % table_name
        for key, value in new_dict.items():
            if 'id' in key:
                continue
            update_state += "%s='%s', " %(key, value)
        update_state = str(update_state[:-2])
        update_state += " where id = %d" % new_dict['id']
        cur.execute(update_state)
        conn.commit()

def concat_dict(columns, new_row):
    new_dict = {}
    for i in zip(columns, new_row):
        new_dict[i[0]] = i[1]
    return new_dict

def do():
    table_list = ['blog_categoryhant', 'blog_taghant', 'blog_keywordhant', 'comment_articlehantcomment']
    for table in table_list:
        update_sql(table)

if __name__ == '__main__':
    do()


