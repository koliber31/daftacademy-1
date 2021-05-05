import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/products")
async def products():
    cursor = app.db_connection.cursor()
    app.db_connection.row_factory = lambda cursor, x: x[0]
    products_list = cursor.execute("SELECT ProductName FROM Products").fetchall()
    return {
        "products": products_list,
    }
