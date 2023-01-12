-- File: create_tables.sql
-- Suggest use club.db

DROP TABLE IF EXISTS people;
CREATE TABLE people (
    PersonID INTEGER PRIMARY KEY,
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

DROP TABLE IF EXISTS sponsors;
CREATE TABLE sponsors (
    applicantID INTEGER NOT NULL,
    sponsorID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS stati;
CREATE TABLE stati (
    StatusID INTEGER PRIMARY KEY,
    status TEXT NOT NULL
    );

DROP TABLE IF EXISTS person_status;
CREATE TABLE person_status (
        personID INTEGER NOT NULL,
        sponsorID INTEGER NOT NULL
        );
