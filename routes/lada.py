from settings import ROOT_DIR
from routes.BaseRoute import BaseRoute
from utils.file import File


class Lada(BaseRoute):
    def get(self):
        return File(f"{ROOT_DIR}/static/lada.html").get_content(), 200, "text/html"

    def post(self):
        '{"supported_methods": "GET"}', 405, "application/json"
