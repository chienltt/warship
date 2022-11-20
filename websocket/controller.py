from warship.websocket.controller import find_match
from warship.websocket.package import pkt_error, pkt_wait, pkt_client_secret
from warship.websocket.class_object.match import Match
from warship.websocket.class_object.client import Client

LIST_MATCH = []
LIST_CLIENT = []


def main_controller():
    return


# This function will run when received the create match request from tournament
def create_match():
    secret_key = "something so fucking secret, will generate by our server"
    match_id = "something will generate by our server"
    match = Match(match_id, secret_key)
    LIST_MATCH.append(match)
    return match


# This function will run when received the connection from client
def create_client(client_id):
    secret_key = "secret key of client, client need send this inside every " \
                 "package"
    client = Client(client_id, secret_key)
    LIST_CLIENT.append(client)
    return client


def find_match(match_id):
    for match in LIST_MATCH:
        if match.id == match_id:
            return match
    return None


def check_client_identity(data):
    client_id = data['client_id']
    for client in LIST_CLIENT:
        if client.client_id == client_id:
            if client.secret == data['client_secret']:
                return True
    return False


async def handle_package_1(websocket, data):
    match = find_match(data['match_id'])
    if not match:
        websocket.send(pkt_error("match invalid"))
    new_client = create_client()
    ok, msg = match.add_client(new_client)
    if not ok:
        websocket.send(pkt_error(msg))
    websocket.send(pkt_client_secret(new_client.secret))
