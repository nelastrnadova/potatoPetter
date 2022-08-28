import json

from models.users import User
from routes.BaseRoute import BaseRoute


class RegisterUser(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        if 'username' not in self.body:
            return '{"missing_arguments": "username"}', 400
        if 'password' not in self.body:
            return '{"missing_arguments": "password"}', 400
        # TODO: test
        new_user = User(username=self.body['username'], password=self.body['password'])
        new_user.save(db=self.db)
        return json.dumps({"new_user_id": new_user.get_cached_pk_value()}), 200
