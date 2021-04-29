from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from datetime import datetime
from hashlib import sha256
from typing import Dict

user, password = '4dm1n', 'NotSoSecurePa$$'

app = FastAPI()
app.secret_key = 'The quick brown fox jumps over the lazy dog'
app.access_tokens = [sha256(f'{user}{password}{app.secret_key}'.encode()).hexdigest()]
app.store = {}

templates = Jinja2Templates(directory='templates')


@app.get("/hello")
def hello_view(request: Request):
    today = datetime.today().date()
    context = {'request': request, 'today': today}
    return templates.TemplateResponse("index.j2.html", context=context)


@app.post("/login_session")
def login_session(user: str, password: str):
    session_token = sha256(f'{user}{password}{app.secret_key}'.encode()).hexdigest()
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        response = JSONResponse()
        response.set_cookie(key="session_token", value=session_token)
        app.store['login_session'] = session_token
    return response


@app.post("/login_token")
def login_token(user: str, password: str):
    session_token = sha256(f'{user}{password}{app.secret_key}'.encode()).hexdigest()
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unauthorised")
    content = {"token": session_token}
    response = JSONResponse(content=content)
    app.store['login_token'] = session_token
    return response

