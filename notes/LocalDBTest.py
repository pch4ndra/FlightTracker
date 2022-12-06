import sqlite3 as sql

conn = sql.connect("lebored.db")
cur = conn.cursor()

# cur.execute("""
#         CREATE TRIGGER AirlineMove 
#         AFTER INSERT ON Airlines WHEN (SELECT COUNT(Name) FROM Airlines WHERE Name = NEW.Name) > 0
#         BEGIN
#             UPDATE Airlines SET Name = 'XX' WHERE IATACode = NEW.IATACode;
#         END;
#         """)

# cur.execute('DROP TRIGGER AirlineMove;')

cur.execute("INSERT INTO Airlines VALUES ('United Airlines', 'DFW', 'XX');")
cur.execute("SELECT * FROM Airlines;")
result = cur.fetchall()
print(result)

