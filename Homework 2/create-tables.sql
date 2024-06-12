PRAGMA foreign_keys=ON;

CREATE TABLE Carriers (
    cid VARCHAR(7) PRIMARY KEY,
    name VARCHAR(83));

CREATE TABLE Months (
    mid INT PRIMARY KEY,
    month VARCHAR(9));

CREATE TABLE Weekdays (
    did INT PRIMARY KEY,
    day_of_week VARCHAR(9));

CREATE TABLE Flights (
    fid INT PRIMARY KEY,
    month_id INT REFERENCES Months(mid),
    day_of_month INT,
    day_of_week_id INT REFERENCES Weekdays(did),
    carrier_id VARCHAR(7) REFERENCES Carriers(cid),
    flight_num INT,
    origin_city VARCHAR(34),
    origin_state VARCHAR(47),
    dest_city VARCHAR(34),
    dest_state VARCHAR(46),
    departure_delay INT,
    taxi_out INT,
    arrival_delay INT,
    canceled INT,
    actual_time INT,
    distance INT,
    capacity INT,
    price INT);
