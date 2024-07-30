from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from random import choice
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

html = """<!DOCTYPE html>
<html>
    <head>
        <title>TestFormData</title>
    </head>
    <body>
        <script>

        </script>
    </body>
</html>
    """

@app.get("/")
async def get():
    return HTMLResponse(html)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



""" ************************饭菜操作************************ """
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


@app.post("/dishget")
async def search_dish(input: schemas.DishSearchItem, db: Session = Depends(get_db)):
    return crud.search_dish(db, input.name)


@app.get("/random/{canteen}")
async def random_get_dish(canteen: schemas.Canteen, db: Session = Depends(get_db)):
    dishes = crud.get_canteen_all_dishes(db, canteen, 6)
    dish = choice(dishes)
    return dish
""" ************************饭菜操作************************ """


""" ********************轮播图与上新宣传******************** """
@app.post("/newadd")
async def add_new_dishes(dishes: List[schemas.DishItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.add_new_dishes(db, dish)
    return {"detail": "Add Success"}


@app.delete("/newdel")
async def delete_new_dishes(dishes: List[schemas.DishDelItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.delete_new_dishes(db, dish)
    return {"detail": "Delete Success"}
""" ********************轮播图与上新宣传******************** """



