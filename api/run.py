from app import app, db
from os import environ

if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0', port=environ.get("PORT", 5000), debug=False)