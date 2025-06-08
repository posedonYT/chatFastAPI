from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import database
from database.schemas.user import NewUserSchema, UserResponseSchema
from database.userdb import UserModel, setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация при запуске
    await setup_database()
    print("Database tables created")
    yield

app = FastAPI(lifespan=lifespan)

sessionDep = Annotated[AsyncSession, Depends(database.userdb.get_session)]

@app.post('/auth/reg')
async def create_user(user: NewUserSchema, session: sessionDep):
    new_user = UserModel(
        name=user.name,
        email=user.email,
        age=user.age,
        password=user.password
    )
    session.add(new_user)
    await session.commit()
    return {"ok": True, "name":new_user.name, "email":new_user.email}

@app.get('/user/{user_id}')
async def get_user(user_id: int, session: sessionDep):
    user = await session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age
    )

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
