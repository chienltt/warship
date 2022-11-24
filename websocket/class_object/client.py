from warship.websocket.class_object.ship import Ship


class Client:
    def __init__(self, client_id, secret, websocket):
        self.client_id = client_id
        self.secret = secret
        self.ship_list = []
        self.is_place_ship = False
        self.connection = websocket

    def place_list_ship(self, list_ship):
        if self.is_place_ship:
            return False, "Client has already placed ship"
        for ship in list_ship:
            if not self.place_ship(ship[0], ship[1]):
                return False, "Invalid ship locations"
        self.is_place_ship = True
        return True, "Success"

    def place_ship(self, top_left_cor, bot_right_cor):
        type = Ship.chec_coor(top_left_cor, bot_right_cor)
        if type == 0:
            return False
        new_ship = Ship(top_left_cor, bot_right_cor, type)
        if not self.check_duplicate_locate(new_ship):
            return False
        self.ship_list.append(new_ship)
        return True

    def check_duplicate_locate(self, new_ship):
        for row in range(new_ship.top_left_cor[0],
                         new_ship.bot_right_cor[0] + 1):
            for col in range(new_ship.top_left_cor[1],
                             new_ship.bot_right_cor[1] + 1):
                for ship in self.ship_list:
                    if row in range(ship.top_left_cor[0],
                                    ship.bot_right_cor[0] + 1) and col in \
                            range(ship.top_left_cor[1],
                                  ship.bot_right_cor[1] + 1):
                        return False
        return True

    def get_num_bullets(self):
        sum = 0
        for ship in self.ship_list:
            sum = sum + ship.type
        return sum