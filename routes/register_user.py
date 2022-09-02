import json

from models.users import User
from routes.BaseRoute import BaseRoute


class RegisterUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405, "application/json"

    def post(self):
        missing_params: list() = self.check_params_exist("username", "password")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: test
        hashed_password: str = User.hash_pass(self.body['password'])
        new_user = User(username=self.body['username'], password=hashed_password)
        if new_user.load(db=self.db, test_exists=True):
            return json.dumps({"errors": "username taken"}), 400, "application/json"

        for user in User().get_all_instances(db=self.db):  # TODO: you may not like it, but this is what peak comedy looks like
            if user.password == hashed_password:
                return json.dumps({"errors": "password is already taken"}), 400, "application/json"

        new_user.save(db=self.db)
        return json.dumps({"new_user_id": new_user.get_cached_pk_value()}), 200, "application/json"
