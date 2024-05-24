#!/usr/bin/env python
# encoding: utf-8


from flask import Flask, flash, render_template, redirect, request
from flask_mysqldb import MySQL
import os
from database.validation import is_valid_name, is_valid_email, is_valid_phone

app = Flask(__name__)

app.config["MYSQL_HOST"] = "sql3.freesqldatabase.com"
app.config["MYSQL_USER"] = "sql3708445"
app.config["MYSQL_PASSWORD"] = "AYCwBI6Lac"
app.config["MYSQL_DB"] = "sql3708445"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

SECRET_KEY = "TESTING"
app.secret_key = str.encode(str(SECRET_KEY))

PORT = os.environ.get("PORT")

mysql = MySQL(app)


@app.route("/")
def Home():
    return redirect("/customers")


#   _____         __
#  / ___/_ _____ / /____  __ _  ___ _______
# / /__/ // (_-</ __/ _ \/  ' \/ -_) __(_-<
# \___/\_,_/___/\__/\___/_/_/_/\__/_/ /___/
#
@app.route("/customers", methods=["GET", "POST"])
def customers():
    """Display all Customers in the database, or search for a Customer by name/phone/email."""

    if request.method == "GET":
        # Display Customer data.
        query = """SELECT
                customer_id AS 'ID',
                customer_name AS 'Name',
                customer_phone AS 'Phone',
                customer_email AS 'Email'
                FROM Customers;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("customers.j2", data=data)

    if request.method == "POST":
        # Search for a Customer by name/phone/email.
        if request.form.get("Search_Customer"):
            customer_search = request.form["customer_search"]
            search_by = request.form["search_by"]

            query = f"""SELECT 
                    customer_id AS 'ID',
                    customer_name AS 'Name',
                    customer_phone AS 'Phone',
                    customer_email AS 'Email'
                    FROM Customers WHERE {search_by} = '{customer_search}';"""
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            try:
                data[1]
            except:
                if customer_search == "":
                    flash("No results found for empty string.")
                else:
                    flash(f"No Customers found with {search_by} of {customer_search}.")

            return render_template("search_customers.j2", data=data)


@app.route("/add_customers", methods=["GET", "POST"])
def add_customers():
    """Add a Customer to the database."""

    # User presses 'Add New Customer' button on customers page.
    if request.method == "GET":
        return render_template("add_customers.j2")

    if request.method == "POST":
        # User presses 'Add Customer' button.
        if request.form.get("Add_Customer"):
            customer_name = request.form["customer_name"]
            customer_phone = request.form["customer_phone"]
            customer_email = request.form["customer_email"]

            # Validate customer_name.
            if customer_name == "":
                flash("Name cannot be empty.")
                return redirect("/add_customers")

            elif not is_valid_name(customer_name):
                flash("Name must be in the format: Firstname Lastname")
                return redirect("/add_customers")

            # Validate customer_phone.
            if customer_phone == "":
                flash("Phone cannot be empty.")
                return redirect("/add_customers")

            elif not is_valid_phone(customer_phone):
                flash("Phone must be in the format: (123) 456-7890")
                return redirect("/add_customers")

            # Validate customer_email.
            if customer_email == "":
                flash("Email cannot be empty.")
                return redirect("/add_customers")

            elif not is_valid_email(customer_email):
                flash("Email must be in the format: example@email.com")
                return redirect("/add_customers")

            # Insert new Customer into database.
            query = "INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, customer_phone, customer_email))
            mysql.connection.commit()

            return redirect("/customers")


@app.route("/delete_customers/<int:customer_id>", methods=["GET", "POST"])
def delete_customers(customer_id):
    """Delete a Customer from the database."""

    # User presses 'Delete Customer' icon on customers page.
    if request.method == "GET":
        # Display Customer data to be deleted.
        query = """SELECT
                customer_id AS 'ID',
                customer_name AS 'Name',
                customer_phone AS 'Phone', 
                customer_email AS 'Email' 
                FROM Customers WHERE customer_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchall()

        return render_template("delete_customers.j2", data=data)

    if request.method == "POST":
        # User presses 'Delete Customer' button.
        if request.form.get("Delete_Customer"):
            query = "DELETE FROM Customers WHERE customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id,))
            mysql.connection.commit()

            return redirect("/customers")


