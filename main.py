from fastapi import FastAPI, HTTPException
from hashlib import sha512
from typing import Optional
from datetime import date, timedelta
from pydantic import BaseModel


class PatientIn(BaseModel):
    name: str
    surname: str


class PatientOut(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


app = FastAPI()
app.counter = 0


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


@app.get('/auth', status_code=204)
def authentication(password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash:
        raise HTTPException(status_code=401)
    password = password.encode()
    if sha512(password).hexdigest() != password_hash:
        raise HTTPException(status_code=401)


@app.post('/register', status_code=201)
def register_view(patient: PatientIn):
    app.counter += 1
    today = date.today()
    register_date = str(today)
    days = len(set(patient.name + patient.surname))
    vaccination_date = str(today + timedelta(days=days))
    return PatientOut(id=app.counter,
                      name=patient.name,
                      surname=patient.surname,
                      register_date=register_date,
                      vaccination_date=vaccination_date)
