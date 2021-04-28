from fastapi import FastAPI, Response, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/hello")
def hello_view(request: Request):
    today = datetime.today().date()
    context = {'request': request, 'today': today}
    return templates.TemplateResponse("index.j2.html", context=context)
