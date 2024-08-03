from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
from . import models, schemas
from typing import List



def get_all_dishes(db: Session, canteen: int, floor: int | None = None, skip: int = 0, limit: int = 200):
    if floor:
        return db.query(models.Dish).filter(models.Dish.canteen == canteen) \
            .filter(models.Dish.floor == floor) \
            .offset(skip).limit(limit).all()
    else:
        return db.query(models.Dish).filter(models.Dish.canteen == canteen) \
            .offset(skip).limit(limit).all()



def add_dishes(db: Session, dish: schemas.DishItem):    
    db_exist_dish = db.query(models.Dish).filter(models.Dish.canteen == dish.canteen,
                                                models.Dish.floor == dish.floor,
                                                models.Dish.window == dish.window,
                                                models.Dish.name == dish.name,
                                                models.Dish.measure == dish.measure).first()  
    if db_exist_dish is None: 
        # with open(dish.image, 'rb') as f:
        #     image_data = f.read()
        db_dish = models.Dish(canteen=dish.canteen, 
                        floor=dish.floor,
                        window=dish.window,
                        name=dish.name,
                        price=dish.price,
                        measure=dish.measure,
                        average_vote=dish.average_vote,
                        image=dish.image)
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
    else:
        raise HTTPException(status_code=400, detail="Try to add existed dishes")


def add_dishes_by_excel(db: Session, dish: dict):
    db_exist_dish = db.query(models.Dish).filter(models.Dish.canteen == dish["canteen"],
                                                models.Dish.floor == dish["floor"],
                                                models.Dish.window == dish["window"],
                                                models.Dish.name == dish["name"],
                                                models.Dish.measure == dish["measure"]).first()  
    if db_exist_dish is None: 
        db_dish = models.Dish(canteen=dish["canteen"],
                                floor=dish["floor"], window=dish["window"],
                                name=dish["name"], measure=dish["measure"],
                                price=dish["price"], image=dish["image"],
                                average_vote=dish["average_vote"])
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
    else:
        raise HTTPException(status_code=400, detail="Try to add existed dishes")



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


def modify_dish(db: Session, dish: schemas.DishPutItem):
    db_exist_dish = db.query(models.Dish).filter(models.Dish.canteen == dish.canteen,
                                                models.Dish.floor == dish.floor,
                                                models.Dish.window == dish.window,
                                                models.Dish.name == dish.name,
                                                models.Dish.measure == dish.measure).first()
    if db_exist_dish is None: 
        raise HTTPException(status_code=400, detail="Try to modify absent dishes")
    else:
        db_exist_dish.canteen = dish.canteen
        db_exist_dish.floor = dish.floor
        db_exist_dish.window = dish.window
        db_exist_dish.name = dish.name        
        db_exist_dish.measure = dish.measure
        db_exist_dish.price = dish.price
        db_exist_dish.image = dish.image
        db.commit()
        


def search_dish(db: Session, name: str, skip: int = 0, limit: int = 200):
    return db.query(models.Dish) \
            .filter(models.Dish.name.contains(name)) \
            .offset(skip).limit(limit).all()


def add_carousel(db: Session, carousel: str):
    db_exist_image = db.query(models.Carousel).filter(models.Carousel.image == carousel).first()
    if db_exist_image is None:
        db_image = models.Carousel(image=carousel)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
    else:
        raise HTTPException(status_code=400, detail="Try to add existed carousels")
    
    
def delete_carousel(db: Session, carousel: str):
    db_image = db.query(models.Carousel).filter(models.Carousel.image == carousel).first()
    if db_image is None:
        raise HTTPException(status_code=400, detail="Try to delete absent carousels")   
    else:
        db.delete(db_image)
        db.commit()
        
        
def add_new_dish(db: Session, new_dish_id: int):
    db_exist_new_dish = db.query(models.NewDish).filter(models.NewDish.dish_id == new_dish_id).first()
    if db_exist_new_dish is None:
        db_new_dish = models.NewDish(dish_id=new_dish_id)
        db.add(db_new_dish)
        db.commit()
        db.refresh(db_new_dish)
    else:
        raise HTTPException(status_code=400, detail="Try to add existed new dishes")


def delete_new_dish(db: Session, new_dish_id: int):
    db_new_dish = db.query(models.NewDish).filter(models.NewDish.dish_id == new_dish_id).first()
    if db_new_dish is None:
        raise HTTPException(status_code=400, detail="Try to delete absent new dishes")
    else:
        db.delete(db_new_dish)
        db.commit()
