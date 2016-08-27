"""
    This modules has functions bounded to particular route. Making request
    to that route will execute that function and return appropriate response.
    Route mentioned for function is just half URI i.e. it exculdes hostname.
"""
from flask import request, render_template
from app import app, API_BASE_URL
import requests


@app.route("/", methods=['GET', 'POST'])
def index():
    """
        This function is bounded with route '/' and supports GET, POST methods.
        GET:
            It renders index.html which is form which asks customer for latitude,
            longitude and car preference(i.e pink or not).
            Additonally, its making request to '/' route of api, just to check api is live.

        POST:
            It takes required arguments from customer and make request for booking
            to the api. The api will do its job according to that and return approriate response.

            Args:
                latitude (float) : Current location (latitude) of customer
                longitude (float) : current location (longitude) of customer
                is_pink (bool) : whether customer wants pink car, if yes then True
                                else false
    """
    response = None
    if request.method == 'GET':
        r = requests.get(API_BASE_URL)
        data = r.json()
        response = render_template(
            'index.html',
            data=data.get('message'),
            error=False)
    elif request.method == 'POST':
        try:
            params = {
                'latitude': float(request.form.get('latitude')),
                'longitude': float(request.form.get('longitude')),
                'is_pink': request.form.get('is_pink')
            }
            print(params)
            BOOK_URL = API_BASE_URL + "customer/book"
            r = requests.post(BOOK_URL, data=params)
            if r.status_code != 500:
                data = r.json()
                print(data)
                if data.get('result') == "NO_CARS_AVAILABLE":
                    response = render_template(
                        'index.html',
                        error="According to your preference, no cars are available for booking. Please try again.",
                        data=False)
                else:
                    response = render_template(
                        'index.html', error=False, data="Booking has been done successfully.")
            else:
                response = render_template(
                    'index.html',
                    error="Oops! Something went wrong with server. Please try again.",
                    data=False)
        except Exception as e:
            response = render_template(
                'index.html',
                error="Please provide valid latitude/longitude",
                data=False)
        #response = request.form.get('latitude')
    return response


@app.route("/cars")
def show_cars():
    """
        Show list of cars
        Makes request to api and asks for list of all cars.
    """
    r = requests.get(API_BASE_URL + "car")
    data = r.json()
    return render_template('show_cars.html', data=data.get('result'))


@app.route("/customers")
def show_customers():
    """
        Show list of all customers
        Makes request to api and asks for list of all customers.
    """
    r = requests.get(API_BASE_URL + "customer")
    data = r.json()
    return render_template('show_customers.html', data=data.get('result'))


@app.route("/customer/<int:customer_id>/complete", methods=["GET", "POST"])
def finish_trip(customer_id):
    """
        Finish trip
        Takes required arguments from customer and makes request to api
        to finish trip.

        Args:
            customer_id (int) : unique id of customer
            latitude (float) : current location of customer (latitude)
            longitude (float) : current location of customer (longitude)
    """
    response = None
    if request.method == 'GET':
        data = "Your customer id is : " + str(customer_id)
        response = render_template(
            'finish_trip.html',
            error=False,
            data=data,
            customer_id=customer_id)
    elif request.method == 'POST':
        try:
            params = {
                'latitude': float(request.form.get('latitude')),
                'longitude': float(request.form.get('longitude'))
            }

            FINISH_URL = API_BASE_URL + "customer/" + str(customer_id) + "/complete"
            r = requests.post(FINISH_URL, data=params)
            if r.status_code != 500:
                data = r.json()
                response = render_template(
                    'index.html',
                    error=False,
                    data=data.get('result'),
                    customer_id=customer_id)
            else:
                response = render_template(
                    'finish_trip.html',
                    error="Oops! Server has few issues. Please try again.",
                    data=False,
                    customer_id=customer_id)

        except ValueError as e:
            response = render_template(
                'finish_trip.html',
                error="Please provide valid longitude/latitude",
                data=False,
                customer_id=customer_id)
        except Exception as e:
            response = render_template(
                'finish_trip.html',
                error="Oops! Something went wrong. Please try again.",
                data=False,
                customer_id=customer_id)
    return response
