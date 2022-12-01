import json

ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 17618
game_name = "warship"
game_des = "none"
game_author = "wda"
championship_server_host = "104.194.240.16"
championship_server_port = 8881
    
# 1: pkt_start
def pkt_start(uuid, op_uuid, match_id):
    data = {
        "type": 1,
        "uuid": uuid,
        "op_uuild": op_uuid,
        "match_id": match_id
    }
    return json.dumps(data) 

# 2: pkt_ok
# Return string
def pkt_ok():
    data = {
        "type": 2
    }
    return json.dumps(data)

# 4: pkt_your_turn
def pkt_your_turn(number_of_bullets):
    data = {
        "type": 4,
        "number_of_bullets": number_of_bullets
    }
    return json.dumps(data)

# 6: pkt_enemy_fired
# coordinates = [{"x": x1, "y": y1}, {"x": x2, "y": y2},...]
def pkt_enemy_fired(number_of_shots, coordinates):
    data = {
        "type": 6,
        "number_of_shots": number_of_shots,
        "coordinates": coordinates
    }
    return json.dumps(data)

# 7: pkt_destroyed
# coordinates = [
#  {
#   "head": {x: x1, y: y1}, 
#   "tail": {x: x2, y: y2}
#  },
#  {
#   "head": {x: x3, y: y3}, 
#   "tail": {x: x4, y: y4}
#  },
# ]
def pkt_destroyed(number_destroyed_ships, destroyed_ships):
    ships = []
    for ship in destroyed_ships:
        ships.append([ship.top_left_cor, ship.bot_right_cor])
    data = {
        "type": 6,
        "number_destroyed_ships": number_destroyed_ships,
        "destroyed_ships": ships
    }
    return json.dumps(data)

# 8: pkt_victory
def pkt_victory(client_id):
    data = {
        "type": 8,
        "uuid": client_id
    }
    return json.dumps(data)

# 9: pkt_defeat
def pkt_defeat(uuid):
    data = {
        "type": 8,
        "uuid": uuid
    }
    return json.dumps(data)

# 10: pkt_wait
def pkt_wait():
    data = {
        "type": 10
    }
    return json.dumps(data)

# 11: pkt_error
def pkt_error(error):
    data = {
        "type": 11,
        "error": error
    }
    return json.dumps(data)

# 12: pkt_bye
def pkt_bye():
    data = {
        "type": 12
    }
    return json.dumps(data)

def pkt_client_secret(secret):
    data = {
        "type": 13,
        "secret": secret
    }
    return json.dumps(data)
