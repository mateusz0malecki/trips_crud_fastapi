from .database import Base
from sqlalchemy import Integer, String, Boolean, Text, Column, ForeignKey
from sqlalchemy.orm import relationship


class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    description = Column(String(200))
    completeness = Column(Boolean)
    contact = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    creator = relationship("User", back_populates="trips")

    def __repr__(self):
        return "<id: {}, name: {}>".format(self.trip_id, self.name)

    @staticmethod
    def get_all_trips(db):
        return db.query(Trip).all()

    @staticmethod
    def get_trip_by_id(db, trip_id):
        return db.query(Trip).filter(Trip.trip_id == trip_id)

    @staticmethod
    def get_trips_by_user(db, user_id):
        return db.query(Trip).filter(Trip.user_id == user_id)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(Text)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    trips = relationship("Trip", back_populates="creator")

    def __repr__(self):
        return "<id: {}, name: {}>".format(self.user_id, self.name)

    @staticmethod
    def get_all_users(db):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db, user_id):
        return db.query(User).filter(User.user_id == user_id)
