# const request header
CREATE_ROOM = 1
REQUEST_ROOM_LIST = 2
REQUEST_LOG_FILE = 3
ENTER_ROOM = 4
SEND_MESSAGE = 5
CLIENT_EXIT_MESSAGE = 6
EXIT_MESSAGE = 0

def create_header(client_request, message_length,data_length):
    return client_request.to_bytes(1, "big") + message_length.to_bytes(3,"big") + data_length.to_bytes(4, "big")
