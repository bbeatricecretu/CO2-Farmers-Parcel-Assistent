import sqlite3

conn = sqlite3.connect('farmers_new_db.sqlite')
cursor = conn.cursor()

# Update one farmer to have daily frequency
cursor.execute("UPDATE farmer_reports SET report_frequency = 'daily' WHERE phone = '+40741111111'")
conn.commit()

# Check what we have
cursor.execute('SELECT phone, report_frequency FROM farmer_reports')
reports = cursor.fetchall()
print('Farmer reports:')
for r in reports:
    print(f'  Phone: {r[0]}, Frequency: {r[1]}')

conn.close()
print("\nNow test the /generate-reports endpoint again!")
