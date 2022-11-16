ngrok_ip = "0.tcp.ap.ngrok.io"
ngrok_port = 17618
game_name = "warship"
game_des = "none"
game_author = "wda"
championship_server_host = "104.194.240.16"
championship_server_port = 8881

PKG_HELLO = (1).to_bytes(4, 'little') + (len(ngrok_ip)).to_bytes(4, 'little')
+ bytes(ngrok_ip, 'utf-8') + ngrok_port.to_bytes(4, 'little') + (
    len(game_name)).to_bytes(4, 'little')
+ bytes(game_name, 'utf-8') + (
    len(game_des)).to_bytes(4, 'little')
+ bytes(game_des, 'utf-8') + (
    len(game_author)).to_bytes(4, 'little')
+ bytes(game_author, 'utf-8')


def get_pkg_hello(data):
    return {
        "abc"
    }


