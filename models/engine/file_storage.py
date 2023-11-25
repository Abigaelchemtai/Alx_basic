#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    This class manages storage of hbnb models in JSON format
    to a file
    """
    __file_path = 'file.json'
    __objects = {}
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage
        """
        if cls is not None:
            some_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    some_dict[key] = value
            return some_dict
        else:
            return self.__objects

    def new(self, obj):
        """
        Adds new object to storage dictionary
        """
        if obj:
            self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """
        Saves storage dictionary to file
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        Loads stored dictionary from file
        """
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = \
                        FileStorage.classes[val['__class__']](**val)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """
        Delete an object from __objects
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()
        else:
            pass

    def close(self):
        """
        call the reload method to save changes back to JSON file
        to maintain persistence when the application stops running
        """
        self.reload()
        """ Adonijah Kiplimo/ Kevin"""