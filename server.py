import socket

import websockets

import asyncio

from helper import get_type, get_len, execute

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65430  # Port to listen on (non-privileged ports are > 1023)
ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 15376
game_name = "battle ship"
game_des = "none"
game_author = "something very secret"
championship_server_host = "104.194.240.16"
championship_server_port = "8881"


async def send_data_to_championship(data):
    async with websockets.connect("ws://{}:{}".format(
            championship_server_host, championship_server_port)) as websocket:
        await websocket.send(data)
    msg = await websocket.recv()


# create handler for each connection

# async def handler(websocket, path):
#     data = await websocket.recv()
#     print("okok",data)
#     reply = f"Data recieved as:  {data}!"
#
#     await websocket.send(reply)
#
#
# start_server = websockets.serve(handler, "127.0.0.1", 65430)
#
# asyncio.get_event_loop().run_until_complete(start_server)
#
# asyncio.get_event_loop().run_forever()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            # Mở kết nối
            print(f"ket noi voi dia chi: {addr}")
            while True:
                # Lắng nghe gói tin PKT_HELLO
                data = conn.recv(1024)
                print("okok", data)
                asyncio.run(
                    send_data_to_championship((1).to_bytes(4, 'little')))

    # connect championship_server
    # send_data_to_championship(
    #     (1).to_bytes(4, 'little') + (len(ngrok_ip)).to_bytes(4, 'little')
    #     + bytes(ngrok_ip, 'utf-8') + ngrok_port.to_bytes(4, 'little') + (
    #         len(game_name)).to_bytes(4, 'little')
    #     + bytes(game_name, 'utf-8') + (
    #         len(game_des)).to_bytes(4, 'little')
    #     + bytes(game_des, 'utf-8') + (
    #         len(game_author)).to_bytes(4, 'little')
    #     + bytes(game_author, 'utf-8'))
    while True:
        conn, addr = s.accept()
        with conn:
            # Mở kết nối
            print(f"ket noi voi dia chi: {addr}")
            while True:
                # Lắng nghe gói tin PKT_HELLO
                data = conn.recv(1024)
                print("okok", data)
                asyncio.run(
                    send_data_to_championship((1).to_bytes(4, 'little')))
