"""
    This modules has functions bind to particular route. Making request
    for that route will excute those functions and returns appropriate results.
    Route mentioned for function is just half URI i.e. it exculdes hostname.

    Attributes:
        LAT_LNG_RANGE (list) : List of all possible values for latitude and longitude.

"""
from datetime import datetime
from flask import jsonify, request
from app import db, app, Serializer, Car, Customer


LAT_LNG_RANGE = list(range(-180, 181))


def get_bool(input_string):
    """
        This function takes string and gives its corresponding boolean value.
        If given input is false then it returns False

        Return: Boolean

        Args:
            input_string (str) : Any string
    """
    if isinstance(input_string, str):
        if input_string.lower() == 'false':
            return False
        else:
            return True
    elif input_string == True:
        return True
    else:
        return False


@app.route("/")
def hello():
    """
        Just sample function bound with route '/'.

        Return:
            {
                'message' : 'Welcome to fuber.'
            }
    """
    return jsonify({'message': 'Welcome to fuber.'})


@app.route("/car/<int:car_id>", methods=['GET'])
def get_car_details(car_id):
    """
        Gives details about particular car. Function bound with route '/car/<car_id>'
        and only GET method is allowed.

        Args:
            car_id (int) : its the unique id of car

        Return:
            Instance of Car class serialized in json.
    """
    car = Car.query.filter_by(id=car_id).first()
    return jsonify({'result': car.serialize()})


@app.route("/car", methods=['GET'])
def get_cars():
    """
        Gives list of cars according filter arguments.
        Only GET method is allowed with route '/car'

        Args:
            available_status (bool) : if True, show cars available for booking
                                        and on False, show cars which are booked [Optional]
            is_pink (bool) : If true, show pink cars else on False, show cars
                                    which are not pink. [Optional]

        Return:
            List of cars matched with filter arguments
    """
    available_status = request.args.get('available_status')
    is_pink = request.args.get('is_pink')
    if available_status and is_pink:
            # show available and pink cars
        car_list = Car.query.filter_by(
            available_status=True, is_pink=True).all()
    elif is_pink:
            # show pink cars
        car_list = Car.query.filter_by(is_pink=True).all()
    elif available_status:
            # show available cars
        car_list = Car.query.filter_by(available_status=True).all()
    else:
            # show all cars
        car_list = Car.query.all()
    return jsonify({'result': Serializer.serialize_list(car_list)})


@app.route("/customer", methods=['GET'])
def get_customers():
    """
        Give list of customers. All customers who booked previously
        and the ones who booked it currently.
        Only GET method is allowed with route '/customer'

        Return:
            List of customers.
    """
    customer_list = Customer.query.all()
    return jsonify(dict(result=Serializer.serialize_list(customer_list)))


@app.route("/car", methods=['POST'])
def add_car():
    """
        Insert cars into database.
        Only POST method is allowed with route '/car'

        Args:
            latitude (float) : latitude of current location
            longitude (float) : longitude of current location
            is_pink (bool) : whether the car is pink, if it is pink then True
                            else, set to False [optional]

    """
    response = None
    try:
        params = dict()
        params.update({'latitude': float(request.form.get('latitude'))})
        params.update({'longitude': float(request.form.get('longitude'))})
        params.update({'is_pink': get_bool(request.form.get('is_pink'))})

        if round(params.get('latitude')) in LAT_LNG_RANGE and round(
                params.get('longitude')) in LAT_LNG_RANGE:
            car = Car(
                params.get('latitude'),
                params.get('longitude'),
                params.get('is_pink'))
            db.session.add(car)
            db.session.commit()
            response = jsonify(dict(result=params))
        else:
            response = jsonify(
                dict(result="Please provide valid latitude/longitude."))
    except ValueError as e:
        response = jsonify(
            {'result': 'Please provide valid latitude/longitude.'})
    except Exception as e:
        response = jsonify(
            dict(result="Oops! Something went wrong. Please try again."))
    return response


