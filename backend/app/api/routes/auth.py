from app.core.auth.hashing import hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schema.auth import (
    UserRegister,
    UserResponse,
    UserLogin,
    Token,
)
from app.core.auth.jwt import create_access_token, decode_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == user.email))

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



@router.post("/login",response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )

    user = result.scalar_one_or_none()

    if (
        not user
        or not verify_password(
            credentials.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or Password",
        )

    token = create_access_token(str(user.id))

    return Token(
        access_token=token
    )