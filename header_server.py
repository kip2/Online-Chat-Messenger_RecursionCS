import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

def start_server():
    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            pass
        except Exception as e:
            print("Error: " + str(e))
        finally:
            print("Closing current connection")
            connection.close()
            break