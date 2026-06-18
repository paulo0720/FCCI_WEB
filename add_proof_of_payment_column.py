import sqlite3
conn = sqlite3.connect("database/fcci.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE members ADD COLUMN proof_of_payment TEXT")
conn.commit()
conn.close()
print("Done")