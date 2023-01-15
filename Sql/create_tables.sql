-- File: create_tables.sql
-- Suggest use club.db
-- now parsed by add_data.py rather than .read by sqlite3

DROP TABLE IF EXISTS People;
CREATE TABLE People (
    PersonID INTEGER PRIMARY KEY,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Sponsors;
CREATE TABLE Sponsors (
    applicantID INTEGER NOT NULL,
    sponsorID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Stati;
CREATE TABLE Stati (
    statusID INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    status TEXT NOT NULL
    );

DROP TABLE IF EXISTS Person_Status;
CREATE TABLE Person_Status (
    personID INTEGER NOT NULL,
    statusID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Applicant_Sponsors;
CREATE TABLE Applicant_Sponsors (
    personID INTEGER NOT NULL,
    sponsorID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Applicant_Dates;
CREATE TABLE Applicant_Dates (
    personID INTEGER NOT NULL UNIQUE,
    received TEXT NOT NULL,
    fee_paid TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    inducted TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Dues;
CREATE TABLE Dues (
    personID INTEGER UNIQUE NOT NULL,
    dues_owed NUMERIC DEFAULT 100
    );

DROP TABLE IF EXISTS Kayak_Slots;
CREATE TABLE Kayak_Slots (
    ID INTEGER NOT NULL PRIMARY KEY,
    slot_code TEXT NOT NULL UNIQUE,
    slot_name TEXT NOT NULL UNIQUE,
    slot_cost NUMERIC DEFAULT 70,
    occupant TEXT
    );

DROP TABLE IF EXISTS Moorings;
CREATE TABLE Moorings (
    mooringID INTEGER NOT NULL PRIMARY KEY,
    mooring_code TEXT NOT NULL UNIQUE,
    mooring_name TEXT NOT NULL UNIQUE,
    mooring_cost NUMERIC NOT NULL,
    occupant TEXT
    );

DROP TABLE IF EXISTS Dock_Privileges;
CREATE TABLE Dock_Privileges (
    member TEXT NOT NULL UNIQUE,
    cost NUMERIC DEFAULT 75
    );


