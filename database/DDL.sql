-- Group 56: Dania Magana and August Frisk

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Customers Table
DROP TABLE IF EXISTS Customers;
CREATE TABLE Customers (
    customer_id int NOT NULL AUTO_INCREMENT,
    customer_name varchar(255) NOT NULL,
    customer_phone varchar(20) NOT NULL,
    customer_email varchar(255) NOT NULL,
    PRIMARY KEY (customer_id)
);

-- Example Data for Customers Table
INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES
('Ava Moreno', '(562) 201-9464', 'ava.moreno@example.com'),
('Oscar Mitchell', '(555) 330-8216', 'oscar.mitchell@example.com'),
('Daryl Caldwell', '(317) 476-7082', 'daryl.caldwell@example.com'),
('Lorraine Rogers', '(967) 508-1735', 'lorraine.rogers@example.com'),
('Ann Harris', '(246) 350-0973', 'ann.harris@example.com');

-- Products Table
DROP TABLE IF EXISTS Products;
CREATE TABLE Products (
    product_id int NOT NULL AUTO_INCREMENT,
    product_description varchar(255) NOT NULL UNIQUE,
    product_price decimal(19,2) NOT NULL,
    PRIMARY KEY (product_id)
);

-- Example Data for Products Table
INSERT INTO Products (product_description, product_price) VALUES
('PlayStation 5', 499.99),
('Five Nights at Freddy''s Collectible Plush', 12.99),
('Super Mario Odyssey', 54.99),
('Nintendo Switch - OLED Model', 349.99),
('Elden Ring', 59.99);

-- Stores Table
DROP TABLE IF EXISTS Stores;
CREATE TABLE Stores (
    store_id int NOT NULL AUTO_INCREMENT,
    store_number varchar(50) NOT NULL UNIQUE,
    store_phone varchar(20) NOT NULL,
    store_email varchar(255) NOT NULL,
    PRIMARY KEY (store_id)
);

-- Example Data for Stores Table
INSERT INTO Stores (store_number, store_phone, store_email) VALUES
('1', '(268) 432-6210', 'heroelectronics1@email.com'),
('17', '(679) 700-6746', 'heroelectronics2@email.com'),
('56', '(983) 821-8911', 'heroelectronics3@email.com'),
('82', '(385) 458-6153', 'heroelectronics4@email.com'),
('100', '(642) 936-9797', 'heroelectronics5@email.com');

-- Orders Table
DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders (
    order_id int NOT NULL AUTO_INCREMENT,
    order_date date NOT NULL,
    customer_id int,
    store_id int NOT NULL,
    order_notes text DEFAULT '',
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
    ON DELETE CASCADE
);

-- Example Data for Orders Table
INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES
('2023-05-01', (SELECT customer_id FROM Customers WHERE customer_name = 'Oscar Mitchell'), (SELECT store_id FROM Stores WHERE store_number = '56'), DEFAULT),
('2023-05-01', (SELECT customer_id FROM Customers WHERE customer_name = 'Ann Harris'), (SELECT store_id FROM Stores WHERE store_number = '56'), DEFAULT),
('2023-04-28', (SELECT customer_id FROM Customers WHERE customer_name = 'Lorraine Rogers'), (SELECT store_id FROM Stores WHERE store_number = '17'), DEFAULT),
('2023-04-27', (SELECT customer_id FROM Customers WHERE customer_name = 'Lorraine Rogers'), (SELECT store_id FROM Stores WHERE store_number = '17'), DEFAULT),
('2023-01-15', NULL, (SELECT store_id FROM Stores WHERE store_number = '100'), 'Store Transfer to Store Number 17');

-- StoreProducts Table
DROP TABLE IF EXISTS StoreProducts;
CREATE TABLE StoreProducts (
    store_product_id int NOT NULL AUTO_INCREMENT,
    store_id int NOT NULL,
    product_id int NOT NULL,
    number_in_stock int NOT NULL,
    PRIMARY KEY (store_product_id),
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE,
    UNIQUE (store_id, product_id)
);

-- Example Data for StoreProducts
INSERT INTO StoreProducts (store_id, product_id, number_in_stock) VALUES
((SELECT store_id FROM Stores WHERE store_number = '17'), (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 0),
((SELECT store_id FROM Stores WHERE store_number = '17'), (SELECT product_id FROM Products WHERE product_description = 'Five Nights at Freddy''s Collectible Plush'), 11),
((SELECT store_id FROM Stores WHERE store_number = '17'), (SELECT product_id FROM Products WHERE product_description = 'Super Mario Odyssey'), 10),
((SELECT store_id FROM Stores WHERE store_number = '56'), (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 5),
((SELECT store_id FROM Stores WHERE store_number = '100'), (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 7);

-- OrderDetails Table
DROP TABLE IF EXISTS OrderDetails;
CREATE TABLE OrderDetails (
    order_detail_id int NOT NULL AUTO_INCREMENT,
    order_id int NOT NULL,
    product_id int NOT NULL,
    order_quantity int NOT NULL,
    line_total decimal(19,2) NOT NULL,
    PRIMARY KEY (order_detail_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE,
    UNIQUE (order_id, product_id)
);

-- Example Data for OrderDetails Table
INSERT INTO OrderDetails (order_id, product_id, order_quantity, line_total) VALUES
(1, (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 1, 499.99),
(1, (SELECT product_id FROM Products WHERE product_description = 'Elden Ring'), 1, 59.99),
(2, (SELECT product_id FROM Products WHERE product_description = 'Five Nights at Freddy''s Collectible Plush'), 2, 25.98),
(3, (SELECT product_id FROM Products WHERE product_description = 'Super Mario Odyssey'), 1, 54.99),
(5, (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 3, 1499.97);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
