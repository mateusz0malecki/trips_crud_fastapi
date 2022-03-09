from fastapi import APIRouter, Depends, status, Response, HTTPException, responses
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from data import database, models, schemas
from data.hash import Hash
from data.JWT import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from data.JWT import check_if_active_user


router = APIRouter(
    tags=['Authentication'])


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(response: Response, data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.name == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username.")
    if not Hash.verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/logout')
async def logout(current_user: schemas.User = Depends(check_if_active_user)):
    response = responses.PlainTextResponse(content="Logged out.")
    response.delete_cookie(key="access_token")
    return response


@router.get('/init_app')
async def init_app(db: Session = Depends(database.get_db)):
    active_admins = db.query(models.User).filter(models.User.is_active).count()
    if active_admins > 0:
        return {'Application is already set-up. Nothing to do'}
    else:
        new_admin = models.User(user_id=1, name='admin', email='noone@blablabla',
                                password=Hash.get_password_hash('admin'), is_active=True, is_admin=True)
        db.add(new_admin)
        db.commit()
        return {'User admin has been created'}
