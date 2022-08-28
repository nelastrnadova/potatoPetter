import json

from models.users import User
from routes.BaseRoute import BaseRoute


class LoginUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        missing_params: list() = self.check_missing_params("username", "password")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: test
        user = User(username=self.body['username'])
        user.load(db=self.db, overwrite_cached=True)
        if user.password == self.body['password']:  # TODO: hash; return cookie? token?
            return json.dumps({"user_id": user.get_cached_pk_value()}), 200
        return json.dumps({"errors": "incorrect password"}), 400
