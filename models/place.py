#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.review import Review
from models.amenity import Amenity
import os

class Place(BaseModel, Base):
    """ defines the attributes to be stored in the DB """
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                   back_populates="place_amenities", viewonly=False)

        association_table = Table("place_amenity", Base.metadata,
                                  Column("place_id", String(60),
                                         ForeignKey("places.id"),
                                         primary_key=True, nullable=False),
                                  Column("amenity_id", String(60),
                                         ForeignKey("amenities.id"),
                                         primary_key=True, nullable=False))

    else:
        """ defines the attributes to be stored in the JSON """
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = ''
        number_bathrooms = ''
        max_guest = ''
        price_by_night = ''
        latitude = ''
        longitude = ''
        amenity_ids = []
        
        @property
        def reviews(self):
            """Get a list of all Reviews"""
            reviewlist = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviewlist.append(review)
            return reviewlist

        @property
        def amenities(self):
            """ Get Linked Amenities"""
            amenitylist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenitylist.append(amenity)
            return amenitylist
            
        @amenities.setter
        def amenities(self, value):
            """ Value help Amenities"""
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
