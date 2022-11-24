import asyncio
import json
import sys
import websockets

sys.path.append("/home/chien/PycharmProjects/python_network_programming"
                "/warship")

from warship.websocket.controller import find_match, handle_package_hello, \
    check_client_identity
from warship.websocket.package import pkt_error, pkt_wait

ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 17618
game_name = "warship"
game_des = "none"
game_author = "wda"
championship_server_host = "104.194.240.16"
championship_server_port = 8881



# create handler for each connection
List_websocket = []


async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        if data['type'] == 0:
            await handle_package_hello(websocket, data)
        else:
            ok = check_client_identity(data)
            if not ok:
                await websocket.send(pkt_error("invalid client information"))
        # TO DO : ...


def run_server():
    start_server = websockets.serve(handler, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)

    asyncio.get_event_loop().run_forever()
