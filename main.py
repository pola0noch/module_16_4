from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated

class User(BaseModel):
    id: int
    username: str
    age: int


app = FastAPI()

users: List[User] = []

@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    return users

@app.post("/user/{username}/{age}", response_model=User)
async def register_user(username: Annotated[str, Path(min_length=5,
                                                   max_length=20,
                                                   description='Username from 5 to 20',
                                                   title='Enter username',
                                                   example='User')],
                        age: Annotated[int, Path(ge=18,
                                                 le=120,
                                                 description='Age from 18 to 120',
                                                 title='Enter age',
                                                 example=18)]):
    new_user_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: Annotated[int, Path(ge=1,
                                                   le=100,
                                                   description='User id is int',
                                                   title='Enter User ID',
                                                   example=1)],
                      user: User):
    for u in users:
        if u.id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: Annotated[int, Path(ge=1,
                                                   le=100,
                                                   description='User id is int',
                                                   title='Enter User ID',
                                                   example=1)]):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return {"detail": f"User {u.username} with id {user_id} has been deleted"}
    raise HTTPException(status_code=404, detail="User not found")





