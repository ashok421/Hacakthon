import psycopg2

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_PjywFAuZ3mI1@ep-steep-bar-a81ukehq-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

cur = conn.cursor()

# Fetch data
cur.execute("SELECT * FROM customers;")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()