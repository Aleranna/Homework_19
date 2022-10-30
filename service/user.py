import jwt
import hashlib
import datetime
import calendar
from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        data['password'] = self.get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_token(self, data: dict):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, PWD_HASH_SALT)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, PWD_HASH_SALT)

        return {'access_token': access_token, 'refresh_token': refresh_token, 'exp': data['exp']}

    def check_token(self, token):
        try:
            data = jwt.decode(jwt=token, key=PWD_HASH_SALT, algorithms='HS256')
            return self.get_token(data)
        except Exception as e:
            return None

    def auth_user(self, username, password):
        user = self.dao.get_by_username(username)

        if not user:
            return None

        hash_password = self.get_hash(password)

        if hash_password != user.password:
            return None

        data = {
            'username': user.username,
            'role': user.role
        }

        return self.get_token(data)


