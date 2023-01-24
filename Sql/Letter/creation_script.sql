-- File: create_db.sql
-- Suggest use contacts.db

DROP TABLE IF EXISTS Contacts;
CREATE TABLE People (
    personID INTEGER PRIMARY KEY,
    prefix TEXT DEFAULT '',
    first TEXT DEFAULT '',
    initial TEXT DEFAULT '',
    last TEXT DEFAULT '',
    suffix TEXT DEFAULT '',
    company TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    land_line TEXT DEFAULT '',
    mobile TEXT DEFAULT '',
    address TEXT DEFAULT '',
    address1 TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT '',
    birthday TEXT DEFAULT '',
    extra TEXT DEFAULT ''
    );


