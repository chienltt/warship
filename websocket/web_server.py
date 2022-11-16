import asyncio

import websockets

ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 17618
game_name = "warship"
game_des = "none"
game_author = "wda"
championship_server_host = "104.194.240.16"
championship_server_port = 8881


# create handler for each connection

async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        reply = f"Data recieved as:  {data}!"
        print("okok", reply)
        print("okok1", type(reply))
        # await websocket.send(
        #     (1).to_bytes(4, 'little') + (len(ngrok_ip)).to_bytes(4, 'little')
        #     + bytes(ngrok_ip, 'utf-8') + ngrok_port.to_bytes(4, 'little') + (
        #         len(game_name)).to_bytes(4, 'little')
        #     + bytes(game_name, 'utf-8') + (
        #         len(game_des)).to_bytes(4, 'little')
        #     + bytes(game_des, 'utf-8') + (
        #         len(game_author)).to_bytes(4, 'little')
        #     + bytes(game_author, 'utf-8'))
        await websocket.send("1/40/24/chien dat hoang "
                             "hung/658/45/awdawdawdawdawd")


start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