@app.route("/update_customers/<int:customer_id>", methods=["GET", "POST"])
def update_customers(customer_id):
    """Update a Customer in the database."""

    # User presses 'Update Customer' icon on customers page.
    if request.method == "GET":
        # Display Customer data to be updated.
        query = """SELECT 
                customer_id AS 'ID', 
                customer_name AS 'Name', 
                customer_phone AS 'Phone', 
                customer_email AS 'Email' 
                FROM Customers WHERE customer_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchall()

        return render_template("update_customers.j2", data=data)

    if request.method == "POST":
        # User presses 'Update Customer' button.
        if request.form.get("Update_Customer"):
            customer_name = request.form["customer_name"]
            customer_phone = request.form["customer_phone"]
            customer_email = request.form["customer_email"]

            # Validate customer_name.
            if customer_name == "":
                flash("Name cannot be empty.")
                return redirect("/update_customers")

            elif not is_valid_name(customer_name):
                flash("Name must be in the format: Firstname Lastname")
                return redirect("/update_customers")

            # Validate customer_phone.
            if customer_phone == "":
                flash("Phone cannot be empty.")
                return redirect("/update_customers")

            elif not is_valid_phone(customer_phone):
                flash("Phone must be in the format: (123) 456-7890")
                return redirect("/update_customers")

            # Validate customer_email.
            if customer_email == "":
                flash("Email cannot be empty.")
                return redirect("/update_customers")

            query = """UPDATE Customers
                    SET customer_name = %s, customer_phone = %s, customer_email = %s
                    WHERE customer_id = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(
                query, (customer_name, customer_phone, customer_email, customer_id)
            )
            mysql.connection.commit()

            return redirect("/customers")


#    ___              __         __
#   / _ \_______  ___/ /_ ______/ /____
#  / ___/ __/ _ \/ _  / // / __/ __(_-<
# /_/  /_/  \___/\_,_/\_,_/\__/\__/___/
#
@app.route("/products", methods=["GET", "POST"])
def products():
    """Display all Products in the database."""

    if request.method == "GET":
        # Display Product data.
        query = """SELECT
                product_id AS 'ID',
                product_description AS 'Description',
                product_price AS 'Price'
                FROM Products;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("products.j2", data=data)


@app.route("/add_products", methods=["GET", "POST"])
def add_products():
    """Add a Product to the database."""

    # User presses 'Add New Product' button on products page.
    if request.method == "GET":
        return render_template("add_products.j2")

    if request.method == "POST":
        # User presses 'Add Product' button.
        if request.form.get("Add_Product"):
            product_description = request.form["product_description"]
            product_price = request.form["product_price"]

            # checks if product_price is not valid
            if float(product_price) < 0:
                flash("Price cannot be less than 0.")
                return render_template("add_products.j2")

            # handles duplicate entries of unique values
            try:
                # Insert new Product into database.
                query = "INSERT INTO Products (product_description, product_price) VALUES (%s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (product_description, product_price))
                mysql.connection.commit()
                
                return redirect("/products")
            except:
                flash("Duplicate entries of Description not allowed.")
                return render_template("add_products.j2")


@app.route("/delete_products/<int:product_id>", methods=["GET", "POST"])
def delete_products(product_id):
    """Delete a Product from the database."""

    # User presses 'Delete Product' icon on products page.
    if request.method == "GET":
        # Display Product data to be deleted.
        query = """SELECT
                product_id AS 'ID', 
                product_description AS 'Description', 
                product_price AS 'Price' 
                FROM Products WHERE product_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (product_id,))
        data = cur.fetchall()

        return render_template("delete_products.j2", data=data)

    if request.method == "POST":
        # User presses 'Delete Product' button.
        if request.form.get("Delete_Product"):
            query = "DELETE FROM Products WHERE product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_id,))
            mysql.connection.commit()

            return redirect("/products")


