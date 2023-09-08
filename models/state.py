#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade="all, delete", backref="state")

    else:
        @property
        def cities(self):
            "return the list of instances from City"
            from models import storage
            list_cities = []
            for k in models.storage.all('City').values():
                if k.state_id == self.id:
                    list_cities.append(k)
            return list_cities
