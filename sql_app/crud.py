from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from typing import List

def get_canteen_all_dishes(db: Session, canteen: str, floor: int, skip: int = 0, limit: int = 200):
    return db.query(models.Dish).filter(models.Dish.canteen == canteen) \
            .filter(models.Dish.floor == floor) \
            .offset(skip).limit(limit).all()


def add_dishes(db: Session, dish: schemas.DishItem):    
    db_exist_dish = db.query(models.Dish).filter(models.Dish.canteen == dish.canteen,
                                                models.Dish.floor == dish.floor,
                                                models.Dish.window == dish.window).first()  
    if db_exist_dish is None: 
        db_dish = models.Dish(canteen=dish.canteen, 
                        floor=dish.floor,
                        window=dish.window,
                        name=dish.name,
                        price=dish.price,
                        measure=dish.measure)
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
    else:
        raise HTTPException(status_code=400, detail="Try to add dish in existed window")


def delete_dishes(db: Session, dish: schemas.DishDelItem):
    db_dish = db.query(models.Dish).filter(models.Dish.name == dish.name,
                                        models.Dish.canteen == dish.canteen,
                                        models.Dish.floor == dish.floor,
                                        models.Dish.window == dish.window).first()
    if db_dish is None:
        raise HTTPException(status_code=400, detail="Try to delete absent dishes")   
    else:
        db.delete(db_dish)
        db.commit()


def modify_dishes(db: Session, dish: schemas.DishItem):
    db_exist_dish = db.query(models.Dish).filter(models.Dish.canteen == dish.canteen,
                                                models.Dish.floor == dish.floor,
                                                models.Dish.window == dish.window).first()
    if db_exist_dish is None: 
        raise HTTPException(status_code=400, detail="Try to modify absent dishes")
    else:
        db_exist_dish.name = dish.name
        db_exist_dish.price = dish.price
        db_exist_dish.measure = dish.measure
        db.commit()
        

def search_dish(db: Session, name: str, skip: int = 0, limit: int = 200) -> bool:
    return db.query(models.Dish) \
            .filter(models.Dish.name.contains(name)) \
            .offset(skip).limit(limit).all()




# def update_book_by_id(db:Session, bookId:int, book:schemas.BooksBase):
#     db_book = db.query(models.Books).filter(models.Books.id == bookId).one_or_none()
#     if db_book is None:
#         return None

#     # Update model class variable from requested fields 
#     for var, value in vars(book).items():
#         setattr(db_book, var, value) if value else None
#     db.commit()
#     db.refresh(db_book)
#     return db_book


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item