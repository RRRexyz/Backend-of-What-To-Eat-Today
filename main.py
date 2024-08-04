from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from random import choice
from typing import List
# from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")


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

# @app.get("/")
# async def get():
#     return HTMLResponse(html)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




""" ************************饭菜操作************************ """
@app.get("/dish/{canteen}/{floor}")
async def get_current_canteen_dishes(canteen: int, floor: int, db: Session = Depends(get_db)):
    return crud.get_all_dishes(db, canteen, floor)


@app.post("/dish")
async def add_dishes(dishes: List[schemas.DishItem], db: Session = Depends(get_db)):
    for dish in dishes:    
        crud.add_dishes(db, dish)
    return {"detail": "Add Success"}


@app.delete("/dish")
async def delete_dishes(dishes: List[schemas.DishDelItem], db: Session = Depends(get_db)):
    for dish in dishes:
        crud.delete_dishes(db, dish)
    return {"detail": "Delete Success"}


@app.post("/dish/excel")
async def upload_excel_import_dishes(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.filename[-4:] == "xlsx":
        data = pd.read_excel(file.file)
        data_dict = data.to_dict(orient='records')
    elif file.filename[-3:] == "csv":
        data = pd.read_csv(file.file, encoding="gbk")
        data_dict = data.to_dict(orient='records')
        
    if data_dict == []:
        return {"detail": "No data to add"}
    
    data_set = set(data_dict[0].keys())
    if data_set != {'window', 'price', 'canteen', 'image', 'floor', 'name', 'id', 'measure', 'average_vote'}:
        return {"detail": "Data format is wrong"}

    for dish in data_dict:
        crud.add_dishes_by_excel(db, dish)
    return {"detail": "Add Success"}


@app.put("/dish")
async def modify_dish(dish: schemas.DishPutItem, db: Session = Depends(get_db)):
    crud.modify_dish(db, dish)
    return {"detail": "Modify Success"}

    
@app.get("/dish/{input}")
async def search_dish(input: str, db: Session = Depends(get_db)):
    return crud.search_dish(db, input)
    
    
@app.get("/random/{canteen}")
async def random_get_dish(canteen: int, db: Session = Depends(get_db)):
    dishes = crud.get_all_dishes(db, canteen)
    dish = choice(dishes)
    return dish    
    
    
# @app.post("/pictures")
# async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     with open(f"pictures/{file.filename}", 'wb') as f:
#         #一次读取1024字节，循环读取写入
#         for chunk in iter(lambda: file.file.read(1024), b''):
#             f.write(chunk)
#     return {"filename": file.filename}

""" ************************饭菜操作************************ """


# """ ********************轮播图与上新宣传******************** """
@app.post("/carousel")
async def add_carousels(carousels: List[schemas.CarouselItem], db:Session = Depends(get_db)):
    for carousel in carousels:
        crud.add_carousel(db, carousel)
    return {"detail": "Add Success"}


@app.get("/carousel/{canteen}")
async def get_carousels(canteen: int, db: Session = Depends(get_db)):
    return crud.get_carousel(db, canteen)


@app.delete("/carousel")
async def delete_cardousels(carousels: List[schemas.CarouselItem], db:Session = Depends(get_db)):
    for carousel in carousels:
        crud.delete_carousel(db, carousel)
    return {"detail": "Delete Success"} 


@app.post("/new")
async def add_new_dishes(new_dishes: List[int] = [1], db: Session = Depends(get_db)):
    for new_dish in new_dishes:
        crud.add_new_dish(db, new_dish)
    return {"detail": "Add Success"} 


@app.get("/new/{canteen}")
async def get_new_dishes(canteen: int, db: Session = Depends(get_db)):
    return crud.get_new_dish(db, canteen)


@app.delete("/new")
async def delete_new_dishes(new_dishes: List[int] = [1], db: Session = Depends(get_db)):
    for new_dish in new_dishes:
        crud.delete_new_dish(db, new_dish)
    return {"detail": "Delete Success"} 
""" ********************轮播图与上新宣传******************** """

""" ***********************反馈系统************************ """
@app.post("/comment")
async def post_comment(comment: schemas.CommentItem, db: Session = Depends(get_db)):
    crud.post_comment(db, comment)
    
    
@app.get("/comment/{canteen}")
async def get_comment(canteen: int, db: Session = Depends(get_db)):
    return crud.get_comment(db, canteen)


@app.delete("/comment")
async def delete_comment(comment: schemas.CommentDelItem, db: Session = Depends(get_db)):
    crud.delete_comment(db, comment)
    return {"Detail": "Delete Success"}
""" ***********************反馈系统************************ """


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)
