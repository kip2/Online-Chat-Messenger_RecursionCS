import socket
import sys
import threading

# const request
# header用定数
CREATE_ROOM = 0
REQUEST_ROOM_LIST = 1
REQUEST_LOG_FILE = 2
ENTER_ROOM = 3
SEND_MESSAGE = 4
EXIT_MESSAGE = 5

# IP address
server_address = "127.0.0.1"
# Port
server_port = 9001


# def protocol_header(filename_length, json_length, data_length):
#     return filename_length.to_bytes(1, "big") + json_length.to_bytes(3,"big") + data_length.to_bytes(4,"big")

def protocol_header(client_request, message_length,data_length):
    return client_request.to_bytes(1, "big") + message_length.to_bytes(3,"big") + data_length.to_bytes(4, "big")

def create_exit_header():
    return EXIT_MESSAGE.to_bytes(1,"big") + int(0).to_bytes(3,"big") + int(0).to_bytes(4,"big")

# データ受信関数
def recv_data(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data == b"":
                break
            print(data.decode("utf-8"))
        except ConnectionResetError:
            break
        except OSError as e:
            if e.errno == 9:
                break
    sock.close()

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    # データ受信をサブスレッドで実行
    thread = threading.Thread(target=recv_data, args=(sock,))
    thread.start()

    # header送信テスト中
    header = protocol_header(CREATE_ROOM, 0, 0)

    sock.send(header)

    # print("room create!")
    # print("Enter Room Name > ")
    # print("Enter the maximum room capacity > ")

    # データ入力ループ
    while True:
        data = input("> ")
        if data == "exit":
            sock.send(data.encode("utf-8"))
            break
        else:
            try:
                sock.send(data.encode("utf-8"))
            except ConnectionResetError:
                break
    sock.shutdown(socket.SHUT_RD)
    sock.close()
    

if __name__ == "__main__":
    start_client()
