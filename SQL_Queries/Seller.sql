DELETE FROM Seller WHERE sellerID = "S01";
INSERT INTO Seller(sellerID, sellerName, phoneNumber, city)
VALUES ("S01", "Faaiq", "03014884962", "Lahore");
UPDATE MAXID SET MAXID.sellers = MAXID.sellers+1;

DELETE FROM Seller WHERE sellerID = "S02";
INSERT INTO Seller(sellerID, sellerName, phoneNumber, city)
VALUES ("S02", "Haashim", "03014884962", "Karachi");
UPDATE MAXID SET MAXID.sellers = MAXID.sellers+1;

DELETE FROM Seller WHERE sellerID = "S03";
INSERT INTO Seller(sellerID, sellerName, phoneNumber, city)
VALUES ("S03", "Sarah", "03014884962", "Islamabad");
UPDATE MAXID SET MAXID.sellers = MAXID.sellers+1;

DELETE FROM Seller WHERE sellerID = "S04";
INSERT INTO Seller(sellerID, sellerName, phoneNumber, city)
VALUES ("S04", "ABD", "03014884962", "Multan");
UPDATE MAXID SET MAXID.sellers = MAXID.sellers+1;