from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from data import models, schemas
from data.database import get_db
from data.hash import Hash
from data.JWT import check_if_active_user, check_if_superuser

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
async def users(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    all_users = models.User.get_all_users(db)
    return all_users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_user(
    request: schemas.NewUser,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_superuser),
):
    created_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hash(request.password),
        is_active=request.is_active,
        is_admin=request.is_admin,
    )
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user
    except IntegrityError as e:
        return {"message": "Given username or email is already used.", "error": e}


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_superuser),
):
    user_to_edit = models.User.get_user_by_id(db, user_id).first()
    if not user_to_edit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {user_id} not found.",
        )
    return user_to_edit


@router.put(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def edit_user(
    request: schemas.EditUser,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_superuser),
):
    user_to_edit = models.User.get_user_by_id(db, user_id)
    if not user_to_edit.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {user_id} not found.",
        )
    message = None
    if request.email == "":
        message = "Email cannot be empty"
    elif request.password == "":
        message = "Password cannot be empty"

    if not message:
        try:
            user_to_edit.update(
                {
                    "email": request.email,
                    "password": Hash.get_password_hash(request.password),
                }
            )
            db.commit()
            return user_to_edit.first()
        except IntegrityError as e:
            return {"message": "Given username or email is already used.", "error": e}
    else:
        message = "Correct error: {}".format(message)
        return message


@router.put(
    "/{action}/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.ShowUser,
)
async def edit_user_status(
    user_id: int,
    action: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_superuser),
):
    user_to_edit = models.User.get_user_by_id(db, user_id).first()
    if not user_to_edit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {user_id} not found.",
        )
    if user_to_edit.user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot edit yourself."
        )
    else:
        if action == "active":
            if user_to_edit:
                user_to_edit.is_active = (user_to_edit.is_active + 1) % 2
                db.commit()
        elif action == "admin":
            if user_to_edit:
                user_to_edit.is_admin = (user_to_edit.is_admin + 1) % 2
                db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Wrong action"
            )
        return user_to_edit


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_superuser),
):
    user_to_delete = models.User.get_user_by_id(db, user_id)
    if not user_to_delete.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {user_id} not found.",
        )
    if user_to_delete.first().user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete yourself.",
        )
    user_to_delete.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
