-- This query outputs 22 rows.

SELECT C.name AS name, SUM(F.departure_delay) AS delay
  FROM Flights AS F, Carriers AS C
 WHERE F.carrier_id = C.cid
 GROUP BY C.name;