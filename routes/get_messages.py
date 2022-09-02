import json

from models.messages import Message
from models.users import User
from routes.BaseRoute import BaseRoute


class GetMessages(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        # TODO: what happens if there arent any messages?
        messages: [Message] = Message().get_all_instances(db=self.db, order_by=Message().get_pk_column_name(), desc=True, limit=15)

        to_return: list() = list()
        for message in messages:
            processed_message = {}

            message_from_user = User(id=message.user_from_id)
            message_from_user.load(db=self.db, overwrite_cached=True)  # TODO: check user exists

            processed_message['user_from'] = message_from_user.username
            processed_message['text'] = message.text

            to_return.append(processed_message)
        if 'reverse' in self.body and self.body['reverse']:
            to_return.reverse()  # TODO: does this modify the list or return a new instance?

        return json.dumps({"messages": to_return}), 200  # TODO: pls
