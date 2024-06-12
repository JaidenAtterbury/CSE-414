-- Both of these queries work

SELECT M.id, M.name
  FROM Members AS M
 WHERE M.id IN (SELECT M1.id
                  FROM Members AS M1, Books AS B1, Lending as L1
                 WHERE M1.id = L1.id AND
                       B1.isbn = L1.isbn AND
                       B1.title = 'Leaves of Grass') AND
       M.id IN (SELECT M2.id
                  FROM Members as M2, Books as B2, Lending as L2
                 WHERE M2.id = L2.id AND
                       B2.isbn = L2.isbn AND
                       B2.title = 'Moby Dick');

SELECT DISTINCT M.id, M.name
  FROM Lending AS L1, Lending AS L2, Books AS B1, Books AS B2, Members AS M
 WHERE L1.id = M.id AND
       L2.id = M.id AND
       L1.isbn = B1.isbn AND
       L2.isbn = B2.isbn AND
       B1.title = 'Leaves of Grass' AND
       B2.title = 'Moby Dick';
