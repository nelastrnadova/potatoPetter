import json

from models.messages import Message
from routes.BaseRoute import BaseRoute


class GetMessages(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        missing_params: list() = self.check_missing_params("user_to_id")
        if missing_params:
            return BaseRoute.get_missing_params_message(missing_params)

        # TODO: what happens if there arent any messages?
        messages: [Message] = Message().get_instances_by_values(db=self.db, where_fields=["user_to_id"],
                                                                where_values=[int(self.body['user_to_id'])])
        messages_text: [str] = [message.text for message in messages]
        return json.dumps({"messages": messages_text}), 200
