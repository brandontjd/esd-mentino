# Importing the relevant files
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times
from flask_cors import CORS

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL",default='mysql+mysqlconnector://root:root@localhost:3306/esd_db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "*"}})
class Bubble(db.Model):
    __tablename__ = "Bubble"

    bubble_id = db.Column(db.Integer(), primary_key=True)
    bubble_name = db.Column(db.String(255), nullable=False)
    create_timestamp = db.Column(db.Integer(), nullable=False)
    meet_timestamp = db.Column(db.Integer(), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    agenda = db.Column(db.Text, nullable=False)
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

@app.route("/bubble_details/one/<int:bubble_id>",methods=['GET'])
def get_single_bubble_detail(bubble_id: int):
    """
    Get bubble detail based on bubble_id

    :param bubble_id: bubble id 
    :type bubble_id: int
    :return: bubble data if available
    :rtype: json
    """
    bubble = Bubble.query.filter(Bubble.bubble_id == bubble_id).first()
    if bubble:
        bubble_json = bubble.json()
        return jsonify({
            "code": 200,
            "data": bubble_json
        }),200
    else: 
        return jsonify({
            "code": 404,
            "message": "No bubble exists for bubble id {}".format(bubble_id)
        }), 404

@app.route("/bubble_details/all",methods=['GET'])
def get_all_bubble_detail():
    """
    Get all bubble details

    :return: all bubble data if available
    :rtype: json
    """
    bubbles = Bubble.query.filter(Bubble.meet_timestamp >= datetime.now().timestamp()).all()
    if bubbles:
        bubble_json = [bubble.json() for bubble in bubbles]
        return jsonify({
            "code": 200,
            "data": bubble_json
        }),200
    else: 
        return jsonify({
            "code": 404,
            "message": "No bubble exists"
        }), 404

@app.route('/bubble_details/one',methods=['POST','PUT','DELETE'])
def create_new_bubble():
    """
    Create a bubble
    :return: all bubble data if available
    :rtype: json
    """
    if request.method == 'POST':
        try:
            # Get highest bubble id in DB
            highest_bubble_id = db.session.query(db.func.max(Bubble.bubble_id)).scalar() + 1
        except:
            # If fail to query, it means no bubbles exist yet
            highest_bubble_id = 1

        bubble_id = highest_bubble_id
        try:
            json_payload = request.get_json()
            bubble_name = json_payload['bubble_name']
            create_timestamp = datetime.now().timestamp()
            meet_timestamp = json_payload['meet_timestamp']
            capacity = json_payload['capacity']
            agenda = json_payload['agenda']
            module_code = json_payload['module_code']
        except:
            return jsonify({
                "code": 403,
                "message": "Insufficient details provided to create bubble",
            }), 403

        try:
            new_bubble = Bubble(bubble_id, bubble_name, create_timestamp, meet_timestamp, capacity, agenda,module_code)
            db.session.add(new_bubble)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Create bubble details success",
                "data": new_bubble.json()
            }),201
        except:
            return jsonify({
                "code": 500,
                "message": "Failed to create new bubble"
            }), 500

    if request.method == 'PUT':
        try:
            json_payload = request.get_json()
            bubble_id = json_payload['bubble_id']
            bubble_name = json_payload['bubble_name']
            meet_timestamp = json_payload['meet_timestamp']
            capacity = json_payload['capacity']
            agenda = json_payload['agenda']
            module_code = json_payload['module_code']
        except:
            return jsonify({
                "code": 403,
                "message": "Insufficient details provided to update bubble",
            }), 403

        try:
            to_be_updated_bubble = Bubble.query.filter_by(bubble_id=bubble_id).first()
            to_be_updated_bubble.bubble_id = bubble_id
            to_be_updated_bubble.bubble_name = bubble_name
            to_be_updated_bubble.meet_timestamp = meet_timestamp
            to_be_updated_bubble.capacity = capacity
            to_be_updated_bubble.agenda = agenda
            to_be_updated_bubble.module_code = module_code
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Update bubble details success",
                "data": to_be_updated_bubble.json()
            }),200
        except Exception as e:
            return jsonify({
                "code": 404,
                "message": "Failed to update bubble - bubble does not exist."
            }), 404

    if request.method == 'DELETE':
        json_payload = request.get_json()
        bubble_id = json_payload['bubble_id']
        
        try:
            Bubble.query.filter(Bubble.bubble_id==bubble_id).delete()
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Delete bubble success",
            }),200
        except Exception as e:
            return jsonify({
                "code": 404,
                "message": "Failed to delete bubble - {}".format(str(e))
            }), 404

if __name__ == "__main__":
    PYTHON_ENV = environ.get("PYTHON_ENV",default="DEV")
    app.run(host="0.0.0.0", port=5002, debug=(PYTHON_ENV == "DEV"))