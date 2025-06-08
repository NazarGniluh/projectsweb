from urllib import request

import items
from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
         yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return
templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add", response_class=HTMLResponse)
def add_item(
        request: Request,
        name: str = Form(),
        description: str = Form(),
        db: Session = Depends(get_db()),
):
        item = models.Item(name=name,description=description)
        db.add(item)
        db.commit()
        return read_items(request, db)





