--  query2.sql


-- TA: ID, name 
-- TI: taID, tbID      -- mapping or intersection table
-- TB: ID, quality

-- SELECT  TA.name, TB.quality
-- FROM TA
-- INNER JOIN TI
--     ON TA.ID = TI.taID
-- INNER JOIN TB
--     ON TB.ID =TI.btID

SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People
    LEFT JOIN Person_Status
        ON People.personID = Person_Status.personID
    LEFT JOIN Stati
        ON Person_Status.personID = Stati.statusID
--  IF Stati.key = 'aw'
    ;
