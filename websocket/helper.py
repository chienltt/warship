import math

from warship.websocket.controller import LIST_CLIENT


def get_len(data):
    return int.from_bytes(data[4:7], "little")


def get_web_socket_connect(client_id):
    for client in LIST_CLIENT:
        if client.client_id == client_id:
            return client.connection
    return None