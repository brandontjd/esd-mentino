# Importing the relevant files
from datetime import datetime
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
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:root@localhost:3306/esd_db'

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
def get_single_bubble_detail(bubble_id: int):
    """
    Join the bubble and bubble comment tables to get bubble details.
    No header needed cos does not pass through Kong

    :param bubble_id: bubble id 
    :type bubble_id: int
    :return: bubble data if available
    :rtype: json
    """
    bubble = Bubble.query.filter(Bubble.bubble_id == bubble_id).first()
    bubble_comment = BubbleComment.query.filter(BubbleComment.bubble_id == bubble_id).all()

    if bubble:
        bubble_json = bubble.json()
        bubble_json['comments'] = [comment.json() for comment in bubble_comment]
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
    Join the bubble and bubble comment tables to get ALL bubble details.
    No header needed cos does not pass through Kong

    :return: all bubble data if available
    :rtype: json
    """
    bubble_list = Bubble.query.all()
    return_list = []
    if bubble_list:
        for bubbles in bubble_list:
            bubble = bubbles.json()
            bubble_comment = BubbleComment.query.filter(BubbleComment.bubble_id == bubble['bubble_id']).all()
            bubble['comments'] = [comment.json() for comment in bubble_comment]
            return_list.append(bubble)

        return jsonify({
            "code": 200,
            "data": return_list
        }),200
    else: 
        return jsonify({
            "code": 404,
            "message": "No bubble exists"
        }), 404

@app.route("/bubble_details/comment",methods=['POST','DELETE'])
def add_delete_comment():
    """
    Add or Delete Comment for a specific bubble
    No header needed cos does not pass through Kong

    :return: response msg
    :rtype: json
    """
    # Adding
    if request.method == 'POST':
        bubble_id = request.form['bubble_id']
        email = request.form['email']
        current_datetime = datetime.now().timestamp()
        comment = request.form['comment']
        try:
            new_comment = BubbleComment(bubble_id, email,current_datetime, comment)
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Bubble comment success"
            }),201
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to add comment"
            }), 404
    elif request.method == 'DELETE':
        bubble_id = request.form['bubble_id']
        email = request.form['email']
        timestamp = request.form['timestamp']
        try:
            BubbleComment.query.filter(BubbleComment.bubble_id == bubble_id, BubbleComment.email == email, BubbleComment.timestamp == timestamp).delete()
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Bubble successfully deleted"
            }),200
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to delete comment"
            }), 404
    else:
        return jsonify({
                "code": 404,
                "message": "Invalid method provided"
            }), 404

@app.route('/bubble_details/one',methods=['POST','PUT','DELETE'])
def create_new_bubble():
    """
    Create, update and delete bubble details record

    :return: all bubble data if available
    :rtype: json
    """
    if request.method == 'POST':
        try:
            highest_bubble_id = db.session.query(db.func.max(Bubble.bubble_id)).scalar() + 1
        except:
            # If fail to query, it means no bubbles exist yet
            highest_bubble_id = 1

        bubble_id = highest_bubble_id
        bubble_name = request.form['bubble_name']
        create_timestamp = datetime.now().timestamp()
        meet_timestamp = request.form['meet_timestamp']
        capacity = request.form['capacity']
        agenda = request.form['agenda']
        module_code = request.form['module_code']

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
                "code": 404,
                "message": "Failed to create new bubble"
            }), 404

    if request.method == 'PUT':
        bubble_id = request.form['bubble_id']
        bubble_name = request.form['bubble_name']
        meet_timestamp = request.form['meet_timestamp']
        capacity = request.form['capacity']
        agenda = request.form['agenda']
        module_code = request.form['module_code']

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
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to update bubble"
            }), 404

    if request.method == 'DELETE':
        bubble_id = request.form['bubble_id']
        
        try:
            Bubble.query.filter(Bubble.bubble_id==bubble_id).delete()
            BubbleComment.query.filter(BubbleComment.bubble_id==bubble_id).delete()
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Delete bubble success",
            }),200
        except:
            return jsonify({
                "code": 404,
                "message": "Failed to delete bubble"
            }), 404

if __name__ == "__main__":
    # There are multiple addresses on machine
    # 0.0.0.0 means machine is listening on all the ports
    app.run(host="0.0.0.0", port=5000, debug=True)