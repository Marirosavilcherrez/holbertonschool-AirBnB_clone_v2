#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import os
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, nullable=False,
                    default=lambda: str(uuid.uuid4()))
        '''CHECK: DATETIME CAN"T BE NULL'''
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    else:
        def __init__(self, *args, **kwargs):
            """Instatntiates a new model"""
            if not kwargs:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = self.created_at
            else:
                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())
                if kwargs.get("created_at"):
                    kwargs["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.created_at = datetime.now()
                if kwargs.get("updated_at"):
                    kwargs["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.updated_at = datetime.now()
                for key, value in kwargs.items():
                    if "__class__" not in key:
                        setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls_name = self.__class__.__name__
        filtered_dict = {key: value for key, value in self.to_dict().items() if key != '__class__'}
        return '[{}] ({}) {}'.format(cls_name, self.id, filtered_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key not in ['_sa_instance_state']:
                    dictionary[key] = value
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
