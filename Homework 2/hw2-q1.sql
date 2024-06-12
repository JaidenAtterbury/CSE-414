-- This query outputs 3 rows.

SELECT DISTINCT flight_num AS flight_num
  FROM Flights AS F, Weekdays AS W, Carriers AS C
 WHERE F.day_of_week_id = W.did AND
       F.carrier_id = C.cid AND
       W.day_of_week = 'Monday' AND
       C.name = "Alaska Airlines Inc." AND
       F.origin_city = 'Seattle WA' AND
       F.dest_city = 'Boston MA';