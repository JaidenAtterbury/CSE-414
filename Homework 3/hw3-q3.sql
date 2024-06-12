-- Output row count: 327

WITH FlightCount AS
    (SELECT DISTINCT F1.origin_city, (SELECT COUNT(F2.fid)
                                        FROM Flights AS F2
                                       WHERE F1.origin_city = F2.origin_city AND
		   					   F2.actual_time < 90 AND
		   					   F2.canceled = 0) AS Count
	 FROM Flights AS F1)
SELECT F3.origin_city AS origin_city, 100.0 * FC.Count/COUNT(F3.fid) AS percentage
  FROM Flights AS F3, FlightCount AS FC
 WHERE F3.origin_city = FC.origin_city AND
       F3.canceled = 0
 GROUP BY F3.origin_city, FC.Count
 ORDER BY percentage, origin_city;
