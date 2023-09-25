from lib.tcp_client import *

import lib

# todo: test用後で消す
from lib.tcp_server import *
sever = TCP_Server(JSON_SERVER_PORT)

# network socket type
NETWORK_SOCKET_TYPE = lib._address_config.NETWORK_SOCKET_TYPE 
# server address
SERVER_ADDRESS = lib._address_config.SERVER_ADDRESS 
# server port
JSON_SERVER_PORT = lib._address_config.JSON_SERVER_PORT

# json save directory
JSON_DIRECTORY_PATH = "json"

def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3,"big") + data_length.to_bytes(4,"big")

def json_client():
    with TCP_Client(SERVER_ADDRESS, JSON_SERVER_PORT) as c:
        pass
    print("test")

if __name__ == "__main__":
    json_client()
    pass
