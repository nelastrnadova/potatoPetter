import json

from models.messages import Message
from routes.BaseRoute import BaseRoute


class SendMessage(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        missing_params: list() = self.check_params_exist("user_from_id", "text")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        new_message = Message(user_from_id=self.body['user_from_id'], text=self.body['text'])
        new_message.save(db=self.db)
        return json.dumps({"new_message_id": new_message.get_cached_pk_value()}), 200
