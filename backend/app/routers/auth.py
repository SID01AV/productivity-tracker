from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check username uniqueness
    existing_username = (
        db.query(models.User)
        .filter(models.User.username == user_in.username)
        .first()
    )
    if existing_username:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # If email is provided, check email uniqueness separately
    if user_in.email:
        existing_email = (
            db.query(models.User)
            .filter(models.User.email == user_in.email)
            .first()
        )
        if existing_email:
            raise HTTPException(status_code=400, detail="Username or email already registered")

    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=auth.get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token({"sub": str(user.id)})
    user_read = schemas.UserRead.from_orm(user)
    return schemas.Token(access_token=access_token, token_type="bearer", user=user_read)


@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user: models.User = Depends(auth.get_current_user)):
    return schemas.UserRead.from_orm(current_user)

