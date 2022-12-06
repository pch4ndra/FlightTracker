# from werkzeug.wrappers import Request, Response
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3 as sql
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tester'

@app.route("/", methods=('GET', 'POST'))

def index():
    # Declare database and html filepaths
    database = "lebored.db"
    html_template = "index.html"

    if request.method == 'POST':
        columns = {
                "Flights": ['IATACode', 'FlightNum', 'DepartFrom', 'Destination', 'Manufacturer', 'Model', 'TakeoffDate'],
                "Tickets": ['TicketID', 'Airline', 'FlightNum', 'RewardsID', 'Price'],
                "Passengers": ['Name', 'MainAirline', 'RewardsID', 'Age', 'Gender', 'Race', 'HomeAirport'],
                "Airports" :  ['IATACode', 'Name', 'City', 'State', 'Country', 'PassengerRank2021', 'PassengerServed2021'],
                "Airlines": ['Name', 'MainHub','IATACode'],
                "Planes" : ['Manufacturer', 'Model', 'NumInUSFleet', 'KgPKm', 'MaxPassengers']
            }
        primary = {
                "Flights": 'FlightNum',
                "Tickets": 'TicketID',
                "Passengers": 'RewardsID',
                "Airports" :  'IATACode',
                "Airlines": 'IATACode',
                "Planes" : 'Model'
            }
        notstrings = ['PassengerRank2021', 'PassengerServed2021','NumInUSFleet','KgPKm','MaxPassengers','Age','TakeoffDate','Price']
        if 'insert' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Get Form Values
            table = str(request.form['inserttable'])
            # Develop SQL Query
            statement = "INSERT INTO "+table+" VALUES ("
            for index,col in enumerate(columns[table]):
                value = str(request.form[table+col])
                if col not in notstrings:
                    statement += "'"
                statement += value
                if col not in notstrings:
                    statement += "'"
                if index != len(columns[table]) - 1:
                    statement += ","
            statement += ");"
            # Perform Query
            cur.execute(statement)
            conn.commit()
            conn.close()
            # Update Template
            stri = [str("INSERTED")]
            return render_template(html_template, output = stri)
        elif 'delete' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Get Form Values
            table = str(request.form['deletetable'])
            # Develop SQL Query
            statement = "DELETE FROM "+table+" WHERE "+primary[table]+" = '" + str(request.form[table + "2"]) + "';"
            # Perform Query
            cur.execute(statement)
            conn.commit()
            conn.close()
            # Update Template
            stri = [str("DELETED")]
            return render_template(html_template, output = stri)
        elif 'update' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Get Form Values
            table = str(request.form['updatetable'])
            oldiata = str(request.form['oldiata'])
            newiata = str(request.form['newiata'])
            # Develop SQL Query
            statement = "UPDATE "+table+" SET IATACode = '" + newiata + "' WHERE IATACode = '" + oldiata + "';"
            # Perform Query
            cur.execute(statement)
            conn.commit()
            conn.close()
            # Update Template
            stri = [str("UPDATED " + oldiata + " to " + newiata)]
            return render_template(html_template, output = stri)
        elif 'search' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Get Form Values
            table = str(request.form['searchtable'])
            searchval = str(request.form['searcher'])
            # Develop SQL Query
            statement = "SELECT * FROM "+table+" WHERE"
            # City LIKE 's%';
            for index,column in enumerate(columns[table]):
                statement += " " + column + " LIKE '%" + searchval + "%' "
                if index != len(columns[table]) - 1:
                    statement += " OR "
            # Perform Query
            cur.execute(statement)
            result = cur.fetchall()
            stri = []
            for item in result:
                stri.append(str(item))
            conn.commit()
            conn.close()
            # Update Template
            return render_template(html_template, output = stri)
        elif 'aquery1' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Develop SQL Query
            statement = "SELECT p.Model, COUNT(f.FlightNum) as NumFlights FROM Flights f NATURAL JOIN Planes p WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) BETWEEN p.MaxPassengers * 0.8 AND p.MaxPassengers * 0.85 GROUP BY p.Model ORDER BY NumFlights DESC LIMIT 15;"
            # Perform Query
            cur.execute(statement)
            result = cur.fetchall()
            stri = []
            for item in result:
                stri.append(str(item))
            conn.commit()
            conn.close()
            # Update Template
            return render_template(html_template, output = stri)
        elif 'aquery2' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Develop SQL Query
            statement = "SELECT f.IATACode, a.Name, COUNT(f.DepartFrom) as FlightCount FROM Flights f JOIN Airports a ON f.DepartFrom = a.IATACode WHERE 10 < (SELECT COUNT(f2.DepartFrom) FROM Flights f2 JOIN Airports a2 ON f2.DepartFrom = a2.IATACode WHERE f2.IATACode = f.IATACode AND a.Name = a2.Name) GROUP BY f.IATACode, a.IATACode ORDER BY FlightCount DESC LIMIT 15;"
            # Perform Query
            cur.execute(statement)
            result = cur.fetchall()
            stri = []
            for item in result:
                stri.append(str(item))
            conn.commit()
            conn.close()
            # Update Template
            return render_template(html_template, output = stri)
        elif 'sprocedure' in request.form:
            # Establish Database Connection
            conn = sql.connect(database)
            cur = conn.cursor()
            # Develop SQL Query
            cursor1 = "SELECT a.IATACode, f.FlightNum, a.Name FROM Flights f NATURAL JOIN Planes p NATURAL JOIN Airlines a WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) BETWEEN p.MaxPassengers * 0.8 AND p.MaxPassengers * 0.85 GROUP BY p.Model;"
            cursor2 = "SELECT a.IATACode, f.FlightNum, a.Name FROM Flights f NATURAL JOIN Planes p NATURAL JOIN Airlines a WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) > p.MaxPassengers * 0.85 GROUP BY p.Model;"
            # Perform Query
            cur.execute(cursor1)
            cur1result = cur.fetchall()
            cur.execute(cursor2)
            cur2result = cur.fetchall()

            cur.execute("DROP TABLE IF EXISTS ProcedureTable;")
            cur.execute("CREATE TABLE ProcedureTable( FlightNum VARCHAR(255) PRIMARY KEY, IATACode VARCHAR(255), AirlineName VARCHAR(255), Status VARCHAR(255), Origin VARCHAR(255), Destination VARCHAR(255));")

            for item in cur1result:
                cur.execute("SELECT Destination FROM Flights WHERE FlightNum = '" + item[1] + "';")
                dest = cur.fetchall()
                cur.execute("SELECT DepartFrom FROM Flights WHERE FlightNum = '" + item[1] + "';")
                origin = cur.fetchall()
                cur.execute("INSERT INTO ProcedureTable VALUES ('" + item[1] + "','" + item[0] + "','" + item[2] + "','" + origin[0][0] + "','" + dest[0][0] + "', 'Inefficient');")
            
            for item in cur2result:
                cur.execute("SELECT Destination FROM Flights WHERE FlightNum = '" + item[1] + "';")
                dest = cur.fetchall()
                cur.execute("SELECT DepartFrom FROM Flights WHERE FlightNum = '" + item[1] + "';")
                origin = cur.fetchall()
                cur.execute("INSERT INTO ProcedureTable VALUES ('" + item[1] + "','" + item[0] + "','" + item[2] + "','" + origin[0][0] + "','" + dest[0][0] + "', 'Efficient');")
            
            cur.execute("SELECT * FROM ProcedureTable;")
            result = cur.fetchall()
            stri = []
            for item in result:
                stri.append(str(item))
            cur.execute("DROP TABLE IF EXISTS ProcedureTable;")
            conn.commit()
            conn.close()

            G = nx.DiGraph()

            result_ = cur.execute("CALL GetEfficientFlights();") if 0 != 0 else result

            airports = set()
            for item in result_: 
                airports.add(item[3])
                airports.add(item[4])

            nodes = list(airports)
            G.add_nodes_from(nodes)
            G.add_edges_from([(x,y) for (a,b,c,x,y,f) in result])
            pos = {}
            for airport in nodes:
                pos[airport] = (np.random.randint(0,50),np.random.randint(0,50))
            labels = {}
            for i in nodes:
                labels[i] = i
            colors = []
            for i in result:
                if i[5] == 'Inefficient':
                    colors.append('red')
                else:
                    colors.append('blue')
            color_map = ['green'] * len(airports)
            nx.draw_networkx(G, pos = pos, labels = labels, arrows = True, node_color = color_map, edge_color = colors, edgecolors = "gray")
            plt.title("Map of Flights (Inefficient is Red | Efficient is Blue)")
            plt.savefig("static/map.png", dpi = 300)

            # Update Template
            return render_template(html_template, output = stri, map_image = "static/map.png")
    return render_template(html_template, output=["Welcome To FlightTracker"], map_image = "static/map.png")

# @app.route("/indexer/<stri>")
# def indexer(stri):
#     return render_template(html_template, output=stri)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8080, app)
