import socket
import threading

IPADDR = "127.0.0.1"
PORT = 49152

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))

def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3,"big") + data_length.to_bytes(4,"big")

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
    # sock.shutdown(socket.SHUT_RDWR)
    sock.close()

# データ受信をサブスレッドで実行
thread = threading.Thread(target=recv_data, args=(sock,))
thread.start()

# データ入力ループ
while True:
    data = input("> ")
    if data == "exit":
        break
    else:
        try:
            sock.send(data.encode("utf-8"))
        except ConnectionResetError:
            break

sock.shutdown(socket.SHUT_RD)
sock.close()