@app.route("/update_products/<int:product_id>", methods=["GET", "POST"])
def update_products(product_id):
    """Update a Product in the database."""

    # User presses 'Update Product' icon on products page.
    if request.method == "GET":
        # Display Product data to be updated.
        query = """SELECT product_id AS 'ID', 
                product_description AS 'Description', 
                product_price AS 'Price' 
                FROM Products WHERE product_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (product_id,))
        data = cur.fetchall()

        return render_template("update_products.j2", data=data)

    if request.method == "POST":
        # User presses 'Update Product' button.
        if request.form.get("Update_Product"):
            product_description = request.form["product_description"]
            product_price = request.form["product_price"]

            # checks if product_price is not valid
            if float(product_price) < 0:
                flash("Price cannot be less than 0.")

                query = """SELECT product_id AS 'ID', 
                        product_description AS 'Description', 
                        product_price AS 'Price' 
                        FROM Products WHERE product_id = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(query, (product_id,))
                data = cur.fetchall()
                
                return render_template("update_products.j2", data=data)
            # product_price is valid
            else:
                query = """UPDATE Products
                        SET product_description = %s, product_price = %s
                        WHERE product_id = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(query, (product_description, product_price, product_id))
                mysql.connection.commit()

                return redirect("/products")


#    ______
#   / __/ /____  _______ ___
#  _\ \/ __/ _ \/ __/ -_|_-<
# /___/\__/\___/_/  \__/___/
#
@app.route("/stores", methods=["GET", "POST"])
def stores():
    """Display all Stores in the database."""

    if request.method == "GET":
        # Display Store data.
        query = """SELECT 
                store_id AS 'ID', 
                store_number AS 'Store Number', 
                store_phone AS 'Phone', 
                store_email AS 'Email' 
                FROM Stores;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("stores.j2", data=data)


@app.route("/add_stores", methods=["GET", "POST"])
def add_stores():
    """Add a Store to the database."""

    # User presses 'Add New Store' button on stores page.
    if request.method == "GET":
        return render_template("add_stores.j2")

    if request.method == "POST":
        # User presses 'Add Store' button.
        if request.form.get("Add_Store"):
            store_number = request.form["store_number"]
            store_phone = request.form["store_phone"]
            store_email = request.form["store_email"]

            # Validate store_phone.
            if store_phone == "":
                flash("Phone cannot be empty.")
                return redirect("/add_stores")

            elif not is_valid_phone(store_phone):
                flash("Phone must be in the format: (123) 456-7890")
                return redirect("/add_stores")

            # Validate store_email.
            if store_email == "":
                flash("Email cannot be empty.")
                return redirect("/add_stores")

            elif not is_valid_email(store_email):
                flash("Email must be in the format: heroelectronics1@email.com")
                return redirect("/add_stores")

            # handles duplicate entries of unique values
            try:
                # Insert new Store into database.
                query = "INSERT INTO Stores (store_number, store_phone, store_email) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (store_number, store_phone, store_email))
                mysql.connection.commit()

                return redirect("/stores")
            except:
                flash("Duplicate entries of Store Number not allowed.")
                return render_template("add_stores.j2")


