from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    id: int
    username: str
    age: int

class UserCreate(BaseModel):
    id: int = Field(gt=0,
                    description='User id from int in list')
    # noinspection PyArgumentList
    username: str = Field(min_lenght=3,
                          max_lenght=20)
    age: int = Field(gt=0,
                     le=150,
                     description='Age from 0 to 150')

app = FastAPI()

users: List[User] = [User(id=0, username='Имя пользователя', age=0)]

@app.get("/users", response_model=List[User])
async def get_users() -> List:
    return users

@app.post("/user/{username}/{age}", response_model=User)
async def register_user(user: UserCreate) -> User:
    new_user_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_user_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, user: UserCreate) -> User:
    for u in users:
        if u.id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int) -> User:
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return u
    raise HTTPException(status_code=404, detail="User not found")


