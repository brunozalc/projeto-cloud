from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.jwt import create_access_token
from sqlalchemy.exc import IntegrityError

import bcrypt


async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def register(user: UserCreate, db: Session):
    try:
        db_user = User(name=user.name, email=user.email,
                       hashed_password=await hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        access_token = create_access_token(data={"sub": str(db_user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="esse usuário já existe! talvez você queira fazer login?")


async def login(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not await verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="credenciais inválidas")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
