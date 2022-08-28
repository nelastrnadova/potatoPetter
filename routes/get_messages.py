import json

from models.messages import Message
from routes.BaseRoute import BaseRoute


class GetMessages(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        if isinstance(self.body, str) or 'user_to_id' not in self.body:
            return '{"missing_arguments": "user_to_id"}', 400
        # TODO: what happens if there arent any messages?
        messages: [Message] = Message().get_instances_by_values(db=self.db, where_fields=["user_to_id"],
                                                                where_values=[int(self.body['user_to_id'])])
        messages_text: [str] = [message.text for message in messages]
        return json.dumps({"messages": messages_text}), 200
