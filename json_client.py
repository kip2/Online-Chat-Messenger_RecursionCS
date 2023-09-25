from lib.tcp_client import *
import os

import lib

# todo: test用後で消す
# from lib.tcp_server import *
# sever = TCP_Server(JSON_SERVER_PORT)

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
        # todo: 後でfilepathの受け渡しについて考慮すること
        filepath = JSON_DIRECTORY_PATH + "/" +  "room_list.json"

        with open(filepath, "rb") as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0,0)

            if filesize > pow(2, 32):
                raise Exception("File must be below 2GB.")

            filename = os.path.basename(f.name)

            # todo: encodeのCHARACTER CODEを定数にする
            filename_bits = filename.encode("utf-8")

            header = protocol_header(len(filename_bits), 0, filesize)

            c.sock.send(header)
            c.sock.send(filename_bits)

            data = f.read(4096)
            while data:
                print("Sending...")
                c.sock.send(data)
                data = f.read(4096)
    # todo: これも消す
    print("Closing socket")

if __name__ == "__main__":
    json_client()
    pass
