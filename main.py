from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_id: int
    user_email: EmailStr
    age: int = Field(default=None, gt=0)
    recommendations: list[str] = Field(default_factory=list)
    zip: str = Field(default=None, min_length=5, max_length=5)

@app.get("/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    user_model = models.Users()
    user_model.user_id = user.user_id
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    db.add(user_model)
    db.commit()

    return user

@app.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado.")

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    db.add(user_model)
    db.commit()

    return user_model

@app.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado.")
    return user_model

@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado."
        )

    db.query(models.Users).filter(models.Users.user_id == user_id).delete()
    db.commit()