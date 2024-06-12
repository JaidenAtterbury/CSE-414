-- This query outputs 6 rows.

SELECT C.name AS name, 100 * AVG(F.canceled) AS percentage
  FROM Flights AS F, Carriers AS C
 WHERE F.carrier_id = C.cid AND
       F.origin_city = 'Seattle WA'
GROUP BY C.name
HAVING percentage > 0.5
ORDER BY percentage;