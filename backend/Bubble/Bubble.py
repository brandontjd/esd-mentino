# Importing the relevant files
from flask import Flask, jsonify, request
from os import environ
import requests
import jwt
# from channel import Channel

# No SQLAlchemy as it is an orchestrator
app = Flask(__name__)

# All Routes that are orchestrated
if environ.get("PYTHON_ENV", default="DEV") == "PROD":
    bubble_activity_host = "http://bubble-activity:5001"
    module_host = "http://module:5006"
    module_verification_host = "http://module-verification:5005"
else:
    bubble_activity_host = "http://localhost:5001"
    module_host = "http://localhost:5006"
    module_verification_host = "http://localhost:5005"

ba_get_all = bubble_activity_host + "/bubble_activity/all"
ba_get_one = bubble_activity_host + "/bubble_activity/one/" # plus bubble id
ba_create_bubble = bubble_activity_host + "/bubble_activity/one" 
ba_join_bubble = bubble_activity_host + "/bubble_activity/join"
ba_upload = bubble_activity_host + "/bubble_activity/upload"

m_get_all = module_host + "/module/all"
m_get_one = module_host + "/module/one/" # plus module code
m_edit = module_host + "/module/one" # Supports POST PUT DELETE

mv_grades = module_verification_host + "/module_verification/own" # Supports PUT and GET

# # Activate pika channel for logging purposes
# pika_channel = Channel(
#   hostname = environ.get("RABBITMQ_HOSTNAME", default="localhost"),
#   port = int(environ.get("RABBITMQ_PORT", default="5672")),
#   exchangename = "esd_exchange",
#   exchangetype = "topic"
# )

def unavailable_callback(service_name,e):
    return jsonify({
        "code":404,
        "message":"{} is unreachable. Error Message - {}".format(service_name,str(e))
    }),404

def decode_jwt(request):
    """
    Helper function to decode JWT token for email
    """
    header = request.headers.get('Authorization')
    auth_token = header.split(' ')[-1]
    # Verifying signature is not necessary as this has been done when request passed through Kong
    json_payload = jwt.decode(auth_token, options={"verify_signature": False})
    email = json_payload['email']
    return {
        "email":email
    }

def logging(email,msg):
    pika_channel.basic_publish(
        routing_key="*.log", 
        body_dict={ "email": email, "type": "info", "data": { "message": msg } }
    )

@app.route("/bubble/all",methods=['GET'])
def get_all_bubbles():
    """
    1. Decode JWT token and retrive email
    2. Invoke bubble_activity.py with email payload to get all bubbles
    """
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })

    try:
        # Error handling for endpoint availability
        bubble_activity_response = requests.request(method="GET",url=ba_get_all,json=email_payload)
        # Upstream services will create the error message, hence no need to validate the status code
        # Regardless of 200 or 404, we will return it
        return bubble_activity_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Activity",e)

@app.route("/bubble/one/<int:bubble_id>",methods=['GET'])
def get_one_bubble(bubble_id):
    """
    1. Decode JWT token and retrive email
    2. Invoke bubble_activity.py with email payload to get one bubble
    """
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })

    try:
        # Error handling for endpoint availability
        bubble_activity_response = requests.request(method="GET",url=ba_get_one+str(bubble_id),json=email_payload)
        return bubble_activity_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Activity",e)

@app.route("/bubble/one",methods=['POST'])
def create_bubble():
    """
    1. Decode JWT token and retrive email
    2. Invoke bubble_activity.py with email payload to create one bubble
    """
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })

    json_payload = request.get_json()
    json_payload["email"] = email_payload['email']
    try:
        # Error handling for endpoint availability
        bubble_activity_response = requests.request(method="POST",url=ba_create_bubble,json=json_payload)
        return bubble_activity_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Activity",e)

@app.route("/bubble/join",methods=["POST"])
def join_bubble():
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })
    try:
        json_payload = request.get_json()
        role = json_payload['role']
        bubble_id = json_payload['bubble_id']
        json_payload['email'] = email_payload['email']
    except:
        return jsonify({
            "code":404,
            "message":"Insufficient details provided."
        })

    # Retrieve module code for bubble_id
    try:
        bubble_activity_response = requests.request(method="GET",url=ba_get_one+str(bubble_id),json=email_payload)
        bubble_data = bubble_activity_response.json()
        module_code = bubble_data['data']['module_code']
    except Exception as e:
        return unavailable_callback("Bubble Activity",e)

    if role == 'mentor':
        # Step 1 - check what they are verified for
        try:
            module_verification_response = requests.request(method="GET",url=mv_grades,json=email_payload)
            verification_data = module_verification_response.json()
        except Exception as e:
            return unavailable_callback("Module Verification",e)
        
        if module_code in verification_data['data']:
            if verification_data['data'][module_code] in ['A-','A','A+']:
                # Step 2 - They are verified, proceed to join
                try:
                    bubble_activity_response = requests.request(method="POST",url=ba_join_bubble,json=json_payload)
                    return bubble_activity_response.json()
                except Exception as e:
                    return unavailable_callback("Bubble Activity",e)

        # Catch all return, because if the "if" above doesn't trigger, the code will flow here
        return jsonify({
            "code":403,
            "message":"User is not verified to mentor this bubble."
        })
    else:
        # it will be participant if not mentor
        try:
            bubble_role_response = requests.request(method="POST",url=ba_join_bubble,json=json_payload)
            return bubble_role_response.json()
        except Exception as e:
            return unavailable_callback("Bubble Roles",e)
        
@app.route("/bubble/upload",methods=["POST"])
def upload_file():
    """
    1. Decode JWT token and retrive email
    2. Amend form payload and invoke bubble_activity service
    """
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })
    form_payload = dict(request.form)
    form_payload["email"] = email_payload['email']
    try:
        file = request.files['file']
        upload_file_response = requests.request(method="POST",url=ba_upload,data=form_payload,files={'file':(file.filename,file.stream,file.content_type,file.headers)})
        return upload_file_response.json()
    except Exception as e:
        return unavailable_callback("Bubble Activity",e)

@app.route("/bubble/module_verification/own",methods=['PUT'])
def module_verification_declaration():
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })
    json_payload = request.get_json()
    json_payload['email'] = email_payload['email']
    try:
        module_verification_response = requests.request(method="PUT",url=mv_grades,json=json_payload)
        return module_verification_response.json()
    except Exception as e:
        return unavailable_callback("Module Verification",e)

@app.route("/bubble/module_verification/own",methods=['GET'])
def get_declared_modules():
    try:
        email_payload = decode_jwt(request)
    except:
        return jsonify({
            "code":403,
            "message":"User is not authenticated."
        })
    try:
        module_verification_response = requests.request(method="GET",url=mv_grades,json=email_payload)
        return module_verification_response.json()
    except Exception as e:
        return unavailable_callback("Module Verification",e)
    
@app.route("/bubble/module/all",methods=['GET'])
def get_all_modules():
    try:
        module_response = requests.request(method="GET",url=m_get_all)
        return module_response.json()
    except Exception as e:
        return unavailable_callback("Module",e)

@app.route("/bubble/module/one/<string:module_code>",methods=['GET'])
def get_one_module(module_code):
    try:
        module_response = requests.request(method="GET",url=m_get_one+str(module_code))
        return module_response.json()
    except Exception as e:
        return unavailable_callback("Module",e)

if __name__ == "__main__":
    PYTHON_ENV = environ.get("PYTHON_ENV",default="DEV")
    app.run(host="0.0.0.0", port=5000, debug=(PYTHON_ENV == "DEV"))