import os
import sqlite3
from datetime import datetime
 
print("=" * 70)
print("Hinahanap ang lahat ng 'fcci.db' files sa computer mo...")
print("Sandali lang, mga ilang segundo ito.")
print("=" * 70)
 
search_roots = [
    os.path.expanduser("~"),  # Buong user folder (Desktop, Documents, Downloads, atbp.)
]
 
found_databases = []
 
for root_dir in search_roots:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Laktawan ang mga folder na malamang walang kinalaman
        # (para mabilis ang scan)
        dirnames[:] = [
            d for d in dirnames
            if d.lower() not in (
                "node_modules", ".git", "appdata", "$recycle.bin",
                "windows", "program files", "program files (x86)"
            )
        ]
 
        for filename in filenames:
            if filename.lower() == "fcci.db":
                full_path = os.path.join(dirpath, filename)
                found_databases.append(full_path)
 
print()
print(f"NAHANAP: {len(found_databases)} na fcci.db file(s)")
print("=" * 70)
 
if not found_databases:
    print("Walang nahanap na fcci.db. Siguraduhing tama ang sinearch.")
 
for db_path in found_databases:
 
    print()
    print(f"📁 LOCATION: {db_path}")
 
    try:
        size_bytes = os.path.getsize(db_path)
        modified_time = datetime.fromtimestamp(os.path.getmtime(db_path))
        print(f"   Size: {size_bytes:,} bytes")
        print(f"   Last modified: {modified_time.strftime('%Y-%m-%d %I:%M %p')}")
 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
 
        cursor.execute("SELECT COUNT(*) FROM members")
        member_count = cursor.fetchone()[0]
        print(f"   👥 Members sa database na ito: {member_count}")
 
        if member_count > 0:
            cursor.execute("SELECT member_id, full_name FROM members LIMIT 5")
            sample = cursor.fetchall()
            print(f"   Sample members:")
            for m in sample:
                print(f"      - {m[0]}: {m[1]}")
 
        conn.close()
 
    except Exception as e:
        print(f"   ⚠️ Hindi ma-basa ang database: {e}")
 
print()
print("=" * 70)
print("TAPOS NA ANG SCAN")
print()
print("Hanapin ang database na may PINAKAMARAMI ang members —")
print("yan malamang ang 'totoong' database mo na may existing data.")
print("I-copy ang file na ito papunta sa: FCCI_WEB/database/fcci.db")
print("=" * 70)