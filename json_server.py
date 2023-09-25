import os
from lib.tcp_server import *

import lib

# network socket type
NETWORK_SOCKET_TYPE = lib._address_config.NETWORK_SOCKET_TYPE 
# server address
SERVER_ADDRESS = lib._address_config.SERVER_ADDRESS 
# server port
JSON_SERVER_PORT = lib._address_config.JSON_SERVER_PORT

# json save directory
JSON_DIRECTORY_PATH = "json"

def json_server():
    with TCP_Server(JSON_SERVER_PORT) as s:
        sock, addr, port = s.sock, s.addr, s.port

        # create temp directory
        create_temp_directory()

    print("test")
        
def create_temp_directory():
    """
        json受け渡しをするtempフォルダを作成する
    """
    if not os.path.exists(JSON_DIRECTORY_PATH):
        os.makedirs(JSON_DIRECTORY_PATH)

if __name__ == "__main__":
    print("Hello")
    json_server()
    pass