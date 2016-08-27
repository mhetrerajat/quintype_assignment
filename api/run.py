"""
	Start api with this file. Type command on terminal:
	> python3 run.py

	This module creates database and tables if they don't exists already.
"""
from os import environ
from app import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=environ.get("PORT", 5000), debug=False)
