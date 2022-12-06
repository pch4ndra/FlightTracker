# Database Connection
<img width="950" alt="image" src="https://user-images.githubusercontent.com/89665603/197295044-140b6e62-6865-4ca5-846b-143868360a11.png">
<img width="471" alt="image" src="https://user-images.githubusercontent.com/89665603/197294782-0308ee82-3b5f-4e62-9ec1-d9f7345350c1.png">

# Data Definition Language (DDL) commands

```sql
/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`leboreddata` /*!40100 DEFAULT CHARACTER 
SET latin1 */;

USE `leboreddata`;

CREATE TABLE Airports (
    IATACode VARCHAR(255),
    Name VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    Country VARCHAR(255),
    PassengerRank2021 INT,
    PassengerServed2021 INT,
    PRIMARY KEY (IATACode)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Airlines (
    Name VARCHAR(255),
    MainHub VARCHAR(255),
    IATACode VARCHAR(255),
    PRIMARY KEY (IATACode),
    FOREIGN KEY (MainHub) REFERENCES Airports(IATACode) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Planes (
    Manufacturer VARCHAR(255),
    Model VARCHAR(255),
    NumInUSFleet INT,
    KgPKm REAL,
    MaxPassengers INT,
    PRIMARY KEY (Model)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Passengers (
    Name VARCHAR(255),
    MainAirline VARCHAR(255),
    RewardsID VARCHAR(255),
    Age INT,
    Gender VARCHAR(255),
    Race VARCHAR(255),
    HomeAirport VARCHAR(255),
    PRIMARY KEY (RewardsID),
    FOREIGN KEY (MainAirline) REFERENCES Airlines(IATACode) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (HomeAirport) REFERENCES Airports(IATACode) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Flights (
    IATACode VARCHAR(255),
    FlightNum VARCHAR(255),
    DepartFrom VARCHAR(255),
    Destination VARCHAR(255),
    Manufacturer VARCHAR(255),
    Model VARCHAR(255),
    TakeoffDate DATE,
    PRIMARY KEY (FlightNum),
    FOREIGN KEY (IATACode) REFERENCES Airlines(IATACode) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (DepartFrom) REFERENCES Airports(IATACode) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (Destination) REFERENCES Airports(IATACode) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (Model) REFERENCES Planes(Model) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Tickets (
    TicketID VARCHAR(255),
    Airline VARCHAR(255),
    FlightNum VARCHAR(255),
    RewardsID VARCHAR(255),
    Price REAL,
    PRIMARY KEY (TicketID),
    FOREIGN KEY (Airline) REFERENCES Flights(IATACode) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (FlightNum) REFERENCES Flights(FlightNum) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (RewardsID) REFERENCES Passengers(RewardsID) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

# Data Amount Per Table
### Airports
<img width="225" alt="image" src="https://user-images.githubusercontent.com/89665603/197069578-ac07e416-a4ed-4ec5-8dfd-f59dfeb49115.png">

### Airlines
<img width="230" alt="image" src="https://user-images.githubusercontent.com/89665603/197069631-4ec14075-5c85-4e9a-a41c-b958a4512343.png">

### Planes
<img width="221" alt="image" src="https://user-images.githubusercontent.com/89665603/197069664-f7fd862d-5c02-4151-9c6a-62aadaaa7a78.png">

### Passengers
<img width="235" alt="image" src="https://user-images.githubusercontent.com/89665603/197069726-0bf30228-dcad-45af-90ff-fabe374218e4.png">

### Flights
<img width="225" alt="image" src="https://user-images.githubusercontent.com/89665603/197069762-bc8ff366-2f6c-47e5-96a5-744012a508c0.png">

### Tickets
<img width="227" alt="image" src="https://user-images.githubusercontent.com/89665603/197289199-4b83fe75-e8c6-4f7c-a2d9-ebae1a7e6fb5.png">

# Advanced Queries

### Query 1
```sql
SELECT p.Model, COUNT(f.FlightNum) as NumFlights
FROM Flights f NATURAL JOIN Planes p
WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) BETWEEN p.MaxPassengers * 0.8 AND p.MaxPassengers * 0.85
GROUP BY p.Model
ORDER BY NumFlights DESC
LIMIT 15;
```

<img width="170" alt="image" src="https://user-images.githubusercontent.com/89665603/197294509-2e4f3398-14ee-4715-b327-b8443b6411f6.png">

### Query 2
```sql
SELECT f.IATACode, a.Name, COUNT(f.DepartFrom) as FlightCount
FROM Flights f JOIN Airports a ON f.DepartFrom = a.IATACode
WHERE 10 < (SELECT COUNT(f2.DepartFrom) FROM Flights f2 JOIN Airports a2 ON f2.DepartFrom = a2.IATACode WHERE f2.IATACode = f.IATACode AND a.Name = a2.Name)
GROUP BY f.IATACode, a.IATACode
ORDER BY FlightCount DESC
LIMIT 15;
```

<img width="472" alt="image" src="https://user-images.githubusercontent.com/89665603/197294480-d7268952-54a4-4f18-a464-2db8355998ae.png">

# Indexing

### Query 1
```sql
EXPLAIN ANALYZE
SELECT p.Model, COUNT(f.FlightNum) as NumFlights
FROM Flights f NATURAL JOIN Planes p
WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) BETWEEN p.MaxPassengers * 0.8 AND p.MaxPassengers * 0.85
GROUP BY p.Model
ORDER BY NumFlights DESC
LIMIT 15;
```

<img width="946" alt="image" src="https://user-images.githubusercontent.com/89665603/197295677-4a2a1dff-1bf5-4a4c-82ec-36a38ee43244.png">

Above is the analze Result without any indexes. We can see that the Aggregate is taking a long time for us. So we add an index on leboreddata.Tickets(TicketID), as shown below.

```sql
CREATE INDEX index_ticketidagg ON leboreddata.Tickets(TicketID);
```

<img width="946" alt="image" src="https://user-images.githubusercontent.com/89665603/197296022-4ff3edca-a82f-41d6-9611-d70f843a2a11.png">

Above is the analyze result with the index on TicketID. However, we can see that there was no significant advantage in the index. Next, we see that the group aggregate on count(Flights.FlightNum) has a very large cost, so we'll add another index to help with this.

```sql
CREATE INDEX index_flightnumagg ON leboreddata.Flights(FlightNum);
```

<img width="960" alt="image" src="https://user-images.githubusercontent.com/89665603/197296305-c3686d40-6941-4165-80b9-80c13f2dcf78.png">

Above is the analyze result with the index on TicketID and an index on FlightNum. However, we still see that there was no significant advantage in the index. Next, we can also see that the natural inner join is costing a lot in the query. So, we'll add another index with hopes of aiding this.

```sql
CREATE INDEX index_pmodelagg ON leboreddata.Planes(Model);
```

<img width="960" alt="image" src="https://user-images.githubusercontent.com/89665603/197296676-77f3f93c-27cb-443c-83b6-1ec99fa00e08.png">

Finally, we still see that all three of the different indexes didn't aid in the lowering of the cost of the queries. Thus, we came to the conclusion that this queryis inherently costing a lot due to the size of the tables rather than any noticable inefficiency in the query.

### Query 2
```sql
EXPLAIN ANALYZE
SELECT f.IATACode, a.Name, COUNT(f.DepartFrom) as FlightCount
FROM Flights f JOIN Airports a ON f.DepartFrom = a.IATACode
WHERE 10 < (SELECT COUNT(f2.DepartFrom) FROM Flights f2 JOIN Airports a2 ON f2.DepartFrom = a2.IATACode WHERE f2.IATACode = f.IATACode AND a.Name = a2.Name)
GROUP BY f.IATACode, a.IATACode
ORDER BY FlightCount DESC
LIMIT 15;
```

<img width="1397" alt="Screen Shot 2022-10-21 at 5 26 03 PM" src="https://user-images.githubusercontent.com/89672480/197297391-942fe02f-e2ba-4a36-9ba6-0eeeffda0dda.png">

Above is the original sql query without any indexing involved. Now, we will try to index to attempt to reduce the time.

```sql
CREATE INDEX index_pmodelag ON leboreddata.Airports(IATACode);
```

<img width="1569" alt="Screen Shot 2022-10-21 at 5 40 20 PM" src="https://user-images.githubusercontent.com/89672480/197298770-c2cf032d-56da-4b5c-8e62-9286e8b5ba81.png">

Above is the analysis result with the index on IATACode. However, we can see that there was no significant advantage in the index, because the size is very large and the join, from this reason, makes the join very inefficient.


```sql
CREATE INDEX index_pmodelaggggg ON leboreddata.Flights(DepartFrom);
```
<img width="1700" alt="Screen Shot 2022-10-21 at 5 39 52 PM" src="https://user-images.githubusercontent.com/89672480/197298722-e9eac941-8017-4f5c-8462-9e6664026732.png">

Above is the analysis result with the index on DepartFrom. However, we can see that there was no significant advantage in the index because the group aggregate is very large.


```sql
CREATE INDEX index_pmodelaggggggg ON leboreddata.Flights(IATACode);
```

<img width="1660" alt="Screen Shot 2022-10-21 at 5 43 29 PM" src="https://user-images.githubusercontent.com/89672480/197299027-9a52f578-41df-4df6-9fee-94af8b2ee902.png">

Above is the analysis result with the index on the Filter which is part of the subquery. Since the size is very large, from this reason, the filter is very inefficient.


## Conclusion

After creating three indexes for each of the advanced queries, we found that the indexes were not helping the cost of each query. We then came to the conclusion that while the queries each have very large costs (specifically at joins, it seems), the cost arises from a very large dataset rather than an inefficient query. According to sources online as well, this would seem to be a very likely cause of not seeing a benefit in creating indexes.

