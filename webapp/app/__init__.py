from flask import Flask

app = Flask(__name__, template_folder='views')

API_BASE_URL = "https://fuberapi.herokuapp.com/"

from app import handler