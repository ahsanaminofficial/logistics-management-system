DROP TABLE IF EXISTS MAXID;
CREATE TABLE MAXID( ID int,
                    sellers int,
                    products int);
DESCRIBE MAXID;

DELETE FROM MAXID WHERE ID = 0;
INSERT INTO MAXID(ID, sellers, products)
VALUES (0,0,0);

