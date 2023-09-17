# const request header
CREATE_ROOM = 0
REQUEST_ROOM_LIST = 1
REQUEST_LOG_FILE = 2
ENTER_ROOM = 3
SEND_MESSAGE = 4
CLIENT_EXIT_MESSAGE = 5
EXIT_MESSAGE = 9

def create_header(client_request, message_length,data_length):
    return client_request.to_bytes(1, "big") + message_length.to_bytes(3,"big") + data_length.to_bytes(4, "big")
