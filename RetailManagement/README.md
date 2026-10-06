# Retail Management System

Flask + MySQL UI for the existing `retailmanagement` database.

## Setup

1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Open `app.py`.
5. Replace:

```python
DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
```

with your local MySQL password. Do not commit your real password to GitHub.

6. Run:

```bash
python app.py
```

7. Open:

`http://127.0.0.1:5000`

## Current database tables

- customers
- products
- suppliers
- orders
- orderdetails
- reviews
- inventorylog

The application is designed around the existing database and does not create or replace the database.
