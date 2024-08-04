from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric,LargeBinary, Text
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):   # This class is to be used in the future for user management
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), index=True)
    sdu_id = Column(String(20), index=True, unique=True)
    is_admin = Column(Boolean, default=False)


class Admin(Base):   # The users with privileges to do data modification, whose login should be different from the normal users
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_name = Column(String(20), index=True)
    hashed_password = Column(String(64), index=True)


class Comment(Base):   # This class is to be used in the future
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    content = Column(Text)
    vote = Column(Integer)
    time = Column(String(25), index=True)



class Canteen(Base):  
    __tablename__ = "canteens"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(8), index=True, nullable=False, unique=True)
    description = Column(Text, index=True)
    # image = Column(LargeBinary)
    image = Column(String)
    campus = Column(String(8), index=True, nullable=False)



class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen = Column(Integer, ForeignKey("canteens.id"), index=True)
    floor = Column(Integer, index=True, nullable=False)
    window = Column(Integer, index=True, nullable=False)
    name = Column(String(20), index=True, nullable=False)
    price = Column(Numeric)
    measure = Column(String(5))
    # image = Column(LargeBinary)
    image = Column(String)
    average_vote = Column(Numeric, default=2.5, index=True)
    
    
    

class NewDish(Base):
    __tablename__ = "new_dishes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), index=True)

    dish = relationship("Dish")


class Carousel(Base):
    __tablename__ = "carousels"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen = canteen = Column(Integer, ForeignKey("canteens.id"), index=True)
    image = Column(String)
