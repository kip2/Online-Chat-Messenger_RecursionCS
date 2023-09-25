import os

import lib
from lib.tcp_client import *
from lib._header import *

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
# todo: recieve test用
# JSON_DIRECTORY_PATH = "temp"

# header size
HEADER_SIZE = JSON_HEADER_SIZE


def recieve_json_client():
    with TCP_Client(SERVER_ADDRESS, JSON_SERVER_PORT) as c:
        try:
            header = c.sock.recv(HEADER_SIZE)

            # header のパース
            filename_length, json_length, data_length = json_header_parsing(header)
            stream_rate = 4096

            filename = c.sock.recv(filename_length).decode(CHARA_CODE)

            if json_length != 0:
                raise Exception("JSON data is not currently supported.")
            if data_length == 0:
                raise Exception("No data to read from client.")

            with open(os.path.join(JSON_DIRECTORY_PATH, filename), "wb+") as f:

                while data_length > 0:
                    data = c.sock.recv(data_length if data_length <= stream_rate else stream_rate)
                    f.write(data)
                    print(f"recieved {len(data)} bytes")
                    data_length -= len(data)
                    print(data_length)

            print("Finished downloading the file from client.")
        except Exception as e:
            print("Error: " + str(e))

def send_json_client(filepath):
    with TCP_Client(SERVER_ADDRESS, JSON_SERVER_PORT) as c:

        with open(filepath, "rb") as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0,0)

            if filesize > pow(2, 32):
                raise Exception("File must be below 2GB.")

            filename = os.path.basename(f.name)

            filename_bits = filename.encode(CHARA_CODE)

            header = create_send_json_header(len(filename_bits), 0, filesize)

            c.sock.send(header)
            c.sock.send(filename_bits)

            data = f.read(4096)
            while data:
                print("Sending...")
                c.sock.send(data)
                data = f.read(4096)

if __name__ == "__main__":
    # filepath = JSON_DIRECTORY_PATH + "/" +  "room_list.json"
    # send_json_client(filepath)
    recieve_json_client()
    pass

