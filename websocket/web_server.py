import asyncio
import json
import sys

import websockets

sys.path.append("/home/chien/PycharmProjects/python_network_programming"
                "/warship")

from controller import (LIST_CONTROLLER, check_client_identity, find_match,
                        handle_package_hello)
from package import pkt_error, pkt_wait

ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 17618
game_name = "warship"
game_des = "none"
game_author = "wda"
championship_server_host = "104.194.240.16"
championship_server_port = 8881



# create handler for each connection
List_websocket = []

async def send_web(data):
    async with websockets.connect("ws://{}:{}".format(
            championship_server_host, championship_server_port)) as websocket:
        print("send data: ",data)
        await websocket.send(data)
    msg = await websocket.recv()
    print("recv data",msg)

async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        data_recv = json.loads(data)
        for (type, controller) in LIST_CONTROLLER:
            if type == data_recv["type"]:
                await controller(websocket, data_recv)
        # TO DO : ...


def run_server():
    start_server = websockets.serve(handler, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)

    asyncio.get_event_loop().run_forever()

run_server()