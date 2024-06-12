-- Output row count: 334

WITH MaxTime AS
    (SELECT F1.origin_city AS origin_city,
            MAX(F1.actual_time) AS max_time
       FROM Flights AS F1
      GROUP BY F1.origin_city)
SELECT DISTINCT F.origin_city AS origin_city, F.dest_city AS dest_city, F.actual_time AS time
  FROM Flights AS F, MaxTime AS MT
 WHERE F.origin_city = MT.origin_city AND
       F.actual_time = MT.max_time
 ORDER BY origin_city, dest_city;