@app.route('/customer/<int:customer_id>/complete', methods=['POST'])
def finish_journey(customer_id):
    """
        Finish car trip for particular customer.
        Only POST method is allowed with route /customer/<customer_id>/complete

        Args:
            customer_id (int) : unique id of the customer
            latitude (float) : latitude of current location
            longitude (float) : longitude of current location
    """
    response = None
    try:
        params = dict()
        params.update({'latitude': float(request.form.get('latitude', None))})
        params.update(
            {'longitude': float(request.form.get('longitude', None))})
        params.update({'customer_id': int(customer_id)})

        if round(params.get('latitude')) in LAT_LNG_RANGE and round(
                params.get('longitude')) in LAT_LNG_RANGE:

            # customer with given customer_id
            booking_customer = Customer.query.filter_by(
                id=params.get('customer_id')).first()

            # car booked by given customer
            booking_car = Car.query.filter_by(
                id=booking_customer.car_id).first()
            completed_on = datetime.now()

            # calculate amount to be paid by customer after completion of trip
            booking_amount = Customer.set_amount(
                booking_customer.booked_on, completed_on, booking_car.is_pink)
            Customer.query.filter_by(id=params.get('customer_id')).update(
                dict(completed_on=completed_on, amount=booking_amount))

            # update new location of car
            Car.query.filter_by(
                id=booking_customer.car_id).update(
                    dict(available_status=True, latitude=params.get('latitude'),
                         longitude=params.get('longitude')))
            db.session.commit()

            response = jsonify(dict(result="Journey completed successfully."))
        else:
            response = jsonify(
                {'result': "Please provide valid latitude and longitude."})
    except ValueError as e:
        response = jsonify(
            dict(result="Please provide valid latitude/longitude."))
    except AttributeError as e:
        response = jsonify(
            dict(
                result="Oops! Customer with given id does not exists. Please check customer_id."))
    except Exception as e:
        response = jsonify(
            dict(result="Oops! Something went wrong. Please try again."))
    return response


@app.route('/customer/book', methods=['POST'])
def book_car():
    """
        Book car
        Only POST method is allowed with route /customer/book

        Args:
            latitude (float) : current location (latitude) of customer
            longitude (float) : current location (longitude) of customer
            is_pink (bool) : does customer want pink car, true if want else False [Optional]
            booked_on (DateTime) : booking time [AutoCalculate]
    """
    response = None
    try:
        params = dict()
        params.update({'latitude': float(request.form.get('latitude'))})
        params.update({'longitude': float(request.form.get('longitude'))})
        params.update({'is_pink': get_bool(request.form.get('is_pink'))})
        params.update({'booked_on': datetime.now()})

        if round(params.get('latitude')) in LAT_LNG_RANGE and round(
                params.get('longitude')) in LAT_LNG_RANGE:

            # check for cars as per customer's preference
            available_cars = Car.query.filter_by(
                is_pink=params.get('is_pink'), available_status=True).all()

            if available_cars:
                # calculate distance between car's location and customer's location
                distance = {}
                for car in available_cars:
                    car_distance = Car.distance_travelled(
                        params.get('latitude'), params.get('longitude'), car)
                    distance.update({car.id: car_distance})
                # get id of car which is nearest to customer
                booking_car_id = sorted(
                    distance.items(), key=lambda x: x[1])[0][0]
                # alot that car to customer
                customer = Customer(booking_car_id)
                db.session.add(customer)
                Car.query.filter_by(
                    id=booking_car_id).update(
                        dict(
                            available_status=False))
                db.session.commit()
                response = jsonify(
                    {'result': Serializer.serialize_list(available_cars)})
            else:
                response = jsonify({'result': "NO_CARS_AVAILABLE"})
        else:
            response = jsonify(
                {'result': "Please provide valid latitude and longitude."})
    except ValueError as e:
        response = jsonify(
            {'result': "Please provide valid latitude/longitude."})
    except Exception as e:
        response = jsonify(
            {'result': "Oops! Something went wrong. Please try again."})

    return response


@app.errorhandler(404)
def not_found_error(error):
    """
        Page not found
        404
    """
    return jsonify(dict(result="Page not found.", status=404)), 404

@app.errorhandler(500)
def internal_error(error):
    """
        Internal Server Error
        500
    """
    return jsonify(dict(result="Oops! Something went wrong with server. Please try again", status=500)), 500
