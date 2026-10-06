from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "retail-management-demo"

# =========================
# MYSQL CONFIGURATION
# =========================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Krish@280606"
DB_NAME = "retailmanagement"


def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def query_db(sql, params=None, fetch=True):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/")
def dashboard():
    counts = {}
    for table, key in [
        ("products", "products"),
        ("customers", "customers"),
        ("suppliers", "suppliers"),
        ("orders", "orders"),
    ]:
        try:
            row = query_db(f"SELECT COUNT(*) AS count FROM `{table}`")[0]
            counts[key] = row["count"]
        except Exception:
            counts[key] = 0

    try:
        recent_orders = query_db("""
            SELECT o.OrderID, o.OrderDate, o.TotalAmount,
                   o.PaymentStatus, c.firstname, c.lastname
            FROM orders o
            LEFT JOIN customers c ON o.CustomerID = c.customerID
            ORDER BY o.OrderDate DESC
            LIMIT 8
        """)
    except Exception:
        recent_orders = []

    return render_template("dashboard.html", counts=counts, recent_orders=recent_orders)


# =========================
# PRODUCTS
# =========================
@app.route("/products")
def products():
    rows = query_db("""
        SELECT p.*, s.suppliername
        FROM products p
        LEFT JOIN suppliers s ON p.supplierID = s.supplierID
        ORDER BY p.ProductID
    """)
    suppliers = query_db("SELECT supplierID, suppliername FROM suppliers ORDER BY suppliername")
    return render_template("products.html", products=rows, suppliers=suppliers)


@app.post("/products/add")
def add_product():
    try:
        query_db("""
            INSERT INTO products
            (ProductName, Category, Description, Price, CostPrice,
             supplierID, StockQuantity, ReorderLevel, LastRestockDate)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["ProductName"],
            request.form["Category"],
            request.form["Description"],
            request.form["Price"],
            request.form["CostPrice"],
            request.form["supplierID"],
            request.form["StockQuantity"],
            request.form["ReorderLevel"],
            request.form["LastRestockDate"] or None
        ), fetch=False)
        flash("Product added successfully.", "success")
    except Error as e:
        flash(f"Could not add product: {e}", "error")
    return redirect(url_for("products"))


@app.post("/products/update/<int:product_id>")
def update_product(product_id):
    try:
        query_db("""
            UPDATE products
            SET ProductName=%s, Category=%s, Description=%s,
                Price=%s, CostPrice=%s, supplierID=%s,
                StockQuantity=%s, ReorderLevel=%s, LastRestockDate=%s
            WHERE ProductID=%s
        """, (
            request.form["ProductName"],
            request.form["Category"],
            request.form["Description"],
            request.form["Price"],
            request.form["CostPrice"],
            request.form["supplierID"],
            request.form["StockQuantity"],
            request.form["ReorderLevel"],
            request.form["LastRestockDate"] or None,
            product_id
        ), fetch=False)
        flash("Product updated successfully.", "success")
    except Error as e:
        flash(f"Could not update product: {e}", "error")
    return redirect(url_for("products"))


@app.post("/products/delete/<int:product_id>")
def delete_product(product_id):
    try:
        query_db("DELETE FROM products WHERE ProductID=%s", (product_id,), fetch=False)
        flash("Product deleted successfully.", "success")
    except Error as e:
        flash(f"Could not delete product. It may be referenced by an order/review: {e}", "error")
    return redirect(url_for("products"))


# =========================
# CUSTOMERS
# =========================
@app.route("/customers")
def customers():
    rows = query_db("SELECT * FROM customers ORDER BY customerID")
    return render_template("customers.html", customers=rows)


@app.post("/customers/add")
def add_customer():
    try:
        query_db("""
            INSERT INTO customers (firstname, lastname, dateofbirth, address)
            VALUES (%s,%s,%s,%s)
        """, (
            request.form["firstname"],
            request.form["lastname"],
            request.form["dateofbirth"] or None,
            request.form["address"]
        ), fetch=False)
        flash("Customer added successfully.", "success")
    except Error as e:
        flash(f"Could not add customer: {e}", "error")
    return redirect(url_for("customers"))


@app.post("/customers/update/<int:customer_id>")
def update_customer(customer_id):
    try:
        query_db("""
            UPDATE customers
            SET firstname=%s, lastname=%s, dateofbirth=%s, address=%s
            WHERE customerID=%s
        """, (
            request.form["firstname"],
            request.form["lastname"],
            request.form["dateofbirth"] or None,
            request.form["address"],
            customer_id
        ), fetch=False)
        flash("Customer updated successfully.", "success")
    except Error as e:
        flash(f"Could not update customer: {e}", "error")
    return redirect(url_for("customers"))


@app.post("/customers/delete/<int:customer_id>")
def delete_customer(customer_id):
    try:
        query_db("DELETE FROM customers WHERE customerID=%s", (customer_id,), fetch=False)
        flash("Customer deleted successfully.", "success")
    except Error as e:
        flash(f"Could not delete customer. It may have orders/reviews: {e}", "error")
    return redirect(url_for("customers"))


# =========================
# SUPPLIERS
# =========================
@app.route("/suppliers")
def suppliers():
    rows = query_db("SELECT * FROM suppliers ORDER BY supplierID")
    return render_template("suppliers.html", suppliers=rows)


@app.post("/suppliers/add")
def add_supplier():
    try:
        query_db("""
            INSERT INTO suppliers
            (suppliername, contactname, address, phone, email, lastdeliverydate)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            request.form["suppliername"],
            request.form["contactname"],
            request.form["address"],
            request.form["phone"],
            request.form["email"],
            request.form["lastdeliverydate"] or None
        ), fetch=False)
        flash("Supplier added successfully.", "success")
    except Error as e:
        flash(f"Could not add supplier: {e}", "error")
    return redirect(url_for("suppliers"))