@app.route("/delete_stores/<int:store_id>", methods=["GET", "POST"])
def delete_stores(store_id):
    """Delete a Store from the database."""

    # User presses 'Delete Store' icon on stores page.
    if request.method == "GET":
        # Display Store data to be deleted.
        query = """SELECT 
                store_id AS 'ID', 
                store_number AS 'Store Number',
                store_phone AS 'Phone', 
                store_email AS 'Email' 
                FROM Stores WHERE store_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (store_id,))
        data = cur.fetchall()

        return render_template("delete_stores.j2", data=data)

    if request.method == "POST":
        # User presses 'Delete Store' button.
        if request.form.get("Delete_Store"):
            query = "DELETE FROM Stores WHERE store_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_id,))
            mysql.connection.commit()

            return redirect("/stores")


@app.route("/update_stores/<int:store_id>", methods=["GET", "POST"])
def update_stores(store_id):
    """Update a Store in the database."""

    # User presses 'Update Store' icon on stores page.
    if request.method == "GET":
        # Display Store data to be updated.
        query = """SELECT store_id AS 'ID', 
                store_number AS 'Store Number', 
                store_phone AS 'Phone', 
                store_email AS 'Email' 
                FROM Stores WHERE store_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (store_id,))
        data = cur.fetchall()

        return render_template("update_stores.j2", data=data)

    if request.method == "POST":
        # User presses 'Update Store' button.
        if request.form.get("Update_Store"):
            store_number = request.form["store_number"]
            store_phone = request.form["store_phone"]
            store_email = request.form["store_email"]

            # Validate store_phone.
            if store_phone == "":
                flash("Phone cannot be empty.")
                return redirect("/update_stores")

            elif not is_valid_phone(store_phone):
                flash("Phone must be in the format: (123) 456-7890")
                return redirect("/update_stores")

            # Validate store_email.
            if store_email == "":
                flash("Email cannot be empty.")
                return redirect("/update_stores")

            elif not is_valid_email(store_email):
                flash("Email must be in the format: heroelectronics1@email.com")
                return redirect("/update_stores")

            query = """UPDATE Stores
                    SET store_number = %s, store_phone = %s, store_email = %s
                    WHERE store_id = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(query, (store_number, store_phone, store_email, store_id))
            mysql.connection.commit()

            return redirect("/stores")


#   ______                 ___              __         __
#   / __/ /____  _______   / _ \_______  ___/ /_ ______/ /____
#  _\ \/ __/ _ \/ __/ -_) / ___/ __/ _ \/ _  / // / __/ __(_-<
# /___/\__/\___/_/  \__/ /_/  /_/  \___/\_,_/\_,_/\__/\__/___/
#
@app.route("/store_products", methods=["GET"])
def store_products():
    """Display all Store Products in the database."""

    if request.method == "GET":
        # Display Store Product data.
        query = """SELECT store_product_id AS 'ID', 
                Stores.store_number AS 'Store Number', 
                Products.product_description AS 'Product', 
                number_in_stock AS 'In Stock'
                FROM StoreProducts
                INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id
                INNER JOIN Products ON Products.product_id = StoreProducts.product_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("store_products.j2", data=data)


@app.route("/add_store_products", methods=["GET", "POST"])
def add_store_products():
    """Add a Store Product to the database."""

    # User presses 'Add New Store Product' button on store_products page.
    if request.method == "GET":
        # Store ID/Number data for dropdown.
        query = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        store_data = cur.fetchall()

        # Product ID/Description data for dropdown.
        query2 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        product_data = cur.fetchall()

        return render_template(
            "add_store_products.j2", stores=store_data, products=product_data
        )

    if request.method == "POST":
        # User presses 'Add Store Product' button.
        if request.form.get("Add_Store_Product"):
            store_id = request.form["store_number"]
            product_id = request.form["product_description"]
            number_in_stock = request.form["number_in_stock"]

            # checks if number_in_stock is not valid
            if int(number_in_stock) < 0:
                flash("Number in Stock value cannot be less than 0.")
                
                # Store ID/Number data for dropdown.
                query = "SELECT store_id, store_number FROM Stores;"
                cur = mysql.connection.cursor()
                cur.execute(query)
                store_data = cur.fetchall()

                # Product ID/Description data for dropdown.
                query2 = "SELECT product_id, product_description FROM Products;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                product_data = cur.fetchall()

                return render_template(
                    "add_store_products.j2", stores=store_data, products=product_data
                )

            # handles duplicate entries of unique combination of store_id and product_id
            try:
                # Insert new Store Product into database.
                query = "INSERT INTO StoreProducts (store_id, product_id, number_in_stock) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (store_id, product_id, number_in_stock))
                mysql.connection.commit()

                return redirect("/store_products")
            except:
                flash("Duplicate entries of Store Number and Product not allowed.")
                
                # Store ID/Number data for dropdown.
                query = "SELECT store_id, store_number FROM Stores;"
                cur = mysql.connection.cursor()
                cur.execute(query)
                store_data = cur.fetchall()

                # Product ID/Description data for dropdown.
                query2 = "SELECT product_id, product_description FROM Products;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                product_data = cur.fetchall()

                return render_template(
                    "add_store_products.j2", stores=store_data, products=product_data
                )


