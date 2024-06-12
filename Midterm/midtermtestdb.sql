CREATE TABLE Books (
    isbn INT PRIMARY KEY,
    title VARCHAR(1000),
    author VARCHAR(1000),
    genre VARCHAR(1000),
    publisher VARCHAR(1000)
);

CREATE TABLE Members (
    id INT PRIMARY KEY,
    name VARCHAR(1000)
);

CREATE TABLE Lending (
    isbn INT REFERENCES Books(isbn),
    id INT REFERENCES Members(id),
    checkout DATETIME,
    returned DATETIME,
    PRIMARY KEY (isbn, id, checkout)
);

INSERT INTO Members
VALUES (1, 'Jaiden'),
       (2, 'Tanner'),
       (3, 'Nathan'),
       (4, 'Kyle'),
       (5, 'Chad');

INSERT INTO Books
VALUES (1, 'Moby Dick', 'Herman Melville', 'Epic', 'Harper and Brothers'),
       (2, 'Leaves of Grass', 'Walt Whitman', 'Poem', 'Simon & Schuster'),
       (3, 'Harmonium', 'Wallace Stevens', 'Poem', 'Alfred A Knopf'),
       (4, 'Drip Too Hard', 'Lil Baby & Gunna', 'Classic', 'Quality Music Control'),
       (5, 'James Stewart Calculus', 'James Stewart', 'Torture', 'Caren and Friends');

INSERT INTO Lending
VALUES (1, 1, '2022-10-02', '2022-11-02'),
       (2, 1, '2022-11-02', NULL),
       (3, 1, '2022-12-02', '2022-01-02'),
       (4, 1, '2022-01-02', NULL),
       (1, 2, '2022-10-02', '2022-11-02'),
       (2, 2, '2022-11-02', '2022-12-02'),
       (3, 2, '2022-12-02', '2022-01-02'),
       (4, 2, '2022-01-02', NULL),
       (1, 3, '2022-10-02', '2022-11-02'),
       (2, 3, '2023-01-02', '2023-02-02'),
       (4, 3, '2023-01-02', '2023-02-02'),
       (2, 4, '2023-01-02', '2023-02-02'),
       (4, 4, '2023-01-02', '2023-02-02'),
       (4, 5, '2023-02-02', NULL),
       (1, 1, '2023-11-02', '2023-11-02'),
       (2, 1, '2023-11-02', '2023-11-02'),
       (1, 2, '2022-11-02', '2022-12-02'),
       (2, 2, '2022-12-02', '2023-01-02');