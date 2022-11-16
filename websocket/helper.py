import math


def get_type(data):
    return int.from_bytes(data[0:3], "little")


def get_len(data):
    return int.from_bytes(data[4:7], "little")


def execute(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        no1 = (-b + math.sqrt(delta)) / (2 * a)
        no2 = (-b - math.sqrt(delta)) / (2 * a)
        return {
            "So nghiem": 2,
            "Nghiem lon": no1,
            "Nghiem nho": no2
        }
    if delta == 0:
        no = (-b / (2 * a))
        return {
            "So nghiem": 1,
            "Nghiem duy nhat": no,
        }

    if delta < 0:
        return {
            "So nghiem": 0,
        }
