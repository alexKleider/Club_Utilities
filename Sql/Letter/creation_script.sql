-- File: create_db.sql
-- Suggest use contacts.db

DROP TABLE IF EXISTS Contacts;
CREATE TABLE People (
    personID INTEGER PRIMARY KEY,
    prefix TEXT DEFAULT '',
    first TEXT NOT NULL,
    initial TEXT DEFAULT '',
    last TEXT NOT NULL,
    suffix TEXT DEFAULT '',
    land_line TEXT DEFAULT '',
    mobile TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT '',
    birthday TEXT DEFAULT '',
    extra TEXT DEFAULT ''
    );

