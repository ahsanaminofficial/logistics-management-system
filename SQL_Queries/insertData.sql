USE LMS;

INSERT INTO LoginInfo(ID, userName, userPassword)
VALUES ("ID", "userName", "userPassword");

INSERT INTO Client(phoneNumber, clientAddress, city)
VALUES ("phoneNumber", "clientAddress", "city");

INSERT INTO Seller(sellerID, sellerName, phoneNumber, city)
VALUES ("sellerID", "sellerName", "phoneNumber", "city");

INSERT INTO Warehouse(warehouseID, city)
VALUES ("warehouseID", "city");

INSERT INTO Product(trackingID, sellerID, warehouseID, currentLocation, productRoute, paymentStatus, price, clientPhoneNumber)
VALUES ("trackingID", "sellerID", "warehouseID", "currentLocation", "productRoute", "paymentStatus", "price", "clientPhoneNumber");

INSERT INTO SellerProduct(sellerID, productID, weightPrice, deliveryPrice, sellerPrice) 
VALUES ("sellerID", "productID", "weightPrice", "deliveryPrice", "sellerPrice");

INSERT INTO ClientProduct(clientPhoneNumber, productID, deliveryAddress)
VALUES ("clientPhoneNumber", "productID", "deliveryAddress");

INSERT INTO Rider(riderID, riderName, warehouseID, productID)
VALUES ("riderID", "riderName", "warehouseID", "productID");

