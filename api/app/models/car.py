from app import db
from ..serializer import Serializer
import math

class Car(db.Model, Serializer):
	id = db.Column(db.Integer, primary_key=True)
	is_pink = db.Column(db.Boolean, default=False)
	latitude = db.Column(db.Float(precision=64))
	longitude = db.Column(db.Float(precision=64))
	available_status = db.Column(db.Boolean, default=True)

	def __init__(self, latitude, longitude, is_pink=False):
		self.latitude = latitude
		self.longitude = longitude
		self.is_pink = is_pink

	def __json__(self):
		return ['id', 'is_pink', 'latitude', 'longitude', 'available_status']


	@staticmethod
	def distance_travelled(current_latitude, current_longitude, original_car_location):
		return math.sqrt((current_latitude-original_car_location.latitude)**2 + (current_longitude-original_car_location.longitude)**2)