# socketをインポート
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000


def input_message(user_name):
    message = input(f"{user_name}> ")
    return message


def send_message(client_socket, message):
    client_socket.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))
    print("メッセージの送信完了")


def receive_message(client_socket):
    server_message = client_socket.recv(4096)
    print(server_message.decode("utf-8"))


def main():
    # ソケットを作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ユーザーネームを入力
    user_name = input("ユーザーネームを入力: ")

    while True:
        # メッセージを入力
        message = input_message(user_name)

        # メッセージを送信
        send_message(client_socket, message)

        # サーバからの応答を受信
        receive_message(client_socket)


if __name__ == "__main__":
    main()
