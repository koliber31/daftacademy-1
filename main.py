from fastapi import FastAPI

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
