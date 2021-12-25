DELETE FROM Product WHERE trackingID = "P01";
INSERT INTO Product(trackingID, sellerID, warehouseID, currentLocation, 
                    productRoute, paymentStatus, price, clientPhoneNumber)
VALUES ("P01", "S01", "W03", "W03", 
        "Lahore/Islamabad/Multan", 0, 1200, "03014884962");
UPDATE MAXID SET MAXID.products = MAXID.products+1;
