
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
('Samuel Gilbert', '(511) 276-3926', 'samuel.gilbert@example.com'),
('Max Daniels', '(730) 962-9938', 'max.daniels@example.com'),
('Leroy Gardner', '(688) 467-6596', 'leroy.gardner@example.com'),
('Theresa Reed', '(906) 472-0810', 'theresa.reed@example.com'),
('Billie Murphy', '(941) 431-8455', 'billie.murphy@example.com');

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
('Nitendo Switch', 249.99),
('XBOX Series S', 299.99),
('XBOX Game Pass', 9.99),
('Overwatch: Ultimate Edition', 59.99);

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
('1', '(923) 732-1673', 'ttgshophadong@example.com'),
('2', '(680) 619-0762', 'ttgshophoangmai@example.com'),
('3', '(475) 427-2386', 'ttgshopquan1@example.com'),
('4', '(441) 514-1164', 'ttgshopdanang@example.com'),
('5', '(900) 409-0540', 'ttgshopquan10@example.com');

-- Orders Table
DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders (
    order_id int NOT NULL AUTO_INCREMENT,
    order_date date NOT NULL,
    customer_id int,
    store_id int NOT NULL,
    order_notes text DEFAULT ('None'),
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
    ON DELETE CASCADE
);

-- Example Data for Orders Table
INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES
('2023-05-01', (SELECT customer_id FROM Customers WHERE customer_name = 'Samuel Gilbert'), (SELECT store_id FROM Stores WHERE store_number = '1'), DEFAULT),
('2023-05-01', (SELECT customer_id FROM Customers WHERE customer_name = 'Billie Murphy'), (SELECT store_id FROM Stores WHERE store_number = '2'), DEFAULT),
('2023-04-28', (SELECT customer_id FROM Customers WHERE customer_name = 'Theresa Reed'), (SELECT store_id FROM Stores WHERE store_number = '4'), DEFAULT),
('2023-04-27', (SELECT customer_id FROM Customers WHERE customer_name = 'Leroy Gardner'), (SELECT store_id FROM Stores WHERE store_number = '3'), DEFAULT),
('2023-01-15', NULL, (SELECT store_id FROM Stores WHERE store_number = '5'), 'Store Transfer to Store Number 2');

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
((SELECT store_id FROM Stores WHERE store_number = '1'), (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 1),
((SELECT store_id FROM Stores WHERE store_number = '1'), (SELECT product_id FROM Products WHERE product_description = 'XBOX Series S'), 12),
((SELECT store_id FROM Stores WHERE store_number = '5'), (SELECT product_id FROM Products WHERE product_description = 'Nitendo Switch'), 10),
((SELECT store_id FROM Stores WHERE store_number = '4'), (SELECT product_id FROM Products WHERE product_description = 'Nitendo Switch'), 5),
((SELECT store_id FROM Stores WHERE store_number = '2'), (SELECT product_id FROM Products WHERE product_description = 'Overwatch: Ultimate Edition'), 7);

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
(1, (SELECT product_id FROM Products WHERE product_description = 'Nitendo Switch'), 1, 249.99),
(2, (SELECT product_id FROM Products WHERE product_description = 'Nitendo Switch'), 2, 499.98),
(3, (SELECT product_id FROM Products WHERE product_description = 'XBOX Series S'), 1, 299.99),
(5, (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 3, 1499.97);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
