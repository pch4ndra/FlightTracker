import sqlite3 as sql

conn = sql.connect("lebored.db")
cur = conn.cursor()

cloud = open("DDLCommands_Local.sql")
ddl = cloud.readlines()
cloud.close()
for index, command in enumerate(ddl):
    ccommand = command.replace("\n","")
    cur.execute(ccommand)

files = ["1_AirportsData.sql","2_AirlinesData.sql","3_PlanesData.sql","4_PassengersData.sql","5_FlightsData.sql","6_TicketsData.sql"]
for file in files:
    cloud = open(file)
    ddl = cloud.readlines()
    cloud.close()
    for index, command in enumerate(ddl):
        ccommand = command.replace("\n","")
        cur.execute(ccommand)
print(cur.fetchall())

conn.commit()
conn.close()