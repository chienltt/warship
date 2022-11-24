from warship.websocket.helper import get_web_socket_connect
from warship.websocket.package import pkt_error, pkt_client_secret, pkt_start, \
    pkt_ok, pkt_your_turn, pkt_wait, pkt_enemy_fired
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
def create_client(client_id, websocket):
    secret_key = "secret key of client, client need send this inside every " \
                 "package"
    client = Client(client_id, secret_key, websocket)
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


async def handle_package_hello(websocket, data):
    match = find_match(data['match_id'])
    if not match:
        websocket.send(pkt_error("match invalid"))
    new_client = create_client(data['client_id'], websocket)
    ok, msg = match.add_client(new_client)
    if not ok:
        websocket.send(pkt_error(msg))
    ws = get_web_socket_connect(data["client_id"])
    ws.send(pkt_client_secret(new_client.secret))


async def handle_package_place_ship(data):
    ws = get_web_socket_connect(data["client_id"])
    match = find_match(data['match_id'])
    if not match:
        ws.send(pkt_error("match invalid"))
    # chuyen data ship thanh dạng mảng, mỗi phần tử ship là 1 mảng [[tọa độ
    # trái trên],[tọa độ phải dưới]]
    list_ship = []
    ok, msg = match.client_place_ship(data["client_id"], list_ship)
    if not ok:
        ws.send(pkt_error(msg))
    if match.check_all_client_placed_ship():
        for client in match.client_list:
            client.connection.send(pkt_ok)
        match.client_list[0].connection.send(
            pkt_your_turn(match.client_list[0].get_num_bullets()))


async def handle_package_fire(data):
    ws = get_web_socket_connect(data["client_id"])
    match = find_match(data['match_id'])
    if not match:
        ws.send(pkt_error("match invalid"))
    # chuyen data cac vien dan thanh dạng mảng, mỗi phần tử ship là 1 mảng
    # toa do cua goc trai tren vien dan
    list_bullets = []
    match.client_fire(data["client_id"], list_bullets)
    if not match.check_all_client_fired:
        ws.send(pkt_wait())
    else:
        for client in match.client_list:
            enemy = match.get_enemy(client.client_id)
            client_list_bullets = match.get_list_bullets(client.client_id)
            enemy.connection.send(
                pkt_enemy_fired(len(client_list_bullets), client_list_bullets))


LIST_CONTROLLER = [
    (1, handle_package_hello),
    (3, handle_package_place_ship),
    (5, handle_package_fire)
]
