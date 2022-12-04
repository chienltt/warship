import asyncio
import json
import sys

import websockets

sys.path.append("/home/chien/PycharmProjects/python_network_programming"
                "/warship")

from warship.websocket.controller import (LIST_CONTROLLER,LIST_MATCH,
                                          LIST_CLIENT,
                                          create_match,
                                          send_match_info_to_web,
                                          check_client_exist)

# from package import pkt_error, pkt_wait

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
        data_recv = json.loads(data)
        if 'action' in data_recv:
            # tournament package
            if data_recv['action'] == 1:
                if not check_client_exist(data_recv['id1'], data_recv['id2']):
                    create_match(data_recv['match'], data_recv['passwd'], data_recv[
                        'id1'], data_recv['id2'])
                    data = {
                        "result": 1,
                        "ip": "ws://0.tcp.ap.ngrok.io",
                        "port": 17899,
                        "path": "path"
                    }
                    await websocket.send(json.dumps(data))
                else:
                    data = {
                        "result": 0,
                    }
                    await websocket.send(json.dumps(data))
            if data_recv['action'] == 2:
                await send_match_info_to_web(data_recv['match'])

        else:
            for (type, controller) in LIST_CONTROLLER:
                if type == data_recv["type"]:
                    await controller(websocket, data_recv)
        # TO DO : ...


def run_server():
    start_server = websockets.serve(handler, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)

    asyncio.get_event_loop().run_forever()


run_server()
