from fastapi import APIRouter, Depends, status, HTTPException, Form, Response
from typing import List
from sqlalchemy.orm import Session

from data import schemas, models
from data.database import get_db
from data.JWT import check_if_active_user


router = APIRouter(
    prefix="/trips",
    tags=['Trips']
)


@router.get('/new_trip', status_code=status.HTTP_200_OK)
async def new_trip_get(current_user: schemas.User = Depends(check_if_active_user)):
    return {"template": "new_trip.html"}


@router.post('/new_trip', response_model=schemas.Trip, status_code=status.HTTP_201_CREATED)
async def new_trip_post(db: Session = Depends(get_db), current_user: schemas.User = Depends(check_if_active_user),
                        trip_name: str = Form(...), email: str = Form(...), description: str = Form(...),
                        completeness: bool = Form(...), contact: bool = Form(False)):
    created_trip = models.Trip(name=trip_name, email=email, description=description,
                               completeness=completeness, contact=contact, user_id=current_user.user_id)
    db.add(created_trip)
    db.commit()
    db.refresh(created_trip)
    return created_trip


@router.get('/', response_model=List[schemas.Trip], status_code=status.HTTP_200_OK)
async def all_trips(db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(check_if_active_user)):
    trips = models.Trip.get_trips_by_user(db, current_user.user_id)
    return trips.all()


@router.get('/edit_trip/{trip_id}', status_code=status.HTTP_200_OK)
async def edit_trip_get(trip_id: int, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(check_if_active_user)):
    trip_to_edit = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_edit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with the id {trip_id} not found.")
    if trip_to_edit.first().user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated.")
    return {"template": "edit_trip.html", "trip": trip_to_edit.first()}


@router.put('/edit_trip/{trip_id}', response_model=schemas.Trip, status_code=status.HTTP_202_ACCEPTED)
async def edit_trip_put(trip_id: int, request: schemas.Trip, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(check_if_active_user)):
    trip_to_edit = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_edit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with the id {trip_id} not found.")
    if trip_to_edit.first().user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated.")
    trip_to_edit.update(dict(request))
    db.commit()
    return trip_to_edit.first()


@router.delete('/delete_trip/{trip_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: int, db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(check_if_active_user)):
    trip_to_delete = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with the id {trip_id} not found.")
    if trip_to_delete.first().user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated.")
    trip_to_delete.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
