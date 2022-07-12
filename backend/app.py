from flask import Flask, request,send_from_directory, jsonify
from flask_cors import CORS #comment this on deployment
from flask_restful import Api
from backend.api.AmadeusApiHandler import AmadeusApiHandler
from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta, timezone
import json
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
                                unset_jwt_cookies, jwt_required, JWTManager
from backend.Record import Record

app = Flask(__name__, static_url_path='', static_folder='frontend/public')
CORS(app) #comment this on deployment
api = Api(app)

app.config["JWT_SECRET_KEY"] = "SUPER-SECRET-KEY"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
user_record = Record('user')

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data=json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        #Return original if no valid JWT
        return response

@app.route('/token', methods=["POST"])
def create_token():
    print(request.json)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    db_results = list(get_user_from_db(email))
    if email != db_results[0] or password != db_results[1]:
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token": access_token}
    print(response)
    return response

@app.route('/logout')
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/profile")
@jwt_required()
def profile():
    response_body = {"name": "test",
                    "about": "test"
                    }
    return response_body

def get_user_from_db(emailaddress):
    user_record.addQuery("email", emailaddress)
    user_record.query()
    for record in user_record.results():
        email = record['email']
        password = record['userpassword']
    return [email, password]


#api.add_resource(UserApiHandler, '/flask/newUser')
api.add_resource(AmadeusApiHandler, '/flask/search')