from pydantic import BaseModel
from enum import Enum
from typing import List
from dataclasses import dataclass


class Canteen(str, Enum):
    xinyuan = "欣园"
    yueyuan = "悦园"


@dataclass
class DishItem(BaseModel):
    """DishItem"""
    """餐厅名称"""
    canteen: str
    """楼层号"""
    floor: int
    """饭菜编号"""
    id: int
    """份量"""
    measure: str
    """名称"""
    name: str
    """价格"""
    price: float
    """窗口号"""
    window: int

    
class DishDelItem(BaseModel):
    name: str
    canteen: str
    floor: int
    window: int


class DishSearchItem(BaseModel):
    name: str

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