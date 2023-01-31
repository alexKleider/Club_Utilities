-- File: create_tables.sql
-- Suggest use club.db
-- parsed by add_data.py to set up tables
-- see associated specifications.txt file

-- first,last,phone,address,town,state,postal_code,country,
--           email,dues,dock,kayak,mooring,status

DROP TABLE IF EXISTS People;
CREATE TABLE People (
    personID INTEGER PRIMARY KEY,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    suffix TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Members;
CREATE TABLE Members (
    memberID INTEGER PRIMARY KEY,
    personID UNIQUE
    );

DROP TABLE IF EXISTS Applicants;
CREATE TABLE Applicants (
    applicantID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL UNIQUE,
    app_rcvd TEXT NOT NULL,
    fee_rcvd TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    inducted TEXT DEFAULT '',
    dues_paid TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Sponsors;
CREATE TABLE Sponsors (
    personID INTEGER NOT NULL,
    sponsorID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Stati;
CREATE TABLE Stati (
    statusID INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    text TEXT NOT NULL
    );

DROP TABLE IF EXISTS Person_Status;
CREATE TABLE Person_Status (
    personID INTEGER NOT NULL,
    statusID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Attrition;
CREATE TABLE Attrition (
    attritionID INTEGER PRIMARY KEY,
    oldID INTEGER NOT NULL,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT '',
    app_rcvd TEXT NOT NULL,
    fee_rcvd TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    inducted TEXT DEFAULT '',
    sponsor1 TEXT DEFAULT '',
    sponsor2 TEXT DEFAULT ''
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


