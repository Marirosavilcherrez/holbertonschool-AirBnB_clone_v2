"""This module instantiates an object of class FileStorage"""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DbStorage
    storage = DbStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
