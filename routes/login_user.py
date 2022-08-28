import json

from models.users import User
from routes.BaseRoute import BaseRoute


class LoginUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        if 'username' not in self.body:
            return '{"missing_arguments": "username"}', 400
        if 'password' not in self.body:
            return '{"missing_arguments": "password"}', 400
        # TODO: test
        user = User(username=self.body['username'])
        user.load(db=self.db, overwrite_cached=True)
        if user.password == self.body['password']:  # TODO: hash; return cookie? token?
            return json.dumps({"user_id": user.get_cached_pk_value()}), 200
        return json.dumps({"errors": "incorrect password"}), 400
