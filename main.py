from fastapi import FastAPI, HTTPException
from hashlib import sha512
from typing import Optional

app = FastAPI()


@app.get("/")
def root():
    return {"message": 'Hello world!'}


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/method")
def method_id():
    return {"method": 'GET'}


@app.post("/method", status_code=201)
def method_id():
    return {"method": 'POST'}


@app.delete("/method")
def method_id():
    return {"method": 'DELETE'}


@app.put("/method")
def method_id():
    return {"method": 'PUT'}


@app.options("/method")
def method_id():
    return {"method": 'OPTIONS'}


@app.get('/auth', status_code=201)
def authentication(password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash:
        raise HTTPException(status_code=401)
    password = password.encode()
    if sha512(password).hexdigest() != password_hash:
        raise HTTPException(status_code=401)

