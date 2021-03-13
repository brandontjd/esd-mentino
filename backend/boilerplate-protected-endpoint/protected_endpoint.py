# Importing the relevant files
from flask import Flask, jsonify, request
from os import environ, times
import jwt

from channel import Channel
import json

app = Flask(__name__)

# -- For any microservice interacting with AMQP -- #
# 1. Please copy the channel.py to your microservice folder and import accordingly
# 2. Add pika==1.2.0 to requirements.txt
# 3. Copy the chunk below
# 4. Refer to docker-compose configuration too
pika_channel = Channel(
  hostname = environ.get("RABBITMQ_HOSTNAME", default="localhost"),
  port = int(environ.get("RABBITMQ_PORT", default="5672")),
  exchangename = "esd_exchange",
  exchangetype = "topic"
)
# ------------------------------------------------ #

@app.route("/protected-endpoint", methods=['POST'])
def get_all():

  # -- Only necessary if email is required -- #
  header = request.headers.get('Authorization')
  auth_token = header.split(' ')[-1]
  # Verifying signature is not necessary as this has been done when request passed through Kong
  json_payload = jwt.decode(auth_token, options={"verify_signature": False})
  email = json_payload['email']
  # ----------------------------------------- #


  # -- Only for logging -- #
  pika_channel.basic_publish(
    routing_key="sample.log", 
    body_dict={ "email": email, "type": "info", "data": { "message": "user in protected endpoint" } }
  )
  # ---------------------- #

  return jsonify({
      "code": 200,
      "message": "You have passed through Kong authorization",
      "email": email,
  }), 200

if __name__ == "__main__":
  # There are multiple addresses on machine
  # 0.0.0.0 means machine is listening on all the ports
  PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
  app.run(host="0.0.0.0", port=5010, debug=(PYTHON_ENV == "DEV"))
