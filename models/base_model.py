#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class BaseModel(Base):
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    create_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            "if there is not argumment key, value when create the instance"
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            "Create instance attribute for instance attribute"
            self.name = str()
        else:
            "if there is a argumment key, value when create the instance"
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            "Delete key=class, there isnt an attributte to appear"
            del kwargs['__class__']
            "Update the dictionary of attributes"
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        "Obtain name of the class split the str"
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        "Remove the key _sa_instance_state from dictionary"
        dictionary.pop['_sa_instance_state', None]
        return dictionary

    def delete(self):
        "Delete the current instance from the storage"
        storage.delete(self)
