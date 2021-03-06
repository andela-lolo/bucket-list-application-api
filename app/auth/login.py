import json
import jwt
from app.models.bucketlist_models import Users
from config import Config
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_restful import abort, Resource


class Index(Resource):

    def get(self):
        return jsonify({"message": "Welcome to the BucketList API."
                        " Register a new user by sending a"
                        " POST request to /auth/register. "
                        "Login by sending a POST request to"
                        " /auth/login to get started."})


class Login(Resource):
    def get(self):
        return jsonify({"message": "To login,"
                        "send a POST request to /auth/login."})

    def post(self):
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(
                400,
                message="No params passed. Kindly fill you username and password")
        username = data['username']
        password = data['password']

        if not username or not password:
            abort(400,
                  message="Kindly fill in the missing details")

        user = Users.query.filter_by(username=username).first()
        if user is None:
            abort(400, message="User does not exist")
        if user.verify_password(password):
            payload = {
                'sub': user.user_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            return jsonify({"message": "Welcome {}".format(user.username),
                            "token": token.decode('utf-8')})
        abort(400, message="Invalid password")
