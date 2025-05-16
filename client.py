import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000


def receive_messages(sock):
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            print(f"\r{data.decode('utf-8')}\nYou: ", end="", flush=True)
        except:
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 初期登録処理
    username = input("ユーザー名を入力: ")
    join_packet = bytes([0x01]) + username.encode("utf-8")
    sock.sendto(join_packet, (SERVER_IP, SERVER_PORT))

    # 受信スレッド開始
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        message = input("You: ")
        packet = bytes([0x02]) + message.encode("utf-8")
        sock.sendto(packet, (SERVER_IP, SERVER_PORT))


if __name__ == "__main__":
    main()
