from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/dish/{canteen}/{floor}")
async def get_current_canteen_dishes(canteen: schemas.Canteen, floor: int, db: Session = Depends(get_db)):
    if canteen == schemas.Canteen.xinyuan:
        return crud.get_canteen_all_dishes(db, "欣园", floor)
    elif canteen == schemas.Canteen.yueyuan:
        return crud.get_canteen_all_dishes(db, "悦园", floor)


@app.post("/dishadd")
async def add_dishes(dishes: List[schemas.DishItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.add_dishes(db, dish)
    return {"detail": "Add Success"}


@app.delete("/dishdel")
async def delete_dishes(dishes: List[schemas.DishDelItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.delete_dishes(db, dish)
    return {"detail": "Delete Success"}


@app.put("/dishmod")
async def modify_dishes(dishes: List[schemas.DishItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.modify_dishes(db, dish)
    return {"detail": "Modify Success"}



# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items