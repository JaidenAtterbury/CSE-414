-- Part 2: E/R to Schema:

-- Subpart a:

CREATE TABLE Person (
    ssn INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE InsuranceCo (
    name VARCHAR(255) PRIMARY KEY,
    phone INT
);

CREATE TABLE Vehicle (
    licensePlate VARCHAR(255) PRIMARY KEY,
    year INT,
    name VARCHAR(255) REFERENCES InsuranceCo(name),
    maxLiability REAL,
    ssn INT REFERENCES Person(ssn)
);

CREATE TABLE Driver (
    ssn INT REFERENCES Person(ssn),
    driverID INT,
    PRIMARY KEY (ssn)
);

CREATE TABLE NonProfessionalDriver (
    ssn INT REFERENCES Driver(ssn),
    PRIMARY KEY (ssn)
);

CREATE TABLE ProfessionalDriver (
    ssn INT REFERENCES Driver(ssn),
    medicalHistory VARCHAR(255),
    PRIMARY KEY (ssn)
);

CREATE TABLE Car (
    licensePlate VARCHAR(255) REFERENCES Vehicle(licensePlate),
    make VARCHAR(255),
    PRIMARY KEY (licensePlate)
);

CREATE TABLE Truck (
    licensePlate VARCHAR(255) REFERENCES Vehicle(licensePlate),
    ssn INT REFERENCES ProfessionalDriver(ssn),
    capacity INT,
    PRIMARY KEY (licensePlate)
);

CREATE TABLE Drives (
    ssn INT REFERENCES NonProfessionalDriver(ssn),
    licensePlate VARCHAR(255) REFERENCES Car(licensePlate),
    PRIMARY KEY (ssn, licensePlate)
);

/*
Subpart b:

The relation in my relational schema that represent the relationship "Insures,"
is the relation named Vehicles. Since this relationship is a many-to-one relationship,
it needs to be stored in the entity set tables to prevent any unnecessary redundancy.
Since the relationship can be described in words as, "each vehicle is insure by at
most one insurance company," it follows that the relation InsuranceCo is constrained
to one. With that said, this implies that in order to capture this relationship with
the correct constraints, we needed to include it in the Vehicle relation. Hence each
vehicle will have at most one maxLiability and one insuranceName.
*/

/*
Subpart c:

In my schema, the relationship "Drives" is represented in its own table, while
the relationship "Operates" is represented in the "Truck" relation. The reason
for the difference in the representation of the relationships, is that the "Drives"
relationship is a many-to-many relationship, and hence it must have its own relation
to fully define the relationship properly. On the other hand, the relationship
"Operates," is in the "Truck" relation, because it is a many-to-one relationship
and thus it needs to be stored in the entity set tables to prevent any unnecessary
redundancy. Furthermore, since the arrow points towards "ProfessionalDriver,"
which implies the Drivers are constrained to one, it follows that the relationship
should be stored in the "Truck" relation in order to fully define the relationship
properly.
*/
