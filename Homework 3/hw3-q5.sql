-- Output row count: 3

WITH OneStop AS 
	(SELECT DISTINCT F1.dest_city AS dest_city
	   FROM Flights AS F1
	  WHERE F1.origin_city = 'Seattle WA')
SELECT DISTINCT F3.dest_city AS city
  FROM Flights AS f3, OneStop AS OS
 WHERE F3.dest_city NOT IN (SELECT dest_city
                              FROM OneStop) AND
	   F3.dest_city NOT IN (SELECT DISTINCT F2.dest_city
							  FROM Flights AS F2, OneStop AS OS2
							 WHERE OS2.dest_city = F2.origin_city) AND
	   F3.dest_city != 'Seattle WA'
ORDER BY city;