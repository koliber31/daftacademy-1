import sqlite3

from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    name: str


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


@app.post("/categories", status_code=201)
async def categories(category: Category):
    cursor = app.db_connection.execute(
        "INSERT INTO Categories (CategoryName) VALUES (?)", (category.name,)
    )
    app.db_connection.commit()
    new_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    category = app.db_connection.execute(
        "SELECT CategoryId AS id, CategoryName AS name FROM categories WHERE CategoryId = ?", (new_id,)).fetchone()
    return category


@app.api_route(path="/categories/{id}", methods=['PUT', 'DELETE'], status_code=200)
async def categories(request: Request, category_id: int, category: Optional[Category] = None):
    app.db_connection.row_factory = sqlite3.Row
    id_exist = app.db_connection.execute(
        "SELECT 1 FROM Categories WHERE CategoryId = ?", (category_id,)
    ).fetchone()
    if not id_exist:
        raise HTTPException(status_code=404, detail=f"Category id {category_id} doesn't exist")

    request_method = request.method

    if request_method == 'PUT':
        cursor = app.db_connection.execute(
            "UPDATE Categories SET CategoryName = ? WHERE CategoryId = ?", (category.name, category_id)
        )
        app.db_connection.commit()
        category = app.db_connection.execute(
            "SELECT CategoryId AS id, CategoryName AS name FROM categories WHERE CategoryId = ?",
            (category_id,)).fetchone()
        return category

    elif request_method == 'DELETE':
        cursor = app.db_connection.execute(
            "DELETE FROM Categories WHERE CategoryId = ?", (category_id,)
        )
        app.db_connection.commit()
        return {'deleted': 1}


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


@app.get("/products/{product_id}/orders")
async def products(product_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("""
        SELECT o.OrderId AS id, c.CompanyName AS customer, od.Quantity AS quantity,
        ROUND((od.UnitPrice * od.Quantity) - (od.Discount * (od.UnitPrice * od.Quantity)), 2) AS total_price
        FROM Orders AS o JOIN Customers AS c USING (CustomerID)
        JOIN 'Order Details' AS od USING (OrderId)
        WHERE od.ProductId= ?""", (product_id,)).fetchall()

    if data:
        return {'orders': data}
    else:
        raise HTTPException(status_code=404, detail=f"Order_id {product_id} doesn't exist")


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
                                     FROM products JOIN categories USING (CategoryId)
                                     JOIN suppliers USING(SupplierId)
                                     ''').fetchall()

    return {'products_extended': data}
