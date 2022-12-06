DROP TRIGGER IF EXISTS AirlineMove;
CREATE TRIGGER AirlineMove 
    AFTER INSERT ON Airlines WHEN (SELECT COUNT(Name) FROM Airlines WHERE Name = NEW.Name) > 0
    BEGIN
        UPDATE Airlines SET Name = 'XX' WHERE IATACode = NEW.IATACode;
END;

DROP PROCEDURE IF EXISTS GetEfficientFlights;
CREATE PROCEDURE GetEfficientFlights()
BEGIN
    DECLARE varIATACode VARCHAR(255);
    DECLARE varFlightNum VARCHAR(255);
    DECLARE varAirlineName VARCHAR(255);
    DECLARE varStatus VARCHAR(255);
    DECLARE exit_loop BOOLEAN DEFAULT FALSE;
    -- -------------------------
    -- ADVANCED QUERY CURSOR 1
    -- -------------------------
    DECLARE ineffCur CURSOR FOR (
        SELECT a.IATACode, f.FlightNum, a.Name FROM Flights f NATURAL JOIN Airliens a WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) BETWEEN p.MaxPassengers * 0.8 AND p.MaxPassengers * 0.85 GROUP BY p.Model ORDER BY NumFlights DESC;
    );

    -- -------------------------
    -- ADVANCED QUERY CURSOR 2
    -- -------------------------
    DECALRE effCur CURSOR FOR (
        SELECT a.IATACode, f.FlightNum, a.Name FROM Flights f NATURAL JOIN Airliens a WHERE (SELECT COUNT(t2.TicketID) FROM Tickets t2 WHERE t2.FlightNum = f.FlightNum) > p.MaxPassengers * 0.85 GROUP BY p.Model ORDER BY NumFlights DESC;
    );

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

    DROP TABLE IF EXISTS NewTable;

    CREATE TABLE NewTable(
        FlightNum VARCHAR(255) PRIMARY KEY,
        IATACode VARCHAR(255),
        AirlineName VARCHAR(255),
        Status VARCHAR(255)
    );

    OPEN ineffCur;
    cloop: LOOP
        FETCH ineffCur INTO varIATACode, varFlightNum, varAirlineName;
        IF (exit_loop) THEN
            LEAVE cloop;
        END IF;

        IF (2 > 1) THEN
            SET varStatus = 'Inefficient';
        END IF;

        INSERT IGNORE INTO NewTable VALUES (varFlightNum, varIATACode, varAirlineName, varStatus);
    END LOOP cloop;
    CLOSE ineffCur;

    OPEN effCur;
    cloop: LOOP
        FETCH effCur INTO varIATACode, varFlightNum, varAirlineName;
        IF (exit_loop) THEN
            LEAVE cloop;
        END IF;

        IF (2 > 1) THEN
            SET varStatus = 'Efficient';
        END IF;

        INSERT IGNORE INTO NewTable VALUES (varFlightNum, varIATACode, varAirlineName, varStatus);
    END LOOP cloop;
    CLOSE effCur;

    SELECT * FROM NewTable;
END;
