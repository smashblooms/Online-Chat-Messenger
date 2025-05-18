import socket
import threading
from datetime import datetime, timedelta
import time

# クライアントが一定時間メッセージを送信していない場合に、サーバーがクライアントを切断する時間
TIME_LIMIT = 120

# サーバーが定期的にクライアントの最終送信時間を確認するための定数
CHECK_INTERVAL = 10


def add_client(data, client_list, client_address):
    username_len = data[0]
    username = data[1 : username_len + 1].decode("utf-8")

    client_list.append({"address": client_address, "last_sent_at": datetime.now()})
    print(f"\n新しいユーザーが接続しました: {username} {client_address}")
    print("--------------------------------------------------------")


def receive_message(data, client_address, client_list):
    username_len = data[0]
    username = data[1 : username_len + 1].decode("utf-8")
    message = data[username_len + 1 :].decode("utf-8")

    for client in client_list:
        if client["address"] == client_address:
            client["last_sent_at"] = datetime.now()
            break

    print(f"username: {username} message: {message} from {client_address}")


def send_message(sock, data, client_list, client_address):
    for client in client_list:
        if client["address"] != client_address:
            sock.sendto(data, client["address"])


def remove_client(client_list, sock):
    while True:
        now = datetime.now()
        for client in client_list:
            print(f"接続しているクライアント: {client['address']}")
            if now - client["last_sent_at"] > timedelta(seconds=TIME_LIMIT):
                print(f"クライアントが切断されました: {client['address']}")
                dissconnect = b"DISCONNECT"
                sock.sendto(dissconnect, client["address"])
                client_list.remove(client)

        time.sleep(CHECK_INTERVAL)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ("127.0.0.1", 8000)
    sock.bind(server_address)

    client_list = []

    print("サーバーが起動しました")
    print(f"サーバーアドレス: {server_address}")
    print("-------------------------------------")

    thread = threading.Thread(
        target=remove_client,
        args=(
            client_list,
            sock,
        ),
    )
    thread.start()

    while True:
        data, client_address = sock.recvfrom(4096)

        # クライアントを新規登録した後、途中でループを抜け、上に戻る
        if client_address not in [client["address"] for client in client_list]:
            add_client(data, client_list, client_address)
            continue

        receive_message(data, client_address, client_list)

        send_message(sock, data, client_list, client_address)


if __name__ == "__main__":
    main()
