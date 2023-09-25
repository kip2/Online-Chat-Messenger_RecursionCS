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

        # create json directory
        create_json_directory()

        while True:
            connection, client_address = sock.accept()
            try:
                print("connection from", client_address)
                header = connection.recv(8)

                filename_length = int.from_bytes(header[:1], "big")
                json_length = int.from_bytes(header[1:3], "big")
                data_length = int.from_bytes(header[4:8], "big")
                stream_rate = 4096

                # todo: 確認終われば消す
                print(f'Received header from client. Byte lengths: Title length {filename_length}, JSON length {json_length}, Data Length {data_length}')

                # todo: encodeのCHARACTER CODEを定数にする
                filename = connection.recv(filename_length).decode("utf-8")
                # todo: 確認終われば消す
                print(f"Filename: {filename}")

                if json_length != 0:
                    raise Exception("JSON data is not currently supported.")
                if data_length == 0:
                    raise Exception("No data to read from client.")

                with open(os.path.join(JSON_DIRECTORY_PATH, filename), "wb+") as f:
                    while data_length > 0:
                        data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                        f.write(data)
                        print(f"recieved {len(data)} bytes")
                        data_length -= len(data)
                        print(data_length)

                print("Finished downloading the file from client.")
                # 一回ごとに通信を終わること
                break
                
            except Exception as e:
                print("Error: " + str(e))
        
def create_json_directory():
    """
        json受け渡しをするjsonフォルダを作成する
    """
    if not os.path.exists(JSON_DIRECTORY_PATH):
        os.makedirs(JSON_DIRECTORY_PATH)

if __name__ == "__main__":
    print("Hello")
    json_server()
    pass