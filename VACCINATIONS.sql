CREATE DATABASE VACCINATIONS;

USE VACCINATIONS;
-- Create table for communities
CREATE TABLE Community (
    community_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    population INT
);

-- Create table for demographics
CREATE TABLE Demographic (
    demographic_id INT PRIMARY KEY,
    age_group VARCHAR(50),
    gender VARCHAR(10)
);

-- Create table for vaccination types
CREATE TABLE Vaccination_Type (
    vaccine_id INT PRIMARY KEY,
    vaccine_name VARCHAR(100),
    manufacturer VARCHAR(100)
);

-- Create table for vaccination records
CREATE TABLE Vaccination_Record (
    record_id INT PRIMARY KEY,
    community_id INT,
    demographic_id INT,
    vaccine_id INT,
    date_administered DATE,
    doses_administered INT,
    FOREIGN KEY (community_id) REFERENCES Community(community_id),
    FOREIGN KEY (demographic_id) REFERENCES Demographic(demographic_id),
    FOREIGN KEY (vaccine_id) REFERENCES Vaccination_Type(vaccine_id)
);




-- Insert sample data into Community
INSERT INTO Community (community_id, name, region, population) VALUES
(1, 'Greenfield', 'North', 15000),
(2, 'Rivertown', 'South', 22000);

-- Insert sample data into Demographic
INSERT INTO Demographic (demographic_id, age_group, gender) VALUES
(1, '0-18', 'All'),
(2, '19-35', 'All'),
(3, '36-60', 'All'),
(4, '60+', 'All');

-- Insert sample data into Vaccination_Type
INSERT INTO Vaccination_Type (vaccine_id, vaccine_name, manufacturer) VALUES
(1, 'Vaccine A', 'PharmaCorp'),
(2, 'Vaccine B', 'HealthMeds');

-- Insert sample data into Vaccination_Record
INSERT INTO Vaccination_Record (record_id, community_id, demographic_id, vaccine_id, date_administered, doses_administered) VALUES
(1, 1, 1, 1, '2024-01-15', 500),
(2, 1, 2, 1, '2024-01-15', 700),
(3, 1, 1, 2, '2024-02-15', 300),
(4, 2, 3, 1, '2024-01-20', 600),
(5, 2, 4, 2, '2024-03-10', 200);

