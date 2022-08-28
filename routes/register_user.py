import json

from models.users import User
from routes.BaseRoute import BaseRoute


class RegisterUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        missing_params: list() = self.check_missing_params("username", "password")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: test
        new_user = User(username=self.body['username'], password=self.body['password'])
        new_user.save(db=self.db)
        return json.dumps({"new_user_id": new_user.get_cached_pk_value()}), 200
