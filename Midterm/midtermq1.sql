CREATE TABLE Lending (
    isbn INT REFERENCES Books(isbn),
    id INT REFERENCES Members(id),
    checkout DATETIME,
    returned DATETIME,
    PRIMARY KEY (isbn, id, checkout)
);