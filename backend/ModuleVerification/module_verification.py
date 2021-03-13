# Importing the relevant files
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times
import json
import jwt

# Instanitating the flask application
app = Flask(__name__)

# When developing, run init.sql inside MAMP / WAMP and use this line instead for SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL", default="mysql+mysqlconnector://root:root@localhost:3306/esd_db")

# Instanitating the SQLAlchemy DB
db = SQLAlchemy(app)

# Creating the database object
# Refer to init.sql for table name and the datatypes
# To keep things simple, I only used varchar and integer, which in flask is String and Integer
class ModuleVerification(db.Model):
    __tablename__ = "ModuleVerification"

    email = db.Column(db.String(255), primary_key=True)
    module_code = db.Column(db.String(255), primary_key=True)
    module_grade = db.Column(db.String(255), nullable=False)

    def __init__(self, email, module_code, module_grade):
        self.email = email
        self.module_code = module_code
        self.module_grade = module_grade

    def json(self):
        return {
        "email": self.email,
        "module_code": self.module_code,
        "module_grade": self.module_grade
        }

class Module(db.Model):
    __tablename__ = "Module"

    module_code = db.Column(db.String(255), primary_key=True)
    module_name = db.Column(db.String(255), nullable=False)


@app.route("/module_verification/own",methods=['PUT'])
def update_module_grades():
    """
    Update module grades for mentor

    If record does not exist, create new in database

    """
    header = request.headers.get('Authorization')
    auth_token = header.split(' ')[-1]
    json_payload = jwt.decode(auth_token, options={ "verify_signature": False })
    email = json_payload['email']
    json_payload = request.get_json()
    modules_list = json_payload["modules"]

    return_list = []
    for module_obj in modules_list:
        module_code = module_obj["module_code"]
        module_grade = module_obj["module_grade"]
            
        if ModuleVerification.query.filter(ModuleVerification.email == email, ModuleVerification.module_code == module_code).first():            
            #record exists, update existing record
            record = ModuleVerification.query.filter(ModuleVerification.email == email, ModuleVerification.module_code == module_code).first()
            record.module_code = module_code
            record.module_grade = module_grade
            db.session.commit()
            return_list.append(record.json())

        else: 
            #create a new record
            new_record = ModuleVerification(email, module_code, module_grade)
            db.session.add(new_record)
            db.session.commit()
            return_list.append(new_record.json())

    try:
        return jsonify({
            "code": 200,
            "message": "Module grade update success",
            "data": return_list
        }), 200
    except Exception as err:
        return jsonify({
            "code": 404,
            "message": "Failed to update module grade",
            "data": str(err)
        }), 404


@app.route("/module_verification/own",methods=['GET'])

def get_module_grades():
    """
    Get already inputted module grades for display

    """
    header = request.headers.get('Authorization')
    auth_token = header.split(' ')[-1]
    json_payload = jwt.decode(auth_token, options={ "verify_signature": False })
    email = json_payload['email']

    return_list = []
    try:
        verified_modules = ModuleVerification.query.filter(ModuleVerification.email == email).all()
        return_list = [module.json() for module in verified_modules]
        return jsonify({
            "code": 200,
            "data": return_list,
            "message": "Got module grades success"
            }),200
    
    except Exception as err:
        return jsonify({
            "code": 404,
            "message": "Failed to get module grades",
            "data": str(err)
        }), 404

    

if __name__ == "__main__":
    # There are multiple addresses on machine
    # 0.0.0.0 means machine is listening on all the ports
    PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
    app.run(host="0.0.0.0", port=5005, debug=(PYTHON_ENV == "DEV"))
    