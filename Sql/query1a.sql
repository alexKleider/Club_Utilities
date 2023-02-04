
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People, Person_Status, Stati
    WHERE Person_Status.statusID = (SELECT statusID  
        FROM Stati WHERE key = 'aw')
    AND Person_Status.personID = People.personID 
    ;
