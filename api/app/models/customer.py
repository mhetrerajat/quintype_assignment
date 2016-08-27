"""
	This module is model of Customer. It has attributes id, car_id, amount,
	booked_on and completed_on.
	It maps with table customer in database.
"""
from datetime import datetime
from app import db
from ..serializer import Serializer


class Customer(db.Model, Serializer):
	"""
		Customer class inherits from two classes db.Model and Serializer.
		It maps attributes defined in class with the columns in customer table.
		Every instance of Customer class represents one row in customer table.

		Note:
        	Do not include the `self` parameter in the ``Args`` section.

        Attributes:
        	id (int): Unique id to represent car.
        	car_id (int): Id of car booked by customer.
        	amount (int) : Amount to be paid by customer when trip completes.
        	booked_on (DateTime) : Time at which booking is done
        	completed_on (DateTime) : Time at which trip will complete.
	"""
	id = db.Column(db.Integer, primary_key=True)
	car_id = db.Column(db.Integer)
	amount = db.Column(db.Integer, default=0)
	booked_on = db.Column(db.DateTime)
	completed_on = db.Column(db.DateTime)

	def __init__(self, car_id):
		"""
    		__init__ method
    		Note:
        		Do not include the `self` parameter in the ``Args`` section.

    		Args:
        		car_id (int): id of the car to be alloted to user.
        		booked_on (DateTime) : Time at which booking is done. [AutoCalculate]
    	"""
    	self.car_id = car_id
    	self.booked_on = datetime.now()

    @staticmethod
    def set_amount(booked_on, completed_on, is_pink):
		"""
    		Calulates amount to be paid by customer. Amount is calulated by
    		computing number of minutes from booking time (i.e booked_on) and
    		time of journey completion (i.e completed_on)
    		Rate is 1 dogecoin per minute.
    		If car is pink then extra 5 dogecoin will be charged.
    		Args:
        		booked_on (DateTime): Time at which booking is done
        		completed_on (DateTime) : Time at which trip is completed
        		is_pink (bool) : Is car pink, if yes then True else False
    	"""
    	time_difference = round((completed_on - booked_on).total_seconds()/60)
    	if is_pink:
    		return time_difference+5
    	else:
    		return time_difference
