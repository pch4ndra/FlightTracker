# ER Diagram



<img width="642" alt="ER Diagram" src="https://user-images.githubusercontent.com/89672480/194468352-3308a5e4-b7ec-499e-bf5f-f4ad613f00b1.png">



# Logical Design (Relational Schema):

Airports (IATACode: VARCHAR(255) [PK], Name: VARCHAR(255), City: VARCHAR(255), State: VARCHAR(255), Country: VARCHAR(255), PassengerRank2021: INT, PassengerServed2021: INT)

Airlines (Name: VARCHAR(255), MainHub: VARCHAR(255) [FK to Airports.IATACode], IATACode: VARCHAR(255) [PK])

Planes (Manufacturer: VARCHAR(255), Model: VARCHAR(255) [PK], NumInUSFleet: INT, KgPKm: REAL, MaxPassengers: INT)

Passengers (Name: VARCHAR(255), MainAirline: VARCHAR(255) [FK to Airlines.IATACode], RewardsID: VARCHAR(255) [PK], Age: INT, Gender: VARCHAR(255), Race: VARCHAR(255), HomeAirport: VARCHAR(255) [FK to Airports.IATACode])

Flights (IATACode: VARCHAR(255) [FK to Airlines.IATACode], FlightNum: VARCHAR(255) [PK], DepartFrom: VARCHAR(255) [FK to Airports.IATACode], Destination: VARCHAR(255) [FK to Airports.IATACode], Manufacturer: VARCHAR(255) [FK to Planes.Manufacturer], Model: VARCHAR(255) [FK to Planes.Model], TakeoffDate: DATE)

Tickets (TicketID: VARCHAR(255) [PK], Airline: VARCHAR(255) [FK to Flights.IATACode], FlightNum: VARCHAR(255) [FK to Flights.FlightNum], RewardsID: VARCHAR(255) [FK to Passengers.RewardsID], Price: REAL)
