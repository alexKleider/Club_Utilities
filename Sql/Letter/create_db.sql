-- File: create_db.sql
-- Suggest use contacts.db

DROP TABLE IF EXISTS Contacts;
CREATE TABLE People (
    personID INTEGER PRIMARY KEY,
    prefix TEXT DEFAULT '',
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    suffix TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT '',
    phone TEXT DEFAULT ''
    );


