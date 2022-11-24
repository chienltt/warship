# Chỉ có 3 loại tàu : tàu dài 2 rộng 2 (loại 1), tàu dài 4 rộng 2 (loại 2),
# tàu dài 6 rộng 2 (loại 3 ) => nếu tọa độ k hợp lệ thì k thể tạo tàu
class Ship:
    def __init__(self, top_left_cor, bot_right_cor, type):
        self.top_left_cor = top_left_cor
        self.bot_right_cor = bot_right_cor
        self.type = type

    @staticmethod
    def chec_coor(top_left_cor, bot_right_cor):
        if abs(top_left_cor[0] - bot_right_cor[0]) == 2:
            if abs(top_left_cor[1] - bot_right_cor[1]) == 2:
                return 1
            if abs(top_left_cor[1] - bot_right_cor[1]) == 4:
                return 2
            if abs(top_left_cor[1] - bot_right_cor[1]) == 6:
                return 3

        if abs(top_left_cor[1] - bot_right_cor[1]) == 2:
            if abs(top_left_cor[0] - bot_right_cor[0]) == 2:
                return 1
            if abs(top_left_cor[0] - bot_right_cor[0]) == 4:
                return 2
            if abs(top_left_cor[0] - bot_right_cor[0]) == 6:
                return 3
        return 0