@app.route("/delete_store_products/<int:store_product_id>", methods=["GET", "POST"])
def delete_store_products(store_product_id):
    """Delete a Store Product from the database."""

    # User presses 'Delete Store Product' icon on store_products page.
    if request.method == "GET":
        # Display Store Product data to be deleted.
        query = """SELECT
                store_product_id AS 'ID',
                Stores.store_number AS 'Store Number',
                Products.product_description AS 'Product',
                number_in_stock AS 'In Stock'
                FROM StoreProducts
                INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id
                INNER JOIN Products ON Products.product_id = StoreProducts.product_id
                WHERE store_product_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (store_product_id,))
        data = cur.fetchall()

        return render_template("delete_store_products.j2", data=data)

    if request.method == "POST":
        # User presses 'Delete Store Product' button.
        if request.form.get("Delete_Store_Product"):
            query = "DELETE FROM StoreProducts WHERE store_product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_product_id,))
            mysql.connection.commit()

            return redirect("/store_products")


@app.route("/update_store_products/<int:store_product_id>", methods=["GET", "POST"])
def update_store_products(store_product_id):
    """Update a Store Product in the database."""

    # User presses 'Update Store Product' icon on store_products page.
    if request.method == "GET":
        # Display Store Product data to be updated.
        query = """SELECT
                store_product_id AS 'ID',
                Stores.store_number AS 'Store Number',
                Products.product_description AS 'Product',
                number_in_stock AS 'In Stock'
                FROM StoreProducts
                INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id
                INNER JOIN Products ON Products.product_id = StoreProducts.product_id
                WHERE store_product_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (store_product_id,))
        data = cur.fetchall()

        # Store ID/Number data for dropdown.
        query2 = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        store_data = cur.fetchall()

        # Product ID/Description data for dropdown.
        query3 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()

        return render_template(
            "update_store_products.j2",
            data=data,
            stores=store_data,
            products=product_data,
        )

    if request.method == "POST":
        # User presses 'Update Store Product' button.
        if request.form.get("Update_Store_Product"):
            store_id = request.form["store_number"]
            product_id = request.form["product_description"]
            number_in_stock = request.form["number_in_stock"]

            # checks if number_in_stock is not valid
            if int(number_in_stock) < 0:
                flash("Number in Stock value cannot be less than 0.")

                query = """SELECT
                        store_product_id AS 'ID',
                        Stores.store_number AS 'Store Number',
                        Products.product_description AS 'Product',
                        number_in_stock AS 'In Stock'
                        FROM StoreProducts
                        INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id
                        INNER JOIN Products ON Products.product_id = StoreProducts.product_id
                        WHERE store_product_id = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(query, (store_product_id,))
                data = cur.fetchall()

                # Store ID/Number data for dropdown.
                query2 = "SELECT store_id, store_number FROM Stores;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                store_data = cur.fetchall()

                # Product ID/Description data for dropdown.
                query3 = "SELECT product_id, product_description FROM Products;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                product_data = cur.fetchall()

                return render_template(
                    "update_store_products.j2",
                    data=data,
                    stores=store_data,
                    products=product_data,
                )
            else:
                # number_in_stock is valid
                query = """UPDATE StoreProducts
                        SET store_id = %s, product_id = %s, number_in_stock = %s
                        WHERE store_product_id = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(
                    query, (store_id, product_id, number_in_stock, store_product_id)
                )
                mysql.connection.commit()

                return redirect("/store_products")


