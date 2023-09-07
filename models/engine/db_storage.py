#!/usr/bin/python3
"""This module defines a class new engine DBStorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
import os


class DbStorage:
    "Private class attributes"
    __engine = None
    __session = None

    def __init__(self):
        "Values retrieved via environment variables"
        mysql_user = os.getenv("HBNB_MYSQL_USER")
        mysql_password = os.getenv("HBNB_MYSQL_PWD")
        mysql_host = os.getenv("HBNB_MYSQL_HOST")  # here = localhost
        mysql_database = os.getenv("HBNB_MYSQL_DB")

        "Public instance methods"
        db_url = f"mysql + mysqldb://{mysql_user}:{mysql_password}\
                                     @{mysql_host}/{mysql_database}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        "Drop all tables if enviroment variable is equal to test"
        if os.getenv('HBNB_ENV') == 'test':
            Base.medadata.drop_all(self.__engine)
        Base.medadata.create_all(self.__engine)

    def all(self, cls=None):
        all_dict = {}
        if cls is None:
            "Query all types of objects"
            classes_query = [User, State, City, Amenity, Place, Review]
        else:
            classes_query = [cls]

        for clas in classes_query:
            class_name = clas.__name__
            for obj_id, obj in self.__session.items():
                key = f"{class_name}.{obj_id}"
                all_dict[key] = obj
        return all_dict

    def new(self, obj):
        "Add the object to current db session"
        self.__session.add(obj)

    def save(self):
        "Commit all changes of the current database session"
        self.session.commit()

    def delete(self, obj=None):
        "Delete from the current database session"
        if obj:
            self.__session.delete(obj)

    def reload(self):
        "Create all tables in the database"
        Base.metadata.create_all(self.__engine)
        "Create current database session from the engine"
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
