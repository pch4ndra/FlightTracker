CREATE TRIGGER AirlineMove BEFORE INSERT ON Airline FOR EACH ROW
BEGIN

    SET @airlineExists = 
                    (SELECT COUNT(IATACode)
                    FROM Airlines
                    WHERE IATACode = NEW.IATACode);
    
    IF @airlineExists > 0 THEN
        SET NEW.IATACode = 'XX';
    END IF;

END;