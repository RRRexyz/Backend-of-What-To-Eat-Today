from pydantic import BaseModel
from enum import Enum
from typing import List
from dataclasses import dataclass


# class Canteen(str, Enum):
#     xinyuan = "欣园"
#     yueyuan = "悦园"


@dataclass
class DishItem(BaseModel):
    canteen: int
    floor: int
    measure: str
    name: str
    price: float
    window: int
    average_vote: float
    image: str = "http://dummyimage.com/400x400"

    
class DishDelItem(BaseModel):
    name: str
    canteen: int
    floor: int
    window: int


class DishPutItem(BaseModel):
    canteen: int
    floor: int
    measure: str
    name: str
    price: float
    window: int
    image: str = "http://dummyimage.com/400x400"


class CarouselItem(BaseModel):
    canteen: int = 1
    image: str = "http://dummyimage.com/400x400"
    
    
class CommentItem(BaseModel):
    user_id: int = 666666
    dish_id: int = 1
    content: str
    vote: int = 3
    time: str = "2024-08-04 12:01:59"


class CommentDelItem(BaseModel):
    user_id: int = 666666
    dish_id: int = 1
    content: str
    time: str = "2024-08-04 12:01:59"


# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True