#   ____         __                __  ____         __        ___      __       _ __
#  / __ \_______/ /__ _______    _/_/ / __ \_______/ /__ ____/ _ \___ / /____ _(_) /__
# / /_/ / __/ _  / -_) __(_-<  _/_/  / /_/ / __/ _  / -_) __/ // / -_) __/ _ `/ / (_-<
# \____/_/  \_,_/\__/_/ /___/ /_/    \____/_/  \_,_/\__/_/ /____/\__/\__/\_,_/_/_/___/
#
@app.route("/orders", methods=["GET"])
def orders():
    """Display all Orders and Order Details in the database."""

    if request.method == "GET":
        # Display Order data.
        query = """SELECT
                order_id AS 'ID',
                order_date AS 'Date',
                Customers.customer_name AS 'Customer',
                Stores.store_number AS 'Store Number',
                order_notes AS 'Notes'
                FROM Orders
                LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id
                LEFT JOIN Stores ON Stores.store_id = Orders.store_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        order_data = cur.fetchall()

        # Display OrderDetails data.
        query2 = """SELECT
                 order_detail_id AS 'ID',
                 order_id AS 'Order ID',
                 Products.product_description AS 'Product',
                 order_quantity AS 'Quantity',
                 line_total AS 'Line Total'
                 FROM OrderDetails
                 INNER JOIN Products
                 ON Products.product_id = OrderDetails.product_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query2)
        order_detail_data = cur.fetchall()

        return render_template(
            "orders.j2", order_data=order_data, order_detail_data=order_detail_data
        )


@app.route("/add_orders", methods=["GET", "POST"])
def add_orders():
    """Add an Order to the database."""

    # User presses 'Add New Order' button on orders page.
    if request.method == "GET":
        # Customer ID/Name data for dropdown.
        query = "SELECT customer_id, customer_name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        customer_data = cur.fetchall()

        # Store ID/Number data for dropdown.
        query2 = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        store_data = cur.fetchall()

        return render_template(
            "add_orders.j2", customers=customer_data, stores=store_data
        )

    if request.method == "POST":
        # User presses 'Add Order' button.
        if request.form.get("Add_Order"):
            order_date = request.form["order_date"]
            customer_id = request.form["customer_name"]
            store_id = request.form["store_number"]
            order_notes = request.form["order_notes"]

            # Insert new Order into database.
            # account for null customer_id
            if customer_id == "NULL":
                query = "INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_date, NULL, store_id, order_notes))
                mysql.connection.commit()
            # no null inputs
            else:
                query = "INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_date, customer_id, store_id, order_notes))
                mysql.connection.commit()

            return redirect("/orders")


