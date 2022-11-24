from warship.websocket.class_object.client import Client


class Match:
    def __init__(self, match_id, secret_key):
        self.id = match_id
        self.secret_key = secret_key
        self.status = "wait"
        self.client_list = []
        self.turn = {
            "index": 0,
            "list_bullets": []
        }

    def add_client(self, client):
        if len(self.client_list) > 1 or self.status != "wait":
            return False, "Match invalid"
        for cl in self.client_list:
            if cl.client_id == client.client_id:
                return False, "Invalid client id"
        client = Client(client.client_id)
        self.client_list.append(client)
        self.check_enough_clients()
        return True, "Success"

    def check_enough_clients(self):
        if len(self.client_list) == 2:
            self.status = "place_ship"
        return

    def check_all_client_placed_ship(self):
        for client in self.client_list:
            if not client.is_place_ship:
                return False
        self.status = "playing"
        self.turn["index"] += 1
        return True

    def check_all_client_fired(self):
        if len(self.turn["list_bullets"]) == len(self.client_list):
            return True
        return False

    def client_place_ship(self, client_id, list_ships):
        for client in self.client_list:
            if client.client_id == client_id:
                ok, msg = client.place_list_ship(list_ships)
                return ok, msg

        return False, "Invalid client id"

    def client_fire(self, client_id, list_bullets):
        for client in self.client_list:
            if client.client_id == client_id:
                self.turn["list_bullets"].append(client_id, list_bullets)

    def get_enemy(self, client_id):
        for client in self.client_list:
            if client.client_id != client_id:
                return client
        return None

    def get_list_bullets(self, client_id):
        for _client_id, list_bullets in self.turn["list_bullets"]:
            if _client_id == client_id:
                return list_bullets
