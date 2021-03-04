# Importing the relevant files
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ

# Instanitating the flask application
app = Flask(__name__)

# This is for production time to be used
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")

# When developing, run init.sql inside MAMP / WAMP and use this line instead for SQLALCHEMY_DATABASE_URI
# If WAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('mysql+mysqlconnector://root@localhost:3306/book')
# IF MAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('mysql+mysqlconnector://root:root@localhost:3306/book')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Instanitating the SQLAlchemy DB
db = SQLAlchemy(app)

# Creating the database object
# Refer to init.sql for table name and the datatypes
# To keep things simple, I only used varchar and integer, which in flask is String and Integer
class Bubble(db.Model):
  __tablename__ = "Bubble"

  bubble_id = db.Column(db.Integer(), primary_key=True)
  bubble_name = db.Column(db.String(255), nullable=False)
  create_timestamp = db.Column(db.Integer(), nullable=False)
  meet_timestamp = db.Column(db.Integer(), nullable=False)
  capacity = db.Column(db.Integer(), nullable=False)
  agenda = db.Column(db.String(255), nullable=False)
  module_code = db.Column(db.String(255), nullable=False)

  def __init__(self, bubble_id, bubble_name, create_timestamp, meet_timestamp, capacity, agenda,module_code):
    self.bubble_id = bubble_id
    self.bubble_name = bubble_name
    self.create_timestamp = create_timestamp
    self.meet_timestamp = meet_timestamp
    self.capacity = capacity
    self.agenda = agenda
    self.module_code = module_code 

  def json(self):
    return {
      "bubble_id": self.bubble_id,
      "bubble_name": self.bubble_name,
      "create_timestamp": self.create_timestamp,
      "meet_timestamp": self.meet_timestamp,
      "capacity": self.capacity,
      "agenda": self.agenda,
      "module_code": self.module_code
    }

@app.route("/")
def get_all():
  bubble_list = Bubble.query.all()
  if len(bubble_list):
    return jsonify({
      "code": 200,
      "data": {
        "books": [bubble.json() for bubble in bubble_list]
      }
    })
  else: 
    return jsonify({
      "code": 404,
      "message": "There are no bubbles"
    }), 404

if __name__ == "__main__":
  # There are multiple addresses on machine
  # 0.0.0.0 means machine is listening on all the ports
  app.run(host="0.0.0.0", port=5000, debug=True)