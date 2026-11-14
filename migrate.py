
import sqlite3

connection = sqlite3.connect("tickets.db")
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(tickets)")
columns = [column[1] for column in cursor.fetchall()]

if "sla_due_at" not in columns:
    cursor.execute(
        "ALTER TABLE tickets ADD COLUMN sla_due_at DATETIME"
    )
    print("SLA column added successfully.")
else:
    print("SLA column already exists.")

connection.commit()
connection.close()