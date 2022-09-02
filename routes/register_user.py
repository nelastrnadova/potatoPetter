import json

from models.users import User
from routes.BaseRoute import BaseRoute


class RegisterUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        missing_params: list() = self.check_params_exist("username", "password")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: test
        new_user = User(username=self.body['username'], password=User.hash_pass(self.body['password']))
        if new_user.load(db=self.db, test_exists=True):
            return json.dumps({"errors": "username taken"}), 400
        new_user.save(db=self.db)
        return json.dumps({"new_user_id": new_user.get_cached_pk_value()}), 200
