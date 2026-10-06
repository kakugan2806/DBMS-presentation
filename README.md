# Retail Inventory and Sales Management System

**Student Name:** Krish Chhotoo Ghadge  
**Roll Number:** 25WU0102132  
**Course:** Database Management Systems (DBMS)  
**Academic Year:** 2026–2027  

## Project Description

The Retail Inventory and Sales Management System is a database-driven application developed to manage products, suppliers, customers, orders, order details, reviews, and inventory records. The system uses MySQL as the database and Flask as the backend framework, with a web-based frontend for interacting with the database.

The project demonstrates relational database design, SQL operations, database connectivity, normalization, and CRUD operations through a user interface.

## Technologies Used

**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, Flask  
**Database:** MySQL  
**Database Connectivity:** MySQL Connector/Python  
**Development Environment:** Visual Studio Code  
**Database Management:** MySQL Workbench  

## Database Tables

The system consists of seven main tables:

- Customers
- Products
- Suppliers
- Orders
- Order Details
- Reviews
- Inventory Log

These tables are connected using primary keys and foreign keys to maintain relationships and data integrity.

## Main Features

The system provides a dashboard for accessing different modules of the retail management system.

The Product Management module allows users to add, view, update, and delete products while maintaining information such as product name, category, price, cost price, supplier, stock quantity, reorder level, and restock date.

The Customer Management module stores and manages customer information.

The Supplier Management module maintains supplier details including contact information and delivery information.

The Order Management module stores order information such as customer, order date, total amount, payment status, payment method, and tracking number.

The Order Details module connects orders with the products purchased.

The Reviews module stores customer ratings and comments for products.

The Inventory Log module records stock adjustments along with the reason and date of the adjustment.

## Database Connectivity

The Flask backend connects the web application to the MySQL `retailmanagement` database. User actions performed through the frontend are processed by Flask routes, which execute SQL queries against the database.

The application supports database operations including insertion, retrieval, updating, and deletion of records.

## Project Structure

The repository contains the project presentations, project report, source code, SQL files, screenshots, and documentation.

The source code contains the Flask backend along with the HTML templates, CSS, and JavaScript files used to build the frontend.

## Project Objective

The main objective of this project is to demonstrate the design and implementation of a practical relational database system for a retail environment. The project shows how database entities can be organized into related tables and accessed through a functional web interface.

## Future Enhancements

Future improvements could include user authentication, role-based access control, automated low-stock notifications, sales analytics, advanced reporting, automated stock deduction after orders, database backups, and deployment to a production server.

## Author

**Krish Chhotoo Ghadge**  
**Roll No.: 25WU0102132**
