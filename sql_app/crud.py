from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from typing import List

def get_canteen_all_dishes(db: Session, canteen: str, floor: int, skip: int = 0, limit: int = 200):
    if floor <= 5:
        return db.query(models.Dish).filter(models.Dish.canteen == canteen) \
            .filter(models.Dish.floor == floor) \
            .offset(skip).limit(limit).all()
    else:
        return db.query(models.Dish).filter(models.Dish.canteen == canteen) \
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





def add_new_dishes(db: Session, dish: schemas.DishItem):    
    db_exist_dish = db.query(models.NewDish).filter(models.NewDish.canteen == dish.canteen,
                                                models.NewDish.floor == dish.floor,
                                                models.NewDish.window == dish.window).first()  
    if db_exist_dish is None: 
        db_dish = models.NewDish(canteen=dish.canteen, 
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


def delete_new_dishes(db: Session, dish: schemas.DishDelItem):
    db_dish = db.query(models.NewDish).filter(models.NewDish.name == dish.name,
                                        models.NewDish.canteen == dish.canteen,
                                        models.NewDish.floor == dish.floor,
                                        models.NewDish.window == dish.window).first()
    if db_dish is None:
        raise HTTPException(status_code=400, detail="Try to delete absent dishes")   
    else:
        db.delete(db_dish)
        db.commit()