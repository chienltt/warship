from warship.websocket.class_object.client import Client


class Match:
    def __init__(self, match_id, secret_key, client_id_1, client_id_2):
        self.id = match_id
        self.secret_key = secret_key
        self.status = "wait"
        self.client_list = [Client(client_id_1, self.secret_key), Client(client_id_2, self.secret_key)]
        self.turn = {
            "index": 0,
            "list_bullets": []
        }
        self.current_turn = {
            "index": 0,
            "client_id": None,
            "list_bullets": []
        }

    def add_client(self, client):
        if self.get_connection() > 1 or self.status != "wait":
            return False, "Match started"
        for cl in self.client_list:
            if cl.client_id == client.client_id:
                return False, "Invalid client id"
        client = Client(client.client_id)
        self.client_list.append(client)
        self.check_enough_clients()
        return True, "Success"
    
    def add_connection(self, client_id, secret, websocket):
        client = self.identify_client(client_id, secret)
        print("Client >>>", client.client_id)
        if not client:
            return None, "invalid client"
        if not client.is_connected():
            client.connect_to(websocket)
            self.check_enough_connections()
            return client, "Success"
        return None, "Invalid! You have more than 1 connection!"

    def find_client(self, client_id):
        for cl in self.client_list:
            if cl.client_id == client_id :
                return cl
        return None

    def identify_client(self, client_id, secret):
        for cl in self.client_list:
            if cl.client_id == client_id and cl.secret == secret:
                return cl
        return None

    def check_enough_connections(self):
        if self.count_connections() == 2:
            self.status = "place_ship"
        return

    def check_enough_clients(self):
        if self.get_connection() == 2:
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
        if self.status != 'place_ship':
            return False, "Invalid action"
        client = self.find_client(client_id)
        if client:
            ok, msg = client.place_list_ship(list_ships)
            return ok, msg
        return False, "Invalid client id"

    # def client_fire(self, client_id, list_bullets):
    #     client = self.find_client(client_id)
    #     if client:
    #         self.turn["list_bullets"].append(client_id, list_bullets)

    def client_fire(self, client_id, list_bullets):
        client = self.find_client(client_id)
        if client:
            self.current_turn["list_bullets"] = list_bullets

    def get_enemy(self, client_id):
        for client in self.client_list:
            if client.client_id != client_id:
                return client
        return None

    def get_list_bullets(self, client_id):
        for _client_id, list_bullets in self.turn["list_bullets"]:
            if _client_id == client_id:
                return list_bullets

    def count_connections(self):
        count = 0
        for cl in self.client_list:
            if cl.connection != None:
                count += 1
        return count

    def get_status(self):
        return self.status
    
    # Trả về mảng các tàu bị phá hủy
    def update_list_ships(self, enemy_client_id, list_bullets):
        print("list_bullets >>> ", list_bullets)
        client = self.find_client(enemy_client_id)
        if not client:
            return None, "Update failed, client_id is invalid"
        destroyed_ships = []
        for ship in client.ship_list:
            print("ship in shiplist <> ", [ship.top_left_cor, ship.bot_right_cor])
        for bullet in list_bullets:
            for ship in client.ship_list:
                print("bullet >>> ", bullet)
                if bullet[0] in range(ship.top_left_cor[0], ship.bot_right_cor[0] + 1) and bullet[1] in range(ship.top_left_cor[1], ship.bot_right_cor[1] + 1):
                    destroyed_ships.append(ship)
                    client.ship_list.remove(ship)
        return destroyed_ships, "Updated successfully"

    def check_win(self):
        for client in self.client_list:
            if len(client.ship_list) == 0:
                self.status = "finished"
                enemy = self.get_enemy(client.client_id)
                return enemy.client_id
        return None

    def change_turn(self, client_id):
        if self.status == "playing":
            self.current_turn["index"] += 1
        self.current_turn["client_id"] = client_id
        self.current_turn["list_bullets"] = []
        return