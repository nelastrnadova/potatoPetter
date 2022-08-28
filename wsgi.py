import argparse
import importlib
import json
import socket
from json import JSONDecodeError

from database.database import Database
from settings import ROOT_DIR

parser = argparse.ArgumentParser()
parser.add_argument("-ip", type=str, help="Ip to run on", default="127.0.0.1")
parser.add_argument("-port", type=int, help="port to run on", default=8000)
parser.add_argument("-db", type=str, help="Path to db file", default=f"{ROOT_DIR}/database.db")
args = parser.parse_args()

db: Database = Database(db_file=args.db)


def main(ip="127.0.0.1", port=8000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    running = True

    try:
        while running:
            connection, client_address = sock.accept()
            data = connection.recv(512)
            request = data.decode().split("\r\n")  # error handling
            request_info = request[0].split(" ")
            method = request_info[0]
            endpoint = request_info[1][1:]
            #  request_body: dict = {}
            try:
                split_request: list = data.decode().split("\r\n\r\n")
                request_body: dict = split_request[1] if len(split_request) > 1 else {}
            except JSONDecodeError:
                request_body: dict = {}

            if check_method(method, "OPTIONS"):  # TODO
                res = "HTTP/1.1 200\r\nAllow: GET, POST, OPTIONS\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: *\r\nAccess-Control-Allow-Headers: *\r\n".encode("utf-8")
                connection.sendall(res)
                connection.close()
                continue
            try:
                response = router(method=method, endpoint=endpoint, body=request_body)  # TODO: error handling?
            except BaseException as e:
                response = (json.dumps({"errors": e}), 500)
            #  TODO: response handler
            #  TODO: controller, views (db)
            connection.sendall(create_http_response(response[0], response[1]))  # TODO: support views; optional redirect
            connection.close()
    except KeyboardInterrupt:  # except pass.. yis
        pass
    except BaseException as e:  # TODO: no Broad exception pls
        connection.sendall(create_http_response(e, 500))
        connection.close()

    sock.close()


def snake_case_to_camel_case(snake_case: str) -> str:  # TODO: can crash easily, fix pl0x
    should_next_upper: bool = False
    camel_case: str = ""
    for c in snake_case:
        if camel_case == "":
            camel_case += c.upper()
            continue
        if c == "_":
            should_next_upper = True
            continue
        if should_next_upper:
            should_next_upper = False
            camel_case += c.upper()
            continue
        camel_case += c
    return camel_case


def router(method: str, endpoint: str, body: json):
    # print(f"getting endpoint: '{endpoint}' with method: '{method}'")  # TODO: remove debug print
    file_name: str = endpoint
    class_name: str = snake_case_to_camel_case(file_name)
    # TODO: check if exists
    route_class = getattr(importlib.import_module(f"routes.{file_name}"), class_name)(body=body, db=db)
    if check_method("GET", method):
        return route_class.get()
    elif check_method("POST", method):
        return route_class.post()
    else:
        return '{"errors": "not implemented"}', 404
    return '', 404


def check_method(target_method: str, method: str) -> bool:
    return target_method.lower() == method.lower()


def create_http_response(response_body: str, status_code: int):  # TODO: rename to indicate it is json? support more?
    return f"HTTP/1.1 {status_code}\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode(
        "utf-8"
    )


if __name__ == "__main__":
    main(ip=args.ip, port=args.port)
