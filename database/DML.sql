
-- ####################################################################
-- The BROWSE customers.html Page
-- ####################################################################

-- get all Customers
SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email' FROM Customers;

-- add a new Customer
INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES
(:nameInput, :phoneInput, :emailInput);

-- update a Customer
SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email'
FROM Customers
WHERE customer_id = :customer_id_selected_from_browse_customers_page;

UPDATE Customers
SET customer_name = :nameInput, customer_phone = :phoneInput, customer_email = :emailInput
WHERE customer_id = :customer_id_from_the_update_form;

-- delete a Customer
DELETE FROM Customers WHERE customer_id = :customer_id_selected_from_browse_customers_page;

-- ####################################################################
-- The BROWSE products.html Page
-- ####################################################################

-- get all Products
SELECT product_id AS 'ID', product_description AS 'Description', product_price AS 'Price' FROM Products;

-- add a new Product
INSERT INTO Products (product_description, product_price) VALUES
(:descriptionInput, :priceInput);

-- update a Product
SELECT product_id AS 'ID', product_description AS 'Description', product_price AS 'Price'
FROM Products
WHERE product_id = :product_id_selected_from_browse_products_page;

UPDATE Products
SET product_description = :descriptionInput, product_price = :priceInput
WHERE product_id = :product_id_from_the_update_form;

-- delete a Product
DELETE FROM Products WHERE product_id = :product_id_selected_from_browse_products_page;

-- ####################################################################
-- The BROWSE stores.html Page
-- ####################################################################

-- get all Stores
SELECT store_id AS 'ID', store_number AS 'Store Number', store_phone AS 'Phone', store_email AS 'Email' FROM Stores;

-- add a new Store
INSERT INTO Stores (store_number, store_phone, store_email) VALUES
(:numberInput, :phoneInput, :emailInput);

-- update a Store
SELECT store_id AS 'ID', store_number AS 'Store Number', store_phone AS 'Phone', store_email AS 'Email'
FROM Stores
WHERE store_id = :store_id_selected_from_browse_stores_page;

UPDATE Stores
SET store_number = :numberInput, store_phone = :phoneInput, store_email = :emailInput
WHERE store_id = :store_id_from_the_update_form;

-- delete a Store
DELETE FROM Stores WHERE store_id = :store_id_selected_from_browse_stores_page;

-- ####################################################################
-- The BROWSE stores-products.html Page
-- ####################################################################

-- get all Store Products
SELECT store_product_id AS 'ID', Stores.store_number AS 'Store Number', Products.product_description AS 'Product', number_in_stock AS 'In Stock'
FROM StoreProducts
INNER JOIN Stores
ON Stores.store_id = StoreProducts.store_id
INNER JOIN Products
ON Products.product_id = StoreProducts.product_id;

-- get all Store IDs and Numbers to populate Store dropdown
SELECT store_id, store_number FROM Stores;

-- get all Product IDs and Descriptions to populate Product dropdown
SELECT product_id, product_description FROM Products;

-- add a new Store Product
INSERT INTO StoreProducts (store_id, product_id, number_in_stock) VALUES
(:store_id_from_dropdown_Input, :product_id_from_dropdown_Input, :number_in_stock_Input);

-- update a Store Product
SELECT store_product_id AS 'ID', Stores.store_number AS 'Store Number', Products.product_description AS 'Product', number_in_stock AS 'In Stock'
FROM StoreProducts
INNER JOIN Stores
ON Stores.store_id = StoreProducts.store_id
INNER JOIN Products
ON Products.product_id = StoreProducts.product_id
WHERE store_product_id = :store_product_id_selected_from_browse_stores_page;

UPDATE StoreProducts
SET store_id = :store_id_from_dropdown_Input, product_id = :product_id_from_dropdown_Input, number_in_stock = :number_in_stock_Input
WHERE store_product_id = :store_product_id_from_the_update_form;

-- delete a Store Product
DELETE FROM StoreProducts WHERE store_product_id = :store_product_id_selected_from_browse_stores_page;

-- ####################################################################
-- The BROWSE orders.html Page
-- ####################################################################

-- get all Orders
SELECT order_id AS 'ID', order_date AS 'Date', Customers.customer_name AS 'Customer', Stores.store_number AS 'Store Number', order_notes AS 'Notes'
FROM Orders
LEFT JOIN Customers
ON Customers.customer_id = Orders.customer_id
LEFT JOIN Stores
ON Stores.store_id = Orders.store_id;

-- get all Order Details
SELECT order_detail_id AS 'ID', order_id AS 'Order ID', Products.product_description AS 'Product', order_quantity AS 'Quantity', line_total AS 'Line Total'
FROM OrderDetails
INNER JOIN Products
ON Products.product_id = OrderDetails.product_id;

-- get all Customer IDs and Names to populate Customer dropdown
SELECT customer_id, customer_name FROM Customers;

-- get all Store IDs and Numbers to populate Store dropdown
SELECT store_id, store_number FROM Stores;

-- get all Product IDs and Descriptions to populate Product dropdown
SELECT product_id, product_description FROM Products;

-- get all Order IDs to populate Order ID dropdown
SELECT order_id, CONCAT(order_id, ' | ', order_date, ' | ', Customers.customer_name, ' | ', Stores.store_number) AS 'Order' 
FROM Orders 
INNER JOIN Customers ON Customers.customer_id = Orders.customer_id 
INNER JOIN Stores ON Stores.store_id = Orders.store_id;

-- get all Order IDs where Customer is NuLL to populate Order ID dropdown
SELECT order_id, CONCAT(order_id, ' | ', order_date, ' | ', 'None', ' | ', Stores.store_number) AS 'Order' 
FROM Orders 
INNER JOIN Stores ON Stores.store_id = Orders.store_id 
WHERE Orders.customer_id is NULL;

-- add a new Order
INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES
(:dateInput, :customer_id_from_dropdown_Input, :store_id_from_dropdown_Input, :order_notes_Input);

-- add a new Order Detail
INSERT INTO OrderDetails (order_id, product_id, order_quantity, line_total) VALUES
(:order_id_from_dropdown_Input, :product_id_from_dropdown_Input, :order_quantity_Input, :line_total_Input);

-- delete an Order
DELETE FROM Orders WHERE order_id = :order_id_selected_from_browse_orders_page;
