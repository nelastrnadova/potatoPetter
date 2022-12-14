import json

from models.users import User
from routes.BaseRoute import BaseRoute


class LoginUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405, "application/json"

    def post(self):
        missing_params: list() = self.check_params_exist("username", "password")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: test
        user = User(username=self.body['username'])
        user.load(db=self.db, overwrite_cached=True)
        if user.password == User.hash_pass(self.body['password']):  # TODO: hash; return cookie? token?
            return json.dumps({"user_id": user.get_cached_pk_value()}), 200, "application/json"
        return json.dumps({"errors": "incorrect password"}), 400, "application/json"
