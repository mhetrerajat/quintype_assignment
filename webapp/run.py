"""
    Start webapp with this file. Type command on terminal:
    > python3 run.py
"""
from os import environ
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ.get("PORT", 5000), debug=False)
    