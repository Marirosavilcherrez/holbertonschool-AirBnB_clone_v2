#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
import os

class City(BaseModel, Base):
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        """ defines the attributes to be stored in the DB """
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    else:
        """defines the attributes to be stored in the JSON"""
        state_id = ""
        name = ""
