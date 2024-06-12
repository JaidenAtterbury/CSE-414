-- Output row count: 256

WITH SeaDest AS
    (SELECT DISTINCT F1.dest_city AS sea_dest
       FROM Flights AS F1
      WHERE F1.origin_city = 'Seattle WA')
SELECT DISTINCT F2.dest_city AS city
  FROM SeaDest AS SD, Flights AS F2
 WHERE SD.sea_dest = F2.origin_city AND
       F2.dest_city != 'Seattle WA' AND
       F2.dest_city NOT IN (SELECT SD2.sea_dest
                              FROM SeaDest AS SD2)
 ORDER BY city;