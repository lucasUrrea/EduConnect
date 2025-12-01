import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='admin', db='bdxd', port=3306)
    cur = conn.cursor()
    cur.execute('SHOW TABLES')
    tables = cur.fetchall()
    print('Connected to bdxd, tables:', tables)
    try:
        cur.execute('SELECT COUNT(*) FROM consultas')
        print('consultas count in bdxd:', cur.fetchone()[0])
    except Exception as e:
        print('Could not query consultas in bdxd:', e)
    conn.close()
except Exception as e:
    print('Connection failed:', type(e).__name__, e)
