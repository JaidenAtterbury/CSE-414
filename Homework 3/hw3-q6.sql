-- Output row count: 3

SELECT DISTINCT C.name AS carrier
  FROM Carriers AS C JOIN (SELECT carrier_id
                             FROM Flights
			                WHERE origin_city = 'Seattle WA' AND
                                  dest_city = 'New York NY') AS F
    ON C.cid = F.carrier_id
 ORDER BY carrier;