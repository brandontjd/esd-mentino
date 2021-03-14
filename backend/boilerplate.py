# Importing the relevant files
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times
from flask_cors import CORS

# Instanitating the flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# This is for production time to be used
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")

# When developing, run init.sql inside MAMP / WAMP and use this line instead for SQLALCHEMY_DATABASE_URI
# If WAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/esd_db'
# IF MAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:root@localhost:3306/esd_db'

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

class BubbleComment(db.Model):
    __tablename__ = "BubbleComment"

    bubble_id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)
    timestamp = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(255), nullable=False)

    def __init__(self, bubble_id, email, timestamp, comment):
        self.bubble_id = bubble_id
        self.email = email
        self.timestamp = timestamp
        self.comment = comment

    def json(self):
        return {
        "bubble_id": self.bubble_id,
        "email": self.email,
        "timestamp": self.timestamp,
        "comment": self.comment
        }

@app.route("/bubble_details/one/<int:bubble_id>",methods=['GET'])
def get_single_bubble_detail(bubble_id):
    """[summary]

    :param bubble_id: [description]
    :type bubble_id: [type]
    :return: [description]
    :rtype: [type]
    """
    bubble = Bubble.query.filter(Bubble.bubble_id == bubble_id).first()
    bubble_comment = BubbleComment.query.filter(BubbleComment.bubble_id == bubble_id).all()

    if bubble:
        bubble_json = bubble.json()
        bubble_json['comments'] = [comment.json() for comment in bubble_comment]
        return jsonify({
        "code": 200,
        "data": bubble_json
        })
    else: 
        return jsonify({
        "code": 404,
        "message": "No bubble exists for bubble id {}".format(bubble_id)
        }), 404

if __name__ == "__main__":
    # There are multiple addresses on machine
    # 0.0.0.0 means machine is listening on all the ports
    app.run(host="0.0.0.0", port=5000, debug=True)