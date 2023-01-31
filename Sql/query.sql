-- query
-- sqlite> .tables
-- Applicants       Dues             Moorings         Sponsors       
-- Attrition        Kayak_Slots      People           Stati          
-- Dock_Privileges  Members          Person_Status
-- People p; Person_Status; Stati
SELECT People.personID, first, last
    FROM People, Person_status
    WHERE Person_Status.personID = People.personID 
    AND Person_Status.statusID = (SELECT statusID  
        FROM Stati WHERE key = 'aw');

-- sqlite> SELECT title FROM book, book_author
--    ...> WHERE book_author.bookID = book.ID
--    ...> AND book_author.authorID = (SELECT ID FROM author
--    ...>                             WHERE name = "Jane Austin");
-- sqlite> SELECT name FROM author, book_author
--    ...> WHERE book_author.authorID = author.ID
--    ...> AND book_author.bookID = (SELECT ID FROM book
--    ...>                           WHERE title = "The UML User Guide");

