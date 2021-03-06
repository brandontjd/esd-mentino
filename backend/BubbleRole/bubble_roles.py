# Importing the relevant files
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times

# Instanitating the flask application
app = Flask(__name__)

# This is for production time to be used
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")

# When developing, run init.sql inside MAMP / WAMP and use this line instead for SQLALCHEMY_DATABASE_URI
# If WAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/esd_db'
# IF MAMP:
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:root@localhost:8889/esd_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL", default="mysql+mysqlconnector://root:root@localhost:3306/esd_db")


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

class BubbleRole(db.Model):
    __tablename__ = "BubbleRole"

    bubble_id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)
    role = db.Column(db.String(255), nullable=False)

    def __init__(self, bubble_id, email, role):
        self.bubble_id = bubble_id
        self.email = email
        self.role = role

    def json(self):
        return {
        "bubble_id": self.bubble_id,
        "email": self.email,
        "role": self.role
        }


@app.route("/bubble_roles/one/<int:bubble_id>",methods=['GET'])
def get_all_participants_of_bubble(bubble_id: int):
    """
    Get all participants associated with one bubble
    No header needed cos does not pass through Kong
    
    """
    bubble = Bubble.query.filter(Bubble.bubble_id == bubble_id).first()
    bubble_role = BubbleRole.query.filter(BubbleRole.bubble_id == bubble_id).all()

    if bubble:
        bubble_json = bubble.json()
        bubble_json['role'] = [role.json() for role in bubble_role]
        return jsonify({
            "code": 200,
            "message": "Got all bubble participants",
            "data": bubble_json
        }),200
    else: 
        return jsonify({
            "code": 404,
            "message": "Failed to retrieve bubble participants"
        }), 404


@app.route("/bubble_roles/person/<email>",methods=['GET'])
def get_bubbles_of_participant(email):
    """
    Get all bubbles associated with one participant
    No header needed cos does not pass through Kong
    
    """
    return_list = []
    joined_bubbles = BubbleRole.query.filter(BubbleRole.email == email).all()
    if joined_bubbles:
        for joined_bubble in joined_bubbles:
            bubble_json = joined_bubble.json()
            return_list.append(bubble_json)

        return jsonify({
            "code": 200,
            "message": "Got all bubbles of participant",
            "data": return_list
        }),200
    else: 
        return jsonify({
            "code": 404,
            "message": "Failed to retrieve bubbles of participant"
        }), 404

@app.route('/bubble_roles/one',methods=['POST','PUT','DELETE'])
def write_bubble_role():
    """
    Add, update and delete bubble roles in database

    :return: add/update/delete bubble roles msg
    :rtype: json
    """
    if request.method == 'POST':
        try:
            highest_bubble_id = db.session.query(db.func.max(Bubble.bubble_id)).scalar() + 1
        except:
            # If fail to query, it means no bubbles exist yet
            highest_bubble_id = 1

        bubble_id = highest_bubble_id
        json_payload = request.get_json()
        email = json_payload['email']
        role = json_payload['role']
        try:
            new_bubble_role = BubbleRole(bubble_id, email, role)
            db.session.add(new_bubble_role)
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Add bubble role success",
                "data": new_bubble_role.json()
            }),200
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to add bubble role"
            }), 404

    if request.method == 'PUT':
        json_payload = request.get_json()
        bubble_id = json_payload['bubble_id']
        email = json_payload['email']
        role = json_payload['role']

        try:
            to_be_updated_bubble_role = BubbleRole.query.filter(BubbleRole.bubble_id==bubble_id, BubbleRole.email==email).first()
            if (to_be_updated_bubble_role.role != role):       
                to_be_updated_bubble_role.bubble_id = bubble_id
                to_be_updated_bubble_role.email = email
                print(to_be_updated_bubble_role.role)
                to_be_updated_bubble_role.role = role
                print(to_be_updated_bubble_role.role)
                db.session.commit()
                return jsonify({
                    "code": 200,
                    "message": "Update bubble role success",
                    "data": to_be_updated_bubble.json()
                }),200
            else:
                return jsonify({
                "code": 404,
                "message": "Database record is same as entry, no need to update"
            }), 404
        except:
            return jsonify({
                "code": 404,
                "message": "Error message but database updated"
            }), 404

    if request.method == 'DELETE':
        json_payload = request.get_json()
        bubble_id = json_payload["bubble_id"]
        email = json_payload['email']
        #who should be able to delete? check if role =

        try:
            BubbleRole.query.filter(BubbleRole.bubble_id==bubble_id, BubbleRole.email==email).delete()
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Delete bubble role success",
            }),200
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to delete bubble role"
            }), 404


if __name__ == "__main__":
    # There are multiple addresses on machine
    # 0.0.0.0 means machine is listening on all the ports
    PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
    app.run(host="0.0.0.0", port=5003, debug=(PYTHON_ENV == "DEV"))
    