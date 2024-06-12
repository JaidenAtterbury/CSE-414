-- This query outputs 12 rows.

SELECT DISTINCT C.name AS name
  FROM Flights AS F, Carriers AS C
 WHERE F.carrier_id = C.cid
GROUP BY C.name, F.day_of_month, F.month_id
HAVING COUNT(*) > 1000;