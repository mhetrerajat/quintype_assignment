# Quintype Assignment

### Usage
Program requires Python 3.5.2

To run api
```
cd api
python3 run.py
```
To run webapp
```
cd webapp
python3 run.py
```

### Features
1. Add and Book Cars. Car is allotted to customer according to their preference and their location. 
2. User Input Validations
3. Customer will be given nearest available car to their location.
4. If car/taxis are not available then, customer’s request will be rejected.
5. Automatic booking amount calculation after trip completion. Car is charged as 1 dogecoin per minute and pink cars are charged for extra 5 dogecoin.
6. Test cases are implemented. Refer **test.py** in **api** directory.
7. Both API and WebApp are deployed on heroku.
8. Pylint is used for code analysis.


### Deployment
- API : [FuberAPI](https://fuberapi.herokuapp.com/)
- WebApp : [FuberApp](https://fuberapp.herokuapp.com/)

### Notes
- Both API and WebApp are implemented in Python with framework called **Flask**.
- **Jinja2** is used as templating language for WebApp.
- Python’s **unittest** module is used to write test cases.
- Python’s **requests** module is used to make http request to API from WebApp.
