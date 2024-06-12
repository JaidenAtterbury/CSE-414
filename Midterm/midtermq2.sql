SELECT M.name, B.title
  FROM Lending AS L, Members AS M, Books AS B
 WHERE L.id = M.id AND
       L.isbn = B.isbn AND
       L.returned IS NULL
 ORDER BY M.name DESC;