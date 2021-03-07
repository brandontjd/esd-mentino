# Importing the relevant files
from flask import Flask, jsonify, request
from os import environ, times
import jwt

app = Flask(__name__)

@app.route("/protected-endpoint/", methods=['POST'])
def get_all():

  # -- Only necessary if email is required -- #
  header = request.headers.get('Authorization')
  auth_token = header.split(' ')[-1]
  # Verifying signature is not necessary as this has been done when request passed through Kong
  json_payload = jwt.decode(auth_token, options={"verify_signature": False})
  email = json_payload['email']
  # ----------------------------------------- #

  try:
    return jsonify({
        "code": 200,
        "message": "You have passed through Kong authorization",
        "email": email,
    }), 200
  except Exception as err:
    return jsonify({
        "code": 500,
        "message": "You have failed Kong authorization",
        "data": str(err)
    }), 500

if __name__ == "__main__":
  # There are multiple addresses on machine
  # 0.0.0.0 means machine is listening on all the ports
  PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
  app.run(host="0.0.0.0", port=5010, debug=(PYTHON_ENV == "DEV"))
