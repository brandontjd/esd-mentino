# Importing the relevant files
from flask import Flask, jsonify, request
from os import environ
import requests

# No SQLAlchemy as it is an orchestrator
app = Flask(__name__)

# All Routes that are orchestrated
if environ.get("PYTHON_ENV", default="DEV") == "PROD":
    bubble_details_host = "http://bubble_details:5002"
    bubble_roles_host = "http://bubble_roles:5003"
    bubble_files_host = "http://bubble_files:5007"
else:
    bubble_details_host = "http://localhost:5002"
    bubble_roles_host = "http://localhost:5003"
    bubble_files_host = "http://localhost:5007"

bd_get_single_bubble = bubble_details_host + "/bubble_details/one/" # plus bubble id
bd_get_all_bubble = bubble_details_host + "/bubble_details/all"
bd_edit = bubble_details_host + "/bubble_details/one"

br_bubble_participant = bubble_roles_host + "/bubble_roles/one/" # plus bubble id
br_user_active_bubble = bubble_roles_host + "/bubble_roles/person/" # plus email
br_edit = bubble_roles_host + "/bubble_roles/one"

bf_get_files = bubble_files_host + "/bubble/file/" # plus bubble id
bf_upload_files = bubble_files_host + "/bubble/file"

def error_callback(error_data):
    """
    Helper function to reduce duplicate code.
    Forwards the error message from upstream service that the orchestrator handles.
    """
    code = error_data["code"]
    msg = error_data["message"]
    return jsonify({
        "code": code,
        "message": msg
    }), code

def unavailable_callback(service_name,e):
    return jsonify({
        "code":404,
        "message":"{} is unreachable. Error Message - {}".format(service_name,str(e))
    }),404

@app.route("/bubble_activity/all",methods=['GET'])
def get_all_bubbles():
    """
    Get bubbles to show in explore and active screens.
    0) Retrieve email from json payload (Bubble Orchestrator should decode JWT and send)
    1) Invoke bubble details to GET all bubbles
    2) Invoke bubble roles to GET bubbles that user is active in 
    3) Loop through the bubbles and check if mentor exists and num of participants 
    4) Segment the bubbles that the user is active in others
    5) Transform the data and return
    """
    try:
        email = request.get_json()["email"]
    except:
        return jsonify({
            "code":403,
            "message":"Email not provided"
        })

    active_bubbles = []
    other_bubbles = []

    try:
        # Error handling for endpoint availability
        bubble_details_response = requests.request(method="GET",url=bd_get_all_bubble)
        bubble_data = bubble_details_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Details",e)

    if bubble_details_response.status_code in range(200,300):
        # Bubble does exist, now retrieve bubble(s) that user is active 
        try:
            # Error handling for endpoint availability
            bubble_roles_response = requests.request(method="GET",url=br_user_active_bubble+email)
            bubbles_roles_data = bubble_roles_response.json()
        except Exception as e:
            return unavailable_callback("Bubble Roles",e)

        if bubble_roles_response.status_code in range(200,300):
            for bubble in bubble_data["data"]:
                bubble_id = bubble["bubble_id"]
                # Assumption that if the above doesn't throw an error, the endpoint should work
                # going forward and thus no more try and except
                bubble_participants = requests.request(method="GET",url=br_bubble_participant+str(bubble_id)).json()["data"]
                
                bubble["num_participants"] = len(bubble_participants)
                bubble["mentor_found"] = "mentor" in bubble_participants.values()
                if str(bubble_id) in bubbles_roles_data["data"].keys():
                    bubble["role"] = bubbles_roles_data["data"][str(bubble_id)]
                    active_bubbles.append(bubble)
                else:
                    other_bubbles.append(bubble)
                    
            return jsonify({
                "code":200,
                "message":"Get all bubble data success",
                "data": {
                    "active_bubbles":active_bubbles,
                    "other_bubbles":other_bubbles
                }
            }),200
        else:
            return error_callback(bubbles_roles_data)
    else:
        return error_callback(bubble_data)

