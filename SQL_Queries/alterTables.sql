USE LMS;

ALTER TABLE SellerProduct
ADD FOREIGN KEY (sellerID) REFERENCES Seller(sellerID);

ALTER TABLE SellerProduct
ADD FOREIGN KEY (productID) REFERENCES Product(trackingID);

ALTER TABLE ClientProduct
ADD FOREIGN KEY (clientPhoneNumber) REFERENCES Client(phoneNumber);

ALTER TABLE ClientProduct
ADD FOREIGN KEY (productID) REFERENCES Product(trackingID);

ALTER TABLE Product
ADD FOREIGN KEY (sellerID) REFERENCES Seller(sellerID);

ALTER TABLE Product 
ADD FOREIGN KEY (warehouseID) REFERENCES Warehouse(warehouseID);

ALTER TABLE Product
ADD FOREIGN KEY (clientPhoneNumber) REFERENCES Client(phoneNumber);