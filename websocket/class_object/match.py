from warship.websocket.class_object.client import Client


class Match:
    def __init__(self, match_id, secret_key):
        self.id = match_id
        self.secret_key = secret_key
        self.status = "wait"
        self.client_list = []

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

    def client_place_ship(self, client_id, list_ships):
        for client in self.client_list:
            if client.client_id == client_id:
                ok, msg = client.place_list_ship(list_ships)
                return ok, msg

        return False, "Invalid client id"
