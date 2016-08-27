from flask import jsonify, request
from app import db, app, Serializer, Car, Customer
import json
from datetime import datetime


LAT_LNG_RANGE = list(range(-180, 181))


def getBool(input_string):
	if type(input_string) is str:
		if input_string.lower() == 'false':
			return False
		else:
			return True
	else:
		return False



@app.route("/")
def hello():
	return jsonify({ 'message' : 'Welcome to fuber.'})


@app.route("/car/<int:car_id>", methods=['GET'])
def get_car_details(car_id):
	car = Car.query.filter_by(id=car_id).first()
	return jsonify({ 'result' : car.serialize()})


@app.route("/car", methods=['GET'])
def get_cars():
	available_status = request.args.get('available_status')
	is_pink = request.args.get('is_pink')
	if available_status and is_pink:
		# show available and pink cars
		car_list = Car.query.filter_by(available_status=True, is_pink=True).all()
	elif is_pink:
		# show pink cars
		car_list = Car.query.filter_by(is_pink=True).all()
	elif available_status:
		# show available cars
		car_list = Car.query.filter_by(available_status=True).all()
	else:
		# show all cars
		car_list = Car.query.all()
	return jsonify({ 'result' : Serializer.serialize_list(car_list)})


@app.route("/customer", methods=['GET'])
def get_customers():
	customer_list = Customer.query.all()
	return jsonify(dict(result=Serializer.serialize_list(customer_list)))


@app.route("/car", methods=['POST'])
def add_car():
	response = None
	try:
		params = dict()
		params.update({ 'latitude' : request.form.get(['latitude'])})
		params.update({ 'longitude' : request.form.get(['longitude'])})
		params.update({ 'is_pink' : getBool(request.form.get(['is_pink']))})

		if round(params.get('latitude')) in LAT_LNG_RANGE and round(params.get('longitude')) in LAT_LNG_RANGE:
			car = Car(params.get('latitude'), params.get('longitude'), params.get('is_pink'))
			db.session.add(car)
			db.session.commit()
			response = jsonify(dict(result=params))
		else:
			response = jsonify(dict(result="Please provide valid latitude/longitude."))
	except ValueError as e:
		response = jsonify({ 'result' : 'Please provide valid latitude/longitude.'})
	except Exception as e:
		response = jsonify(dict(result="Oops! Something went wrong. Please try again."))
	return response


@app.route('/customer/<int:customer_id>/complete', methods=['POST'])
def finish_journey(customer_id):
	response = None
	try:
		params = dict()
		params.update({ 'latitude' : float(request.form.get('latitude', None))})
		params.update({ 'longitude' : float(request.form.get('longitude', None))})
		params.update({ 'customer_id' : int(customer_id)})

		if round(params.get('latitude')) in LAT_LNG_RANGE and round(params.get('longitude')) in LAT_LNG_RANGE:
			booking_customer = Customer.query.filter_by(id=params.get('customer_id')).first()
			booking_car = Car.query.filter_by(id=booking_customer.car_id).first()
			completed_on = datetime.now()
			booking_amount = Customer.set_amount(booking_customer.booked_on, completed_on, booking_car.is_pink)
			Customer.query.filter_by(id=params.get('customer_id')).update(dict(completed_on=completed_on, amount=booking_amount))
			Car.query.filter_by(id=booking_customer.car_id).update(dict(available_status=True, latitude=params.get('latitude'), longitude=params.get('longitude')))
			db.session.commit()
			
			response = jsonify(dict(result="Journey completed successfully."))
		else:
			response = jsonify({'result' : "Please provide valid latitude and longitude."})
	except ValueError as e:
		response = jsonify(dict(result="Please provide valid latitude/longitude."))
	except AttributeError as e:
		response = jsonify(dict(result="Oops! Customer with given id does not exists. Please check customer_id."))
	except Exception as e:
		response = jsonify(dict(result="Oops! Something went wrong. Please try again."))
	return response


@app.route('/customer/book', methods=['POST'])
def book_car():
	response = None
	try:
		params = dict()
		params.update({ 'latitude' : float(request.form.get('latitude'))})
		params.update({ 'longitude' : float(request.form.get('longitude'))})
		params.update({ 'is_pink' : getBool(request.form.get('is_pink'))})
		params.update({ 'booked_on' : datetime.now()})

		if round(params.get('latitude')) in LAT_LNG_RANGE and round(params.get('longitude')) in LAT_LNG_RANGE:
			available_cars = Car.query.filter_by(is_pink=params.get('is_pink'), available_status=True).all()

			if available_cars:
				distance = {}
				for car in available_cars:
					car_distance = Car.distance_travelled(params.get('latitude'), params.get('longitude'), car)
					distance.update({ car.id : car_distance})
				booking_car_id = sorted(distance.items(), key=lambda x: x[1])[0][0]
				customer = Customer(booking_car_id)
				db.session.add(customer)
				Car.query.filter_by(id=booking_car_id).update(dict(available_status=False))
				db.session.commit()
				response = jsonify({ 'result' : Serializer.serialize_list(available_cars)})
			else:
				response = jsonify({ 'result' : "NO_CARS_AVAILABLE"})
		else:
			response = jsonify({'result' : "Please provide valid latitude and longitude."})
	except ValueError as e:
		response = jsonify({'result' : "Please provide valid latitude/longitude."})
	except Exception as e:
		response = jsonify({'result' : "Oops! Something went wrong. Please try again."})

	return response
