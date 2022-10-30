from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import UserSchema
from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            abort(400)

        token = user_service.auth_user(username, password)
        if not token:
            return 'wrong username or password', 401
        return token, 201

    def put(self):
        data = request.json
        refresh_token = data.get('refresh_token')

        if refresh_token is None:
            return "token invalid", 400

        tokens = user_service.check_token(refresh_token)
        return tokens, 201