@app.route("/bubble_activity/one/<int:bubble_id>",methods=['GET'])
def get_one_bubble(bubble_id):
    """
    Very similar logic to get all bubbles, so not much comments here.
    """
    try:
        email = request.get_json()["email"]
    except:
        return jsonify({
            "code":403,
            "message":"Email not provided"
        })

    url_dict = {
        "Bubble Details":bd_get_single_bubble+str(bubble_id),
        "Bubble Roles":br_user_active_bubble+email,
        "Bubble Files":bf_get_files+str(bubble_id),
        "Bubble Participants":br_bubble_participant+str(bubble_id)
    }

    response_dict = {}

    for url_name in url_dict:
        try:
            response = requests.request(method="GET",url=url_dict[url_name])
            data = response.json()
        except Exception as e:
            return unavailable_callback(url_name,e)
        
        if response.status_code not in range(200,300):
            if url_name == "Bubble Files":
                response_dict[url_name] = {"data":[{}]}
            else:
                return error_callback(data)
        else:
            response_dict[url_name] = data

    bubble = response_dict["Bubble Details"]["data"]
    bubble_participants = response_dict["Bubble Participants"]["data"]
    bubble["num_participants"] = len(bubble_participants)
    bubble["mentor_found"] = "mentor" in bubble_participants.values()
    if str(bubble_id) in response_dict["Bubble Roles"]["data"].keys():
        bubble["role"] = response_dict["Bubble Roles"]["data"][str(bubble_id)]
    else:
        bubble["role"] = "None"
    
    bubble["files"] = response_dict["Bubble Files"]["data"]
    
    return jsonify({
        "code":200,
        "message":"Get bubble data success",
        "data": bubble
    }),200
    
@app.route('/bubble_activity/one',methods=['POST'])
def create_new_bubble():
    """
    Create a bubble. No payload verification, as it should take place at the upstream service level.
    1) Invoke bubble details to create the bubble
    2) If step 1 success, then invoke bubble roles to create new record of ownership
    """
    try:
        create_bubble_response = requests.request(method="POST",url=bd_edit,json=request.get_json())
        create_bubble_data = create_bubble_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Details",e)

    if create_bubble_response.status_code in range(200,300):
        json_payload = create_bubble_data["data"].copy()
        json_payload["role"] = "owner"
        json_payload["email"] = request.get_json()["email"]
        try:
            create_roles_response = requests.request(method="POST",url=br_edit,json=json_payload)
        except Exception as e:
            return unavailable_callback("Bubble Roles",e)

        if create_roles_response.status_code in range(200,300):
            create_bubble_data["data"]["role"] = "owner"
            return jsonify({
                "code":201,
                "message":"bubble creation success",
                "data":create_bubble_data["data"]
                }),201
        else:
            return error_callback(create_roles_response.json())

    else:
        return error_callback(create_bubble_data)

@app.route("/bubble_activity/join",methods=["POST"])
def join_bubble():
    """
    Create role for user in role DB. 
    Retrieves the emails after successfully joining for downstream service to notify users
    """
    try:
        create_roles_response = requests.request(method="POST",url=br_edit,json=request.get_json())
    except Exception as e:
        return unavailable_callback("Bubble Roles",e)

    if create_roles_response.status_code in range(200,300):
        bubble_id = request.get_json()['bubble_id']
        bubble_participants = requests.request(method="GET",url=br_bubble_participant+str(bubble_id)).json()["data"]
        emails = list(bubble_participants.keys())
        return jsonify({
                "code":201,
                "message":"bubble join success",
                "data" : {
                    "emails":emails
                }
            }),201
    else:
        return error_callback(create_roles_response.json())

@app.route("/bubble_activity/upload",methods=["POST"])
def upload_file():
    """
    Upload file to GCP for the bubble.
    1) Check if user is mentor of the bubble 
    2) Invoke bubble file to upload
    """
    
    try:
        email = request.form['email']
        bubble_id = request.form['bubble_id']
    except:
        return jsonify({
            "code":400,
            "message": "Insufficient details provided for upload permissions."
        }),400

    try:
        get_bubble_participants_response = requests.request(method="GET",url=br_bubble_participant+str(bubble_id))
    except Exception as e:
        return unavailable_callback("Bubble Roles",e)

    if get_bubble_participants_response.status_code in range(200,300):
        participant_data = get_bubble_participants_response.json()["data"]
        if email not in participant_data or participant_data[email] != "mentor":
            return jsonify({
                        "code":403,
                        "message":"Unable to upload - not mentor"
                    }),403
        try:
            # Can't directly pass the file into the request due to flask handling it as a FileStorage object
            # Found some obsecure stackoverflow answer that solves this - https://stackoverflow.com/questions/24678673/using-flask-as-pass-through-proxy-for-file-upload
            file = request.files['file']
            upload_file_response = requests.request(method="POST",url=bf_upload_files,data=request.form,files={'file':(file.filename,file.stream,file.content_type,file.headers)})
        except Exception as e:
            return unavailable_callback("Bubble File",e)
        
        if upload_file_response.status_code in range(200,300):
            return jsonify({
                        "code":201,
                        "message":"Bubble file upload success"
                    }),201
        else:
            return error_callback(upload_file_response.json())
    else:
        return error_callback(get_bubble_participants_response.json())
        
if __name__ == "__main__":
    PYTHON_ENV = environ.get("PYTHON_ENV",default="DEV")
    app.run(host="0.0.0.0", port=5001, debug=(PYTHON_ENV == "DEV"))