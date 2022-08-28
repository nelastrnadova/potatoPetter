import json

from models.messages import Message
from routes.BaseRoute import BaseRoute


class SendMessage(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        if 'user_to_id' not in self.body:
            return '{"missing_arguments": "user_to_id"}', 400
        if 'user_from_id' not in self.body:
            return '{"missing_arguments": "user_from_id"}', 400
        if 'text' not in self.body:
            return '{"missing_arguments": "text"}', 400
        # TODO: test
        new_message = Message(user_from_id=self.body['user_from_id'], user_to_id=self.body['user_to_id'],
                              text=self.body['text'])
        new_message.save(db=self.db)
        return json.dumps({"new_message_id": new_message.get_cached_pk_value()}), 200
