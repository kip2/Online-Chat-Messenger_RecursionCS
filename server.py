import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

def start_server():

    dpath = "temp"
    # tempディレクトリがなければ作成する
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    print("Starting up on {} port {}".format(server_address, server_port))

    # ソケットにアドレスとポート番号を紐付け
    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            print("connection from", client_address)

            # headerの読み取り
            # headerには、ファイル名の長さ、JSONデータの長さ、クライアントから受信するデータの長さが含まれる
            header = connection.recv(8)
            # headerからの抽出
            filename_length = int.from_bytes(header[:1], "big")
            json_length = int.from_bytes(header[1:3], "big")
            data_length = int.from_bytes(header[4:8], "big")
            stream_rate = 4096

            print('Received header from client. Byte lengths: Title length {}, JSON length {}, Data Length {}'.format(filename_length, json_length,data_length))

                # 次に、クライアントからファイル名を読み取り、変数に格納します。JSONデータがある場合は、サポートされていないため、例外が発生します。受信するデータがない場合、コードは例外を発生させます。
            filename = connection.recv(filename_length).decode('utf-8')

            print('Filename: {}'.format(filename))

            if json_length != 0:
                raise Exception('JSON data is not currently supported.')
            
            if data_length == 0:
                raise Exception('No data to read from client.')
        
            # 次に、コードはクライアントから受け取ったファイル名で新しいファイルをtempフォルダに作成します。このファイルは、withステートメントを使用してバイナリモードで開かれ、write()関数を使用して、クライアントから受信したデータをファイルに書き込みます。データはrecv()関数を使用して塊単位で読み込まれ、データの塊を受信するたびにデータ長がデクリメントされます。
            # w+は終了しない場合はファイルを作成し、そうでない場合はデータを切り捨てます
            with open(os.path.join(dpath, filename),'wb+') as f:
                # すべてのデータの読み書きが終了するまで、クライアントから読み込まれます
                while data_length > 0:
                    data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                    f.write(data)
                    print('recieved {} bytes'.format(len(data)))
                    data_length -= len(data)
                    print(data_length)
        
            print('Finished downloading the file from client.')

        except Exception as e:
            print("Error: " + str(e))
        finally:
            print("Closing current connection")
            connection.close()
            break

if __name__ == "__main__":
    start_server()