@app.route("/add_order_details", methods=["GET", "POST"])
def add_order_details():
    """Add an OrderDetail to an Order."""

    # User presses 'Add New Order Detail' button on orders page.
    if request.method == "GET":
        # Order ID data for dropdown if customer is not NULL.
        query = """SELECT
                order_id,
                CONCAT(order_id, ' | ', order_date, ' | ', Customers.customer_name, ' | ', Stores.store_number) AS 'Order'
                FROM Orders
                INNER JOIN Customers ON Customers.customer_id = Orders.customer_id
                INNER JOIN Stores ON Stores.store_id = Orders.store_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        order_data = cur.fetchall()

        # Order ID data for dropdown if customer is NULL.
        query2 = """SELECT
                 order_id,
                 CONCAT(order_id, ' | ', order_date, ' | ', 'None', ' | ', Stores.store_number) AS 'Order'
                 FROM Orders
                 INNER JOIN Stores ON Stores.store_id = Orders.store_id
                 WHERE Orders.customer_id is NULL;"""
        cur = mysql.connection.cursor()
        cur.execute(query2)
        null_order_data = cur.fetchall()

        # Product ID/Description data for dropdown.
        query3 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()

        # User presses 'Add New Order Detail' button.
        return render_template(
            "add_order_details.j2",
            orders=order_data,
            products=product_data,
            null_orders=null_order_data,
        )

    if request.method == "POST":
        # User presses 'Add Order Detail' button.
        if request.form.get("Add_Order_Detail"):
            order_id = request.form["order_id"]
            product_id = request.form["product_description"]
            order_quantity = request.form["order_quantity"]
            line_total = request.form["line_total"]

            # checks if order_quantity or line_total are not valid
            if int(order_quantity) < 0 or float(line_total) < 0:
                if int(order_quantity) < 0 and float(line_total) < 0:
                    flash("Quantity and Line Total cannot be less than 0.")
                elif int(order_quantity) < 0:
                    flash("Quantity cannot be less than 0.")
                elif float(line_total) < 0:
                    flash("Line Total cannot be less than 0.")

                # Order ID data for dropdown if customer is not NULL.
                query = """SELECT
                        order_id,
                        CONCAT(order_id, ' | ', order_date, ' | ', Customers.customer_name, ' | ', Stores.store_number) AS 'Order'
                        FROM Orders
                        INNER JOIN Customers ON Customers.customer_id = Orders.customer_id
                        INNER JOIN Stores ON Stores.store_id = Orders.store_id;"""
                cur = mysql.connection.cursor()
                cur.execute(query)
                order_data = cur.fetchall()

                # Order ID data for dropdown if customer is NULL.
                query2 = """SELECT
                        order_id,
                        CONCAT(order_id, ' | ', order_date, ' | ', 'None', ' | ', Stores.store_number) AS 'Order'
                        FROM Orders
                        INNER JOIN Stores ON Stores.store_id = Orders.store_id
                        WHERE Orders.customer_id is NULL;"""
                cur = mysql.connection.cursor()
                cur.execute(query2)
                null_order_data = cur.fetchall()

                # Product ID/Description data for dropdown.
                query3 = "SELECT product_id, product_description FROM Products;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                product_data = cur.fetchall()

                return render_template(
                    "add_order_details.j2",
                    orders=order_data,
                    products=product_data,
                    null_orders=null_order_data,
                )

            # handles duplicate entries of unique combination of order_id and product_id
            try:
                # Insert new OrderDetail into database.
                query = "INSERT INTO OrderDetails (order_id, product_id, order_quantity, line_total) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_id, product_id, order_quantity, line_total))
                mysql.connection.commit()

                return redirect("/orders")
            except:
                flash("Duplicate entries of Order ID and Product not allowed.")
                
                # Order ID data for dropdown if customer is not NULL.
                query = """SELECT
                        order_id,
                        CONCAT(order_id, ' | ', order_date, ' | ', Customers.customer_name, ' | ', Stores.store_number) AS 'Order'
                        FROM Orders
                        INNER JOIN Customers ON Customers.customer_id = Orders.customer_id
                        INNER JOIN Stores ON Stores.store_id = Orders.store_id;"""
                cur = mysql.connection.cursor()
                cur.execute(query)
                order_data = cur.fetchall()

                # Order ID data for dropdown if customer is NULL.
                query2 = """SELECT
                        order_id,
                        CONCAT(order_id, ' | ', order_date, ' | ', 'None', ' | ', Stores.store_number) AS 'Order'
                        FROM Orders
                        INNER JOIN Stores ON Stores.store_id = Orders.store_id
                        WHERE Orders.customer_id is NULL;"""
                cur = mysql.connection.cursor()
                cur.execute(query2)
                null_order_data = cur.fetchall()

                # Product ID/Description data for dropdown.
                query3 = "SELECT product_id, product_description FROM Products;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                product_data = cur.fetchall()

                return render_template(
                    "add_order_details.j2",
                    orders=order_data,
                    products=product_data,
                    null_orders=null_order_data,
                )


@app.route("/delete_orders/<int:order_id>", methods=["GET", "POST"])
def delete_orders(order_id):
    """Delete an Order and its OrderDetails from the database."""

    # User presses 'Delete Order' icon on orders page.
    if request.method == "GET":
        # Display Order data to be deleted.
        query = """SELECT
                order_id AS 'ID',
                order_date AS 'Date',
                Customers.customer_name AS 'Customer',
                Stores.store_number AS 'Store Number',
                order_notes AS 'Notes'
                FROM Orders
                LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id
                LEFT JOIN Stores ON Stores.store_id = Orders.store_id
                WHERE order_id = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (order_id,))
        data = cur.fetchall()

        return render_template("delete_orders.j2", data=data)

    if request.method == "POST":
        # User presses 'Delete Order' button.
        if request.form.get("Delete_Order"):
            query = "DELETE FROM Orders WHERE order_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id,))
            mysql.connection.commit()

            return redirect("/orders")


# Listener
if __name__ == "__main__":
    app.run(port=PORT, debug=True)