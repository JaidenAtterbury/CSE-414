CREATE TABLE Caregivers (
    Username VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Patients (
    Username VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time DATE,
    Username VARCHAR(255) NOT NULL REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name VARCHAR(255),
    Doses INT,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointments (
    Aid INT IDENTITY(1,1),
    Date DATE,
    Puname VARCHAR(255) NOT NULL REFERENCES Patients(Username),
    Cuname VARCHAR(255) NOT NULL REFERENCES Caregivers(Username),
    Vname VARCHAR(255) NOT NULL REFERENCES Vaccines(Name),
    PRIMARY KEY (Aid)
);