import socket
import threading
import sys


def receive_message(sock):
    while True:
        data, client_address = sock.recvfrom(4096)

        if data == b"DISCONNECT":
            print("\nサーバーとの接続が切れました")
            print("チャットを終了します")
            sock.close()
            break

        username_len = data[0]
        username = data[1 : username_len + 1].decode("utf-8")
        message = data[username_len + 1 :].decode("utf-8")

        print(f"\r{username}: {message}\nYou> ", end="", flush=True)


def send_join(sock, server_address, username):
    username_len = len(username)
    username_len_bytes = username_len.to_bytes(1, "big")

    packet = username_len_bytes + (username).encode("utf-8")
    sock.sendto(packet, server_address)


def send_message(sock, server_address, username, message):
    username_len = len(username)
    username_len_bytes = username_len.to_bytes(1, "big")

    packet = username_len_bytes + (username + message).encode("utf-8")
    sock.sendto(packet, server_address)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ("127.0.0.1", 8000)

    # ユーザー登録
    username = input("ユーザーネームを入力してください: ")
    send_join(sock, server_address, username)

    thread = threading.Thread(target=receive_message, args=(sock,))
    thread.start()

    while True:
        message = input(f"You> ")

        send_message(sock, server_address, username, message)


if __name__ == "__main__":
    main()
