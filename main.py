import sqlite3

from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db", check_same_thread=False)
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CategoryId AS id, CategoryName AS name FROM Categories").fetchall()
    return {
        'categories': data
    }


@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CustomerId, CompanyName, Address, PostalCode, City, Country FROM customers").fetchall()
    refactored = []
    for row in data:
        keys = ['Address', 'PostalCode', 'City', 'Country']
        full_address = []
        for key in keys:
            if row[key]:
                full_address.append(row[key])

        refactored.append(
            {'id': row['CustomerId'],
             'name': row['CompanyName'],
             'full_address': ' '.join(full_address)}
        )
    return {
        'customers': refactored
    }


@app.get("/products/{product_id}")
async def products(product_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT ProductId AS id, ProductName AS name FROM products WHERE ProductId= ?", (product_id,)).fetchone()
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail='Incorrect id value')


@app.get("/employees/")
async def employees(limit: Optional[int] = None, offset: Optional[int] = None, order='id'):
    app.db_connection.row_factory = sqlite3.Row
    if order not in ['id', 'first_name', 'last_name', 'city']:
        raise HTTPException(status_code=400, detail='Wrong order parameter')
    limitation = ' '
    if limit or limit == 0:
        limitation += f'LIMIT {limit}'
        if offset or offset == 0:
            limitation += f' OFFSET {offset}'
    data = app.db_connection.execute(
        f"SELECT EmployeeId AS id, LastName AS last_name, FirstName AS first_name, City AS city FROM employees ORDER BY {order}" + limitation).fetchall()
    return {'employees': data}


@app.get("/products_extended")
def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
                                     SELECT products.ProductID AS id, products.ProductName AS name,
                                     categories.CategoryName AS category, suppliers.CompanyName AS supplier
                                     FROM products JOIN categories ON products.CategoryId = categories.CategoryId
                                     JOIN suppliers ON products.SupplierId = suppliers.SupplierId
                                     ''').fetchall()

    return {'products_extended': data}
