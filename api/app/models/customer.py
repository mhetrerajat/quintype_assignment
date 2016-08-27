from app import db
from ..serializer import Serializer
from datetime import datetime

class Customer(db.Model, Serializer):
	id = db.Column(db.Integer, primary_key=True)
	car_id = db.Column(db.Integer)
	amount = db.Column(db.Integer, default=0)
	booked_on = db.Column(db.DateTime)
	completed_on = db.Column(db.DateTime)

	def __init__(self, car_id):
		self.car_id = car_id
		self.booked_on = datetime.now()

	@staticmethod
	def set_amount(booked_on, completed_on, is_pink):
		time_difference = round((completed_on - booked_on).total_seconds()/60)
		if is_pink:
			return time_difference+5
		else:
			return time_difference