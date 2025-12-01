import pymysql
import sys

# Credenciales por defecto tomadas de modulos_consultas/settings.py
HOST = 'localhost'
USER = 'root'
PASSWORD = 'admin'
DB = 'bdxd'
PORT = 3306

try:
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT, charset='utf8mb4')
    with conn.cursor() as cur:
        cur.execute("SELECT VERSION();")
        ver = cur.fetchone()
        print('OK - server version:', ver[0] if ver else 'unknown')
    conn.close()
except Exception as e:
    print('ERROR -', repr(e))
    sys.exit(1)
