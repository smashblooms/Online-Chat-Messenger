import socket


SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000


def receive_message(server_socket):
    client_message, client_address = server_socket.recvfrom(4096)
    client_message = client_message.decode("utf-8")
    return client_message, client_address


def send_message(server_socket, client_address, message):
    server_socket.sendto(message.encode("utf-8"), client_address)
    print("--------------------------------\n")


def main():
    # ソケットを作成する
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 待ち受けに使用するIPアドレスとポート番号を指定
    server_socket.bind((SERVER_IP, SERVER_PORT))

    while True:
        # クライアントからのメッセージを受信する
        client_message, client_address = receive_message(server_socket)

        # クライアントからのメッセージを表示する
        print(f"{client_address}からのメッセージを受信しました.")
        print(f"メッセージは: [ {client_message} ].")

        # クライアントに応答する
        send_message(server_socket, client_address, client_message)


if __name__ == "__main__":
    main()
