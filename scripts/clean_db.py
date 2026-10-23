import sqlite3

conn = sqlite3.connect('database/database.db')
c = conn.cursor()
c.execute('SELECT id, model_name, algorithm, accuracy FROM model_history')
print('Current model_history rows:')
for r in c.fetchall():
    print(r)

# Delete any old Random Forest records
c.execute("DELETE FROM model_history WHERE LOWER(algorithm) LIKE '%forest%' OR LOWER(model_name) LIKE '%forest%'")
conn.commit()

print('\nAfter cleanup:')
c.execute('SELECT id, model_name, algorithm, accuracy, is_active FROM model_history')
for r in c.fetchall():
    print(r)
conn.close()
