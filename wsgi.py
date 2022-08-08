import argparse
import json
import socket
from json import JSONDecodeError

from database import Database

parser = argparse.ArgumentParser()
parser.add_argument("-ip", type=str, help="Ip to run on", default="127.0.0.1")
parser.add_argument("-port", type=int, help="port to run on", default=8000)
parser.add_argument("-db", type=str, help="Path to db file", default="database.db")
args = parser.parse_args()

db = Database(args.db)


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
            response = router(method=method, endpoint=endpoint, body=request_body)
            connection.sendall(create_http_response(response[0], response[1]))  # TODO: support views
            connection.close()
    except KeyboardInterrupt:  # except pass.. yis
        pass

    sock.close()


def router(method: str, endpoint: str, body: json):
    if endpoint in ["", "/index", "/", "/index.php", "/index.html"]:
        return '{\"response\": \"hello potat\"}', 200 if check_method("GET", method) else '', 405
    return '', 404


def check_method(target_method: str, method: str) -> bool:
    return target_method.lower() == method.lower()


def create_http_response(response_body: str, status_code: int):  # TODO: rename to indicate it is json? support more?
    return f"HTTP/1.1 {status_code}\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode(
        "utf-8"
    )


if __name__ == "__main__":
    main(ip=args.ip, port=args.port)
