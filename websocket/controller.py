from class_object.client import Client
from class_object.match import Match
# from helper import get_web_socket_connect
from package import (pkt_bye, pkt_client_secret, pkt_defeat, pkt_destroyed,
                     pkt_enemy_fired, pkt_error, pkt_ok, pkt_start,
                     pkt_victory, pkt_wait, pkt_your_turn)

LIST_MATCH = [Match("1", "1", "1", "2")]
LIST_CLIENT = [Client("1", "1"), Client("2", "1")]


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
def create_client(client_id, secret_key, websocket):
    # secret_key = "secret key of client, client need send this inside every " \
    #              "package"
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

#------------------handler------------------------#


async def handle_package_hello(websocket, data):
    match = find_match(data['match_id'])
    if not match:
        await websocket.send(pkt_error("match invalid"))
        return
    client, msg = match.add_connection(data["client_id"], data["secret_key"], websocket)
    print("match status >>> ", match.get_status())
    if not client:
        await websocket.send(pkt_error(msg))
        return
    # ws = get_web_socket_connect(data["client_id"])
    ws = client.get_connection()
    await ws.send(pkt_wait())
    if match.get_status() == "place_ship":
        enemy = match.get_enemy(client.client_id)
        enemy_ws = enemy.get_connection()
        await ws.send(pkt_start(client.client_id, enemy.client_id, match.id))
        await enemy_ws.send(pkt_start(enemy.client_id, client.client_id, match.id))


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
    await enemy_ws.send(pkt_enemy_fired(len(match.current_turn["list_bullets"]), match.current_turn["list_bullets"]))
    
    destroyed_ships, msg = match.update_list_ships(enemy.client_id, list_bullets)
    await websocket.send(pkt_destroyed(len(destroyed_ships), destroyed_ships))

    check_win = match.check_win(client_id)
    if check_win:
        await websocket.send(pkt_victory(client_id))
        await enemy_ws.send(pkt_defeat(enemy.client_id))
        await websocket.send(pkt_bye())
        await enemy_ws.send(pkt_bye())
        return
    
    await enemy_ws.send(pkt_your_turn(enemy.get_num_bullets()))
    match.change_turn(enemy.client_id)


 


LIST_CONTROLLER = [
    (0, handle_package_hello),
    (3, handle_package_place_ship),
    (5, handle_package_fire1)
]
