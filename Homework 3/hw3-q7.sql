-- Output row count: 3

SELECT DISTINCT C.name AS carrier
  FROM Carriers AS C, Flights AS F
 WHERE F.carrier_id = C.cid AND
       F.origin_city = 'Seattle WA' AND
       F.dest_city = 'New York NY'
 ORDER BY carrier;