from routes.BaseRoute import BaseRoute


class GetMessages(BaseRoute):
    def get(self):
        return '{"supported_methods": "POST"}', 405

    def post(self):
        if 'user_to_id' not in self.body:
            return '{"missing_arguments": "user_to_id"}', 400
        # TODO: pagination
        return '{"messages": "TODO"}', 200
