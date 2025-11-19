from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .database import engine, Base
from sqlalchemy import text
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Whatsapp Product Review Collector")

@app.get("/")
def read_root():
    return {"Message": "Success"}

    
# test endpoint to verify db connection
@app.post("/posts")
def create_post(payload: dict, db: Session = Depends(get_db)):
    
    result = db.execute(text("SELECT 1")).scalar()
    return {"ok": True, "db_check": result, "payload": payload}
