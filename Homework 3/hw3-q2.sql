-- Output row count: 133

SELECT DISTINCT F.origin_city AS city
  FROM Flights AS F
 WHERE F.canceled = 0
 GROUP BY F.origin_city
HAVING MAX(F.actual_time) < 240
 ORDER BY city;