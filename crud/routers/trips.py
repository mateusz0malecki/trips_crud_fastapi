from fastapi import APIRouter, Depends, status, HTTPException, Form, Response
from typing import List
from sqlalchemy.orm import Session

from data import schemas, models
from data.database import get_db
from data.JWT import check_if_active_user


router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("/", response_model=List[schemas.Trip], status_code=status.HTTP_200_OK)
async def all_trips(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    trips = models.Trip.get_trips_by_user(db, current_user.user_id)
    return trips.all()


@router.post(
    "/", response_model=schemas.Trip, status_code=status.HTTP_201_CREATED
)
async def new_trip(
    request: schemas.Trip,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    created_trip = models.Trip(
        name=request.name,
        email=request.email,
        description=request.description,
        completeness=request.completeness,
        contact=request.contact,
        user_id=current_user.user_id
    )
    db.add(created_trip)
    db.commit()
    db.refresh(created_trip)
    return created_trip


@router.get("/{trip_id}", status_code=status.HTTP_200_OK)
async def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    trip_to_edit = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_edit.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with the id {trip_id} not found.",
        )
    if trip_to_edit.first().user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated."
        )
    return {"template": "edit_trip.html", "trip": trip_to_edit.first()}


@router.put(
    "/{trip_id}",
    response_model=schemas.Trip,
    status_code=status.HTTP_202_ACCEPTED,
)
async def edit_trip(
    trip_id: int,
    request: schemas.Trip,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    trip_to_edit = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_edit.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with the id {trip_id} not found.",
        )
    if trip_to_edit.first().user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated."
        )
    trip_to_edit.update(dict(request))
    db.commit()
    return trip_to_edit.first()


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(check_if_active_user),
):
    trip_to_delete = models.Trip.get_trip_by_id(db, trip_id)
    if not trip_to_delete.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with the id {trip_id} not found.",
        )
    if trip_to_delete.first().user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated."
        )
    trip_to_delete.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
