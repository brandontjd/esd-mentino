# Importing the relevant files
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times
import hashlib
import uuid

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "dbURL", default="mysql+mysqlconnector://root@localhost:3306/esd_db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
  __tablename__ = "User"

  email = db.Column(db.String(255), primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  password_salt = db.Column(db.String(255), nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)

  def __init__(self, email, name, password_salt, password_hash):
    self.email = email
    self.name = name
    self.password_salt = password_salt
    self.password_hash = password_hash

  def json(self):
    return {
        "email": self.email,
        "name": self.name,
        "password_salt": self.password_salt,
        "password_hash": self.password_hash,
    }


@app.route("/user/signup", methods=['POST'])
def sign_up():
  """
  :param: { email: <str:email>, name: <str:name>, password: <str:password> }
  :return: { message: <str:message> }
  :rtype: json string
  """

  json_payload = request.get_json()
  email = json_payload['email']
  name = json_payload['name']
  password = json_payload['password']

  password_salt = uuid.uuid4().hex
  password_hash = hashlib.sha512(
    password.encode('utf-8') + password_salt.encode('utf-8')
  ).hexdigest()

  new_user = User(email, name, password_salt, password_hash)

  try:
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "code": 201,
        "message": "Create user success"
    }), 201
  except Exception as err:
    return jsonify({
        "code": 500,
        "message": "Failed to create new user",
        "data": str(err)
    }), 500


if __name__ == "__main__":
  # There are multiple addresses on machine
  # 0.0.0.0 means machine is listening on all the ports
  PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
  app.run(host="0.0.0.0", port=5004, debug=(PYTHON_ENV == "DEV"))
