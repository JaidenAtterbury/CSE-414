SELECT B.genre, COUNT(L.checkout)
  FROM Books AS B LEFT OUTER JOIN Lending AS L ON B.isbn = L.isbn
 GROUP BY B.genre
 ORDER BY COUNT(L.checkout) ASC;