"""
    This module is model of Car. It has attributes id, is_pink, latitude,
    longitude and available_status.
    It maps with table car in database.
"""
import math
from app import db
from ..serializer import Serializer

class Car(db.Model, Serializer):
    """
        Car class inherits from two classes db.Model and Serializer.
        It maps attributes defined in class with the columns in car table.
        Every instance of Car class represents one row in car table.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Attributes:
            id (int): Unique id to represent car.
            is_pink (bool): Its true, if car is pink else its false.
            latitude (float) : Location of car
            longitude (float) : Location of car
            available_status (bool) : Its true, if car is available for booking
                                     else, its set to false.
    """
    id = db.Column(db.Integer, primary_key=True)
    is_pink = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float(precision=64))
    longitude = db.Column(db.Float(precision=64))
    available_status = db.Column(db.Boolean, default=True)

    def __init__(self, latitude, longitude, is_pink=False):
        """
            __init__ method
            Note:
                Do not include the `self` parameter in the ``Args`` section.

            Args:
                is_pink (bool): Its true, if car is pink else its false. [Optional]
                latitude (float) : Location of car
                longitude (float) : Location of car
        """
        self.latitude = latitude
        self.longitude = longitude
        self.is_pink = is_pink

    def __json__(self):
        """
            Serialize json
        """
        return ['id', 'is_pink', 'latitude', 'longitude', 'available_status']


    @staticmethod
    def distance_travelled(current_latitude, current_longitude, original_car_location):
        """
            Calulates distance between to current location and old location.
            Args:
                current_latitude (float): Current latitude of car
                current_longitude (float) : Current longitude of car
                original_car_location (Car) : Instance of Car class. Gives just previous
                                location of car i.e location at the time of booking.
        """
        return math.sqrt(
            (current_latitude-original_car_location.latitude)**2 +
            (current_longitude-original_car_location.longitude)**2)
