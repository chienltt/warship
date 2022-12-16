import json

import websockets

from warship.websocket.class_object.client import Client
from warship.websocket.class_object.match import Match
# from helper import get_web_socket_connect
from warship.websocket.package import (pkt_bye, pkt_client_secret, pkt_defeat,
                                       pkt_destroyed,
                                       pkt_enemy_fired, pkt_error, pkt_ok,
                                       pkt_start,
                                       pkt_victory, pkt_wait, pkt_your_turn)

LIST_MATCH = []
LIST_CLIENT = []


def main_controller():
    return


championship_server_host = "104.194.240.16/ws/channels/"


async def send_web(data):
    print("sending data to web : ",data)
    async with websockets.connect("ws://{}".format(
            championship_server_host)) as websocket:
        print("send data: ", data)
        await websocket.send(json.dumps(data))


# This function will run when received the create match request from tournament
def create_match(match_id, secret_key, id1, id2):
    match = Match(str(match_id), str(secret_key), str(id1), str(id2))
    LIST_MATCH.append(match)
    for client in match.client_list:
        LIST_CLIENT.append(client)
    return match


# This function will run when received the connection from client
def create_client(client_id, secret_key, websocket):
    # secret_key = "secret key of client, client need send this inside every " \
    #              "package"
    client = Client(client_id, secret_key, websocket)
    LIST_CLIENT.append(client)
    return client


def remove_match(match_id):
    match_index = 0
    for index, match in LIST_MATCH:
        if match.id == match_id:
            match_index = index
            for client in match:
                remove_client(client.client_id)
    del LIST_MATCH[match_index]


def remove_client(client_id):
    client_index = 0
    for index, client in LIST_MATCH:
        if client.id == client_id:
            client_index = index
    del LIST_MATCH[client_index]


def check_client_exist(id1, id2):
    for client in LIST_CLIENT:
        if client.client_id == id1 or client.client_id == id2:
            return True
    return False


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


# ------------------handler------------------------#


async def handle_package_hello(websocket, data):
    match = find_match(data['match_id'])
    if not match:
        await websocket.send(pkt_error("match invalid"))
        return
    client, msg = match.add_connection(data["client_id"], data["secret_key"],
                                       websocket)
    if not client:
        await websocket.send(pkt_error(msg))
        return
    print("match status >>> ", match.get_status())
    # ws = get_web_socket_connect(data["client_id"])
    ws = client.get_connection()
    await ws.send(pkt_wait())
    if match.get_status() == "place_ship":
        enemy = match.get_enemy(client.client_id)
        enemy_ws = enemy.get_connection()
        await ws.send(pkt_start(client.client_id, enemy.client_id, match.id))
        await enemy_ws.send(
            pkt_start(enemy.client_id, client.client_id, match.id))
        await send_web(
            {
                "result": 1,
                "match": match.id,
            }
        )


async def handle_package_place_ship(websocket, data):
    match = find_match(str(data['match_id']))
    print("match >>>", match)
    if not match:
        await websocket.send(pkt_error("match invalid"))
        return
    client = match.find_client(data["client_id"])
    if not client:
        return
    print(client.get_connection() == websocket)
    if client.get_connection() != websocket:
        await websocket.send(pkt_error("invalid"))
        return
    # chuyen data ship thanh dạng mảng, mỗi phần tử ship là 1 mảng [[tọa độ
    # trái trên],[tọa độ phải dưới]]
    list_ships = data['list_ships']
    ok, msg = match.client_place_ship(str(data["client_id"]), list_ships)
    if not ok:
        await websocket.send(pkt_error(msg))
        return
    for ship in client.ship_list:
        print("ship in shiplist <> ", [ship.top_left_cor, ship.bot_right_cor])
    if match.check_all_client_placed_ship():
        for client in match.client_list:
            await client.connection.send(pkt_ok())
        await match.client_list[0].connection.send(
            pkt_your_turn(match.client_list[0].get_num_bullets()))
        match.change_turn(match.client_list[0].client_id)
        return
    await websocket.send(pkt_wait())
    print("current_turn >>> ", match.current_turn["client_id"])


async def handle_package_fire(websocket, data):
    match = find_match(data['match_id'])
    if not match:
        await websocket.send(pkt_error("match invalid"))
    # chuyen data cac vien dan thanh dạng mảng, mỗi phần tử ship là 1 mảng
    # toa do cua goc trai tren vien dan
    list_bullets = data["coordinates"]
    match.client_fire(data["client_id"], list_bullets)
    if not match.check_all_client_fired:
        await websocket.send(pkt_wait())
    else:
        for client in match.client_list:
            enemy = match.get_enemy(client.client_id)
            client_list_bullets = match.get_list_bullets(client.client_id)
            enemy_ws = enemy.get_connection()
            await enemy_ws.send(
                pkt_enemy_fired(len(client_list_bullets), client_list_bullets))


async def handle_package_fire1(websocket, data):
    match = find_match(data['match_id'])
    client_id = data["client_id"]
    if not match:
        await websocket.send(pkt_error("match invalid"))
        return
    if match.current_turn["client_id"] != client_id:
        await websocket.send(pkt_error("Not your turn!"))
        return
    list_bullets = data["coordinates"]
    match.client_fire(client_id, list_bullets)

    enemy = match.get_enemy(client_id)
    enemy_ws = enemy.get_connection()
    await enemy_ws.send(pkt_enemy_fired(len(match.current_turn["list_bullets"]),
                                        match.current_turn["list_bullets"]))

    destroyed_ships, msg = match.update_list_ships(enemy.client_id,
                                                   list_bullets)
    await websocket.send(pkt_destroyed(len(destroyed_ships), destroyed_ships))
    await send_match_info_to_web(match.id)
    check_win = match.check_win()
    if check_win:
        print("match end")
        await websocket.send(pkt_victory(client_id))
        await enemy_ws.send(pkt_defeat(enemy.client_id))
        await websocket.send(pkt_bye())
        await enemy_ws.send(pkt_bye())
        await send_web(
            {
                "result": 3,
                "match": match.id,
            }
        )
        remove_match(match.id)
        return

    await enemy_ws.send(pkt_your_turn(enemy.get_num_bullets()))
    match.change_turn(enemy.client_id)


async def handle_package_bye(websocket):
    return


async def send_match_info_to_web(match_id):
    status = {
        "wait": 1,
        "playing": 1,
        "finished": 2
    }
    match = find_match(match_id)
    data = {
        "result": 2,
        "match": int(match_id),
        "status": status[match.status],
        str(match.client_list[0].client_id): int(match.client_list[
                                                     0].get_num_bullets()),
        str(match.client_list[1].client_id): int(match.client_list[
                                                     0].get_num_bullets())
    }
    await send_web(data)


LIST_CONTROLLER = [
    (0, handle_package_hello),
    (3, handle_package_place_ship),
    (5, handle_package_fire1)
    # (12, handle_package_bye)
]
