import socket
import os

# const request
# header用定数
CREATE_ROOM = 0
REQUEST_ROOM_LIST = 1
REQUEST_LOG_FILE = 2
ENTER_ROOM = 3
SEND_MESSAGE = 4

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "127.0.0.1"
server_port = 9001

# client list
clients = []

def create_room():
    clients[0][0].send(b"CREATE ROOM!")
    print(clients[0][0])

def send_room_list():
    clients[0][0].send(b"CREATE ROOM!")
    
def send_log_file():
    clients[0][0].send(b"CREATE ROOM!")

def allow_enter():
    clients[0][0].send(b"CREATE ROOM!")

def receive_message():
    clients[0][0].send(b"CREATE ROOM!")

def start_server():

    print("Starting up on {} port {}".format(server_address, server_port))

    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        clients.append((connection, client_address))
        try:
            print("connection from", client_address)
            # headerの読み取り
            # header4バイト
            # clientが何を求めているかを受け取る
            header = connection.recv(8)
            # headerからの抽出
            client_request = int.from_bytes(header[:1], "big")
            message_length = int.from_bytes(header[1:3], "big")
            data_length = int.from_bytes(header[4:8], "big")

            print('Received header from client. Byte lengths: Client request {}, message length {}, Data Length {}'.format(client_request,message_length,data_length))

            # headerの種類によって動作を変える
            if client_request == CREATE_ROOM:
                create_room()
            elif client_request == REQUEST_ROOM_LIST:
                send_room_list()
            elif client_request == REQUEST_LOG_FILE:
                send_log_file()
            elif client_request == ENTER_ROOM:
                allow_enter()
            elif client_request == SEND_MESSAGE:
                receive_message()
        except Exception as e:
            print("Error: " + str(e))
        # todo 勝手にfinallyに入ってconnectを抜けている
        finally:
            print("Closing current connection")
            connection.close()
            break

if __name__ == "__main__":
    start_server()