@app.post("/suppliers/update/<int:supplier_id>")
def update_supplier(supplier_id):
    try:
        query_db("""
            UPDATE suppliers
            SET suppliername=%s, contactname=%s, address=%s,
                phone=%s, email=%s, lastdeliverydate=%s
            WHERE supplierID=%s
        """, (
            request.form["suppliername"],
            request.form["contactname"],
            request.form["address"],
            request.form["phone"],
            request.form["email"],
            request.form["lastdeliverydate"] or None,
            supplier_id
        ), fetch=False)
        flash("Supplier updated successfully.", "success")
    except Error as e:
        flash(f"Could not update supplier: {e}", "error")
    return redirect(url_for("suppliers"))


@app.post("/suppliers/delete/<int:supplier_id>")
def delete_supplier(supplier_id):
    try:
        query_db("DELETE FROM suppliers WHERE supplierID=%s", (supplier_id,), fetch=False)
        flash("Supplier deleted successfully.", "success")
    except Error as e:
        flash(f"Could not delete supplier. Products may reference it: {e}", "error")
    return redirect(url_for("suppliers"))


# =========================
# ORDERS / READ VIEW
# =========================
@app.route("/orders")
def orders():
    rows = query_db("""
        SELECT o.*, c.firstname, c.lastname
        FROM orders o
        LEFT JOIN customers c ON o.CustomerID = c.customerID
        ORDER BY o.OrderDate DESC
    """)
    return render_template("orders.html", orders=rows)


@app.route("/orderdetails")
def orderdetails():
    rows = query_db("""
        SELECT od.OrderDetailID, od.OrderID, od.ProductID,
               p.ProductName, od.Quantity, od.UnitPrice, od.LineTotal
        FROM orderdetails od
        LEFT JOIN products p ON od.ProductID = p.ProductID
        ORDER BY od.OrderDetailID DESC
    """)
    return render_template("orderdetails.html", orderdetails=rows)


@app.route("/reviews")
def reviews():
    rows = query_db("""
        SELECT r.*, p.ProductName,
               CONCAT(c.firstname, ' ', c.lastname) AS CustomerName
        FROM reviews r
        LEFT JOIN products p ON r.ProductID = p.ProductID
        LEFT JOIN customers c ON r.CustomerID = c.customerID
        ORDER BY r.ReviewDate DESC
    """)
    return render_template("reviews.html", reviews=rows)


@app.route("/inventorylog")
def inventorylog():
    rows = query_db("""
        SELECT il.*, p.ProductName
        FROM inventorylog il
        LEFT JOIN products p ON il.ProductID = p.ProductID
        ORDER BY il.LogDate DESC
    """)
    return render_template("inventorylog.html", inventorylog=rows)


if __name__ == "__main__":
    app.run(debug=True)
