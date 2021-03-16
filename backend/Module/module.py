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
class Module(db.Model):
    __tablename__ = "Module"

    module_code = db.Column(db.String(255), primary_key=True)
    module_name = db.Column(db.String(255), nullable=False)

    def __init__(self, module_code, module_name):
        self.module_code = module_code
        self.module_name = module_name

    def json(self):
        return {
        "module_code": self.module_code,
        "module_name": self.module_name
        }


@app.route("/module/all",methods=['GET'])
def get_all_modules():
    """
    Get all modules

    """
    try:
        modules = Module.query.all()
        return_list = [module.json() for module in modules]
        return jsonify({
            "code": 200,
            "message": "Got all modules success",
            "data": return_list
        }),200
    except Exception as err:
        return jsonify({
            "code":404,
            "message": "Failed to get all modules",
            "data": str(err)
        }), 404

@app.route("/module/one/<string:module_code>",methods=['GET'])
def get_module(module_code:str):
    """
    Get specific module by code

    """
    try:
        module = Module.query.filter(Module.module_code==module_code).first()
        return jsonify({
            "code": 200,
            "message": "Got module success",
            "data": module.json()
        }),200
    except Exception as err:
        return jsonify({
            "code":404,
            "message": "Failed to get module",
            "data": str(err)
        }), 404

    
@app.route('/module/one',methods=['POST','PUT','DELETE'])
def write_module_db():
    """
    Add, update and delete module in database

    """
    if request.method == 'POST':

        json_payload = request.get_json()
        module_code = json_payload['module_code']
        module_name = json_payload['module_name']
        try:
            new_module = Module(module_code,module_name)
            db.session.add(new_module)
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Add module to module db success",
                "data": new_module.json()
            }),200
        except Exception as err:
            return jsonify({
                "code": 404,
                "message": "Failed to add module to module db",
                "data": str(err)
            }), 404

    if request.method == 'PUT':
        json_payload = request.get_json()
        module_code = json_payload['module_code']
        module_name = json_payload['module_name']
        try:
            to_be_updated_module = Module.query.filter(Module.module_code==module_code).first()
            if to_be_updated_module is None:
                return jsonify({
                    "code": 404,
                    "message": "Record not found in module db"
                }), 404

            to_be_updated_module.module_code = module_code
            to_be_updated_module.module_name = module_name
            try:
                db.session.commit()
                return jsonify({
                    "code": 200,
                    "message": "Update record in module db success",
                    "data": to_be_updated_module.json()
                }),200

            except IntegrityError:
                return jsonify({
                    "code": 500,
                    "message": "Duplicate entry"
                }), 500

        except Exception as err:
            return jsonify({
                "code": 404,
                "message": "Failed to update record in module db",
                "data": str(err)
            }), 404

    if request.method == 'DELETE':
        json_payload = request.get_json()
        module_code = json_payload['module_code']

        try:
            Module.query.filter(Module.module_code==module_code).delete()
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "Delete record in module db success",
            }),200
        except Exception as err:
            return jsonify({
                "code": 404,
                "message": "Failed to delete record in module db",
                "data": str(err)
            }), 404


if __name__ == "__main__":
    # There are multiple addresses on machine
    # 0.0.0.0 means machine is listening on all the ports
    PYTHON_ENV = environ.get("PYTHON_ENV", default="DEV")
    app.run(host="0.0.0.0", port=5006, debug=(PYTHON_ENV == "DEV"))
    