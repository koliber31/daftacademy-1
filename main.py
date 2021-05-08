import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    name: str


app = FastAPI()


def check_category_id(category_id):
    app.db_connection.row_factory = sqlite3.Row
    id_exist = app.db_connection.execute(
        "SELECT 1 FROM Categories WHERE CategoryId = ?", (category_id,)
    ).fetchone()
    if not id_exist:
        raise HTTPException(status_code=404, detail=f"Category id {category_id} doesn't exist")


def new_remove(text):
    new = ''
    for word in text.split(' '):
        if word.lower() == 'new':
            continue
        elif word.lower().startswith('new'):
            new += word[3:] + ' '
        else:
            new += word + ' '
    return new.strip()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db", check_same_thread=False)
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def categories_list():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CategoryId AS id, CategoryName AS name FROM Categories").fetchall()
    return {
        'categories': data
    }


@app.post("/categories", status_code=201)
async def category_add(category: Category):
    cursor = app.db_connection.execute(
        "INSERT INTO Categories (CategoryName) VALUES (?)", (category.name,)
    )
    app.db_connection.commit()
    new_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    category = app.db_connection.execute(
        "SELECT CategoryId AS id, CategoryName AS name FROM categories WHERE CategoryId = ?", (new_id,)).fetchone()
    return category


@app.put("/categories/{category_id}")
async def category_update(category: Category, category_id: int):
    check_category_id(category_id)
    category.name = new_remove(category.name)
    cursor = app.db_connection.execute(
        "UPDATE Categories SET CategoryName = ? WHERE CategoryId = ?", (category.name, category_id)
    )
    app.db_connection.commit()
    category = app.db_connection.execute(
        "SELECT CategoryId AS id, CategoryName AS name FROM categories WHERE CategoryId = ?",
        (category_id,)).fetchone()
    return category


@app.delete("/categories/{category_id}")
async def category_delete(category_id: int):
    check_category_id(category_id)
    cursor = app.db_connection.execute(
        "DELETE FROM Categories WHERE CategoryId = ?", (category_id,)
    )
    app.db_connection.commit()
    return {"deleted": cursor.rowcount}


@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        """SELECT CustomerId AS id, CompanyName AS name,
          Address || ' ' || PostalCode || ' ' || City || ' ' || Country AS full_address FROM customers""").fetchall()
    return {
        'customers': data
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
