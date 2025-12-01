import sqlite3, os

db = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3'))
print('Using DB:', db)
if not os.path.exists(db):
    print('db.sqlite3 not found')
else:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cur.fetchall()
    print('Tables:', rows)
    try:
        cur.execute('SELECT count(*) FROM consultas')
        c = cur.fetchone()[0]
        print('consultas count:', c)
    except Exception as e:
        print('Could not query consultas:', e)
    conn.close()
