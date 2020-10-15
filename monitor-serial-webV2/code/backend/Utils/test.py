import sqlite3

conn = sqlite3.connect('data.db')

cur = conn.cursor()

cur.execute("UPDATE Device SET byteId = '11' WHERE byteId = '12'")
conn.commit()

