from typing import Optional
import sqlite3
from fastapi import FastAPI, Request, Response, status, HTTPException

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get('/categories')
async def func(response: Response):
    #app.db_connection.row_factory = sqlite3.Row

    categories = app.db_connection.execute("SELECT CategoryName, CategoryID FROM Categories ORDER BY CategoryID").fetchall()
    response.status_code = status.HTTP_200_OK
    return {"categories":[
         {'id': x[1] , 'name': f"{x[0]}"} for x in categories
    ]}

@app.get('/customers')
async def func(response: Response):
    customers = app.db_connection.execute("SELECT CompanyName, CustomerID, Address, PostalCode, City, Country FROM Customers ORDER BY CAST(CustomerID as INTEGER)").fetchall()
    response.status_code = status.HTTP_200_OK
    # return {"customers":[
    #      {'id': x[1] , 'name': f'{x[0]}' , 'full_address': f'{x[2]}'} for x in customers
    # ]}
    # result = {
    #     'customers': []
    # }
    # for c in customers:
    #     _id = str(c[1])
    #     name = str(c[0])
    #     Address = c[2] + ' ' if c[2] else ''
    #     PostalCode = c[3] + ' 'if c[3] else ''
    #     City = c[4] + ' ' if c[4] else ''
    #     Country= c[5] if c[5] else ''
    #     full_address = '{Address}{PostalCode}{City}{Country}'.format(Address=Address,PostalCode=PostalCode,City=City,Country=Country)
        
    #     result['customers'].append(
    #         {'id': _id, 'name': name, 'full_address': full_address}
    #     )
    # return result

    # print(f'{type([1][2])}')
    # print(f'{customers}')
    # return {"customers":[
    #     {'id': f'{x[1]}', 'name': f'{x[0]}', 'full_address': f'{x[2]}'} for x in customers
    # ]}
    number = 0
    for x in customers:
        if x[2] is None:
            print(x)
            x = list(x)
            x[2] = ''
            x = tuple(x)
            print(x)
        if x[3] is None:
            x = list(x)
            x[3] = ''
            x = tuple(x)
        if x[4] is None:
            x = list(x)
            x[4] = ''
            x = tuple(x)
        if x[5] is None:
            x = list(x)
            x[5] = ''
            x = tuple(x)
        customers[number] = x
        number += 1
    return {"customers":[
         {'id': f'{x[1]}' , 'name': f'{x[0]}' , 'full_address': f'{x[2]} {x[3]} {x[4]} {x[5]}'} for x in customers
    ]}

@app.get('/products/{id_}')
async def func(id_: int, response: Response):
    response.status_code = status.HTTP_200_OK
    number = []
    ids = app.db_connection.execute(f"SELECT ProductID FROM Products").fetchall()
    data = app.db_connection.execute(f"SELECT ProductID, ProductName FROM Products WHERE ProductID = {id_}").fetchone()
    for i in range(len(ids)):
        number.append(ids[i][0])
    if id_ not in number:
        raise HTTPException(status_code=404)
    return {'id': data[0], 'name': data[1]}

@app.get('/employees')
async def func(response: Response, limit: Optional[int] = None, offset: Optional[int] = None, order: Optional[str] = None):
    app.db_connection.row_factory = sqlite3.Row
    if order not in ['first_name', 'last_name', 'city', None]:
        raise HTTPException(status_code=400)
    if limit is None:
        if offset is None:
            if order is None:
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY EmployeeID").fetchall()
            if order == 'first_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY FirstName").fetchall()
            if order == 'last_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY LastName").fetchall() 
            if order == 'city':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY City").fetchall()   
        if offset != None:
            if order is None:
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY EmployeeID LIMIT {-1} OFFSET {offset}").fetchall()
            if order == 'first_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY FirstName LIMIT {-1} OFFSET {offset}").fetchall()
            if order == 'last_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY LastName LIMIT {-1} OFFSET {offset}").fetchall() 
            if order == 'city':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY City LIMIT {-1} OFFSET {offset}").fetchall()
    if limit != None:
        if offset is None:
            if order is None:
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY EmployeeID LIMIT {limit}").fetchall()
            if order == 'first_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY FirstName LIMIT {limit}").fetchall()
            if order == 'last_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY LastName LIMIT {limit}").fetchall() 
            if order == 'city':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY City LIMIT {limit}").fetchall()            
        if offset != None:
            if order is None:
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY EmployeeID LIMIT {limit} OFFSET {offset}").fetchall()
            if order == 'first_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY FirstName LIMIT {limit} OFFSET {offset}").fetchall()
            if order == 'last_name':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY LastName LIMIT {limit} OFFSET {offset}").fetchall() 
            if order == 'city':
                data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY City LIMIT {limit} OFFSET {offset}").fetchall()            
    
    response.status_code = status.HTTP_200_OK
    return {"employees":[
        {'id': x[0] , 'last_name': f'{x[1]}' , 'first_name': f'{x[2]}', 'city': f'{x[3]}'} for x in data
    ]}

@app.get('/products_extended')
async def func(response: Response):
    response.status_code = status.HTTP_200_OK
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''SELECT Products.ProductID, Products.ProductName, Categories.CategoryName, Suppliers.CompanyName FROM Products JOIN Categories ON Products.CategoryID = Categories.CategoryID JOIN Suppliers ON Suppliers.SupplierID = Products.SupplierID''').fetchall()
    return {"products_extended":[
        {"id": x['ProductID'], "name": f"{x['ProductName']}", "category": f"{x['CategoryName']}", "supplier": f"{x['CompanyName']}"} for x in data
    ]}

@app.get('/products/{id_}/orders')
async def func(response: Response, id_: int):
    number = []
    ids = app.db_connection.execute(f"SELECT OrderID FROM Orders").fetchall()
    for i in range(len(ids)):
        number.append(ids[i][0])
    if id_ not in number:
        raise HTTPException(status_code=404)


    response.status_code = status.HTTP_200_OK
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''SELECT Orders.OrderID, Customers.CompanyName, OrderDetails.Quantity, ROUND((OrderDetails.UnitPrice * OrderDetails.Quantity) - (OrderDetails.Discount * (OrderDetails.UnitPrice * OrderDetails.Quantity)), 2) AS total_price FROM Orders JOIN Customers ON Orders.CustomerID = Customers.CustomerID JOIN 'Order Details' AS OrderDetails ON Orders.OrderID = OrderDetails.OrderID WHERE OrderDetails.OrderID = ?''', (id_,)).fetchall()
    return {"orders":[
        {"id": x['OrderID'], "customer": f"{x['CompanyName']}", "quantity": x['Quantity'], "total_price": x['total_price']} for x in data
    ]}
