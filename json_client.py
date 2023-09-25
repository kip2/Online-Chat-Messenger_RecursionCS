from lib.tcp_client import *

import lib

def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3,"big") + data_length.to_bytes(4,"big")

def json_client():
    pass

if __name__ == "__main__":
    json_client()
    pass
