-- Part 4: Mr. Frumble Relationship Discovery & Normalization:

-- Subpart a:

CREATE TABLE Sales (
    name VARCHAR(255),
    discount VARCHAR(255),
    month VARCHAR(9),
    price INT
);

.mode tabs

.import mrFrumbleData.txt Sales

-- Subpart b:

-- We will start the FD hunt by checking all of the simple FDs.

-- Start with name->attribute:

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.name = S2.name AND
       S1.discount != S2.discount;

/*
This query checks if name->discount holds for this instance. Since this query
is non-empty (3286), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.name = S2.name AND
       S1.month != S2.month;

/*
This query checks if name->month holds for this instance. Since this query
is non-empty (4620), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.name = S2.name AND
       S1.price != S2.price;

/*
This query checks if name->month holds for this instance. Since this query
is empty, this functional dependency does hold for this instance.
*/

-- Move on to discount->attribute:

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.discount = S2.discount AND
       S1.name != S2.name;

/*
This query checks if dicount->name holds for this instance. Since this query
is non-empty (61398), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.discount = S2.discount AND
       S1.month != S2.month;

/*
This query checks if discount->month holds for this instance. Since this query
is non-empty (48032), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.discount = S2.discount AND
       S1.price != S2.price;

/*
This query checks if discount->price holds for this instance. Since this query
is non-empty (55170), this functional dependency does hold for this instance.
*/

-- Move on to month->attribute:

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.month = S2.month AND
       S1.name != S2.name;

/*
This query checks if month->name holds for this instance. Since this query
is non-empty (14700), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.month = S2.month AND
       S1.discount != S2.discount;

/*
This query checks if month->discount holds for this instance. Since this query
is empty, this functional dependency does hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.month = S2.month AND
       S1.price != S2.price;

/*
This query checks if month->price holds for this instance. Since this query
is non-empty (13208), this functional dependency does hold for this instance.
*/

-- Lastly, move on to price->attribute:

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.price = S2.price AND
       S1.name != S2.name;

/*
This query checks if price->name holds for this instance. Since this query
is non-empty (17906), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.price = S2.price AND
       S1.discount != S2.discount;

/*
This query checks if price->discount holds for this instance. Since this query
is non-empty (14964), this functional dependency does not hold for this instance.
*/

SELECT COUNT(*)
  FROM Sales AS S1, Sales AS S2
 WHERE S1.price = S2.price AND
       S1.month != S2.month;

/*
This query checks if price->month holds for this instance. Since this query
is non-empty (21034), this functional dependency does hold for this instance.
*/

/*
After checking the simple non-trivial functional dependencies, we currently
have: name->price, month->discount, and thus name,month->price,discount.
*/

/*
After checking with the dataset/running SQL queries, every other FD is either
invalid, or it can be built from name->price, month->discount, thus these are
our only two FDs.
*/

-- Subpart c:

/*
Given the relational schema S(name,discount,month,price) with functional
dependencies name->price and month->discount, our goal is to decompose this
schema into BCNF. If we start with the FD name->price, then we see that the
closure of name is {name,price}, hence S is not in BCNF. Thus we decompose S
into S1(name,price) and S2(name,discount,month). S1 is in BCNF, so we will move
onto S2. We can now use the FD month->discount, the closure of month is
{month, discount}, hence S2 is not in BCNF. Thus we decompose S2 into
S3(month,discount) and S4(name,month). Both of these relations are in BCNF,
hence decomposing S leaves us with the following set of relations:
S1(name,price), S3(month,discount), and S4(name,month).
*/

CREATE TABLE S1 (
    name VARCHAR(255) PRIMARY KEY,
    price INT
);

CREATE TABLE S3 (
    month VARCHAR(9) PRIMARY KEY,
    discount VARCHAR(255)
);

CREATE TABLE S4 (
    name VARCHAR(255) REFERENCES S1(name),
    month VARCHAR(9) REFERENCES S3(month)
);

-- Subpart d:

INSERT INTO S1
SELECT DISTINCT name, price
  FROM Sales;

SELECT COUNT(*)
  FROM S1;

/* 
Select the row count from relation S1. This table has 36 rows.
Note: If the import includes the attribute row, the count becomes 37.
*/

INSERT INTO S3
SELECT DISTINCT month, discount
  FROM Sales;

SELECT COUNT(*)
  FROM S3;

/* 
Select the row count from relation S3. This table has 12 rows.
Note: If the import includes the attribute row, the count becomes 13.
*/

INSERT INTO S4
SELECT DISTINCT month, name
  FROM Sales;

SELECT COUNT(*)
  FROM S4;

/* 
Select the row count from relation S4. This table has 426 rows.
Note: If the import includes the attribute row, the count becomes 427.
*/
