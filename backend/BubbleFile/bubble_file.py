# Setup steps from: https://github.com/googleapis/python-storage
# Documentation for bucket obj: https://googleapis.dev/python/storage/latest/buckets.html
# Documentation for blob obj: https://googleapis.dev/python/storage/latest/blobs.html
# Documentation for uploading files: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

# Importing the relevant files
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ, times,path
from werkzeug.utils import secure_filename
import werkzeug
import json
from google.cloud import storage
class BucketConnector:
    def __init__(self):
        """
        Create connection to GCP Bucket
        Still pending how docker will handle this, need to test out
        """
        self.bucket_name = environ.get("BucketName",default="end_mentoring_bubble")
        client = storage.Client()
        self.bucket = client.get_bucket(self.bucket_name)

    def upload_file(self,file_name: str, user_file):
        """
        Uploading file to GCP Bucket
        """
        blob = self.bucket.blob(file_name)
        try:
            # with open(user_file, "rb") as file:
            blob.upload_from_file(user_file)
            return jsonify({
                "status":"success",
                "url":blob.public_url
            })

        except Exception as e:
            # Documentation can't find the exact exception that is raised here.
            return jsonify({
                "status":"failed",
                "error_msg":e
            })

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL",default='mysql+mysqlconnector://root:root@localhost:3306/esd_db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Validating file size and type
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 # 10 MB
app.config["UPLOAD_EXTENSIONS"] = ["pdf","docx","pptx","txt"]

db = SQLAlchemy(app)
bc = BucketConnector()

class BubbleFile(db.Model):
    __tablename__ = "BubbleFile"

    bubble_id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.Integer(), primary_key=True)
    blob_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, bubble_id, timestamp, blob_url,description):
        self.bubble_id = bubble_id
        self.timestamp = timestamp
        self.blob_url = blob_url
        self.description = description

    def json(self):
        return {
            "bubble_id":self.bubble_id,
            "timestamp":self.timestamp,
            "blob_url":self.blob_url,
            "description":self.description
        }

@app.route("/bubble/file/<int:bubble_id>",methods=['GET'])
def get_bubble_files(bubble_id: int):
    files = BubbleFile.query.filter(BubbleFile.bubble_id == bubble_id).all()
    if files:
        file_json = [file.json() for file in files]
        return jsonify({
            "code": 200,
            "message":"bubble file data success",
            "data": file_json
        }),200
    else:
        return jsonify({
            "code": 404,
            "message": "No bubble files for bubble id {}".format(bubble_id)
        }), 404

@app.route("/bubble/file",methods=['POST'])
def upload_bubble_files():
    try:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
    except werkzeug.exceptions.RequestEntityTooLarge as e:
        return jsonify({
            "code":413,
            "message": str(e) + "- {} MB.".format(app.config["MAX_CONTENT_LENGTH"])
        }),413
    
    if filename == "":
        return jsonify({
            "code":404,
            "message": "No file attached."
        }),404

    try:
        bubble_id = request.form.get('bubble_id')
        current_datetime = datetime.now().timestamp()
        description = request.form.get('description')
        
    except:
        return jsonify({
            "code":404,
            "message": "Insufficient details provided for upload."
        }),404
    
    file_ext = filename.split('.')[-1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return jsonify({
            "code":415,
            "message": "Invalid filetype provided."
        }),415

    # Upload to GCP Blob
    blob_status = bc.upload_file(filename,uploaded_file).json
    if blob_status["status"] == "failed":
        return jsonify({
                "code":404,
                "message": blob_status["error_msg"]
            }),404

    try:
        new_file = BubbleFile(bubble_id, current_datetime, blob_status["url"] ,description)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({
                "code":201,
                "message": "bubble file upload success"
            }),201

    except Exception as err:
        return jsonify({
            "code": 500,
            "message": "Failed to upload file",
            "data": str(err)
        }), 500

if __name__ == "__main__":
    PYTHON_ENV = environ.get("PYTHON_ENV",default="DEV")
    app.run(host="0.0.0.0", port=5007, debug=(PYTHON_ENV == "DEV"))