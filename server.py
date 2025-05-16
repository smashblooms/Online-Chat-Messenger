import socket
from collections import defaultdict

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000

active_clients = defaultdict(str)


def handle_message(data, addr):
    try:
        message_type = data[0]

        if message_type == 0x01:  # JOINメッセージ
            username = data[1:].decode("utf-8")
            active_clients[addr] = username
            return f"* {username}が参加しました\n--------------------------------"

        elif message_type == 0x02:  # 通常メッセージ
            username = active_clients.get(addr, "Unknown")
            message = data[1:].decode("utf-8")
            return f"{username}> {message}"

    except Exception as e:
        print(f"エラー: {e}")
    return None


def broadcast(sock, message, exclude_addr=None):
    if not message:
        return

    encoded = message.encode("utf-8")
    for client_addr in active_clients:
        if client_addr == exclude_addr:
            continue
        try:
            sock.sendto(encoded, client_addr)
        except:
            pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print("サーバーが起動しました")
    print("--------------------------------")

    while True:
        data, addr = sock.recvfrom(4096)
        formatted = handle_message(data, addr)
        if formatted:
            broadcast(sock, formatted, addr)  # 送信元を除外
            print(formatted)  # サーバーコンソールに表示


if __name__ == "__main__":
    main()
