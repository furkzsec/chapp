import socket
import threading
import requests
from colorama import Fore

header = 64
ip = socket.gethostbyname(socket.gethostname())
port = 1337
addr = (ip,port)
format = "utf-8"
ks = "///**//"
disconnect_message = "DISCONNECT_SERVER_CODE"
username_message = "EXAMPLE_APP_USERNAME_FIELD"

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)

    users = []

    def send_message(to_username, msg):
        for user in users:
            if user['username'] == to_username:
                connection = user["connection"]
                msg = msg.encode(format)
                msg_lenth = str(len(msg)).encode(format)
                head = msg_lenth + b'' * (header - len(msg))
                connection.send(head)
                connection.send(msg)
                break

    def delete_connection(username):
        for (idx , user) in enumerate(users):
            if user['username'] == username:
                del users[idx]

    def handle_client(conn, addr):
        print("[New Connection] {addr} connected...")
        connected = True
        while connected:
            max_lenth = conn.recv(header).decode(format)
            if max_lenth:
                max_lenth= int(max_lenth)
                msg = conn.recv(max_lenth).decode(format)
                write_active_connections()
                messages = msg.split(ks)
                username = messages[0]
                print(f"{users}")
                if username_message in msg:
                    data = {
                        "username": username,
                        "connection": conn
                    }
                    users.append(data)
                    continue

                if disconnect_message in msg:
                    print("[Disconnect] Disconnecting from server")
                    delete_connection(username)
                    connected = False
                if len(messages) > 2:
                    print(f"[{addr}] message will send -> {msg}")
                    to_username = messages[1]
                    send_message(to_username, msg)
        conn.close()
        write_active_connections()

    def write_active_connections():
        print(f"Active Connection Count is {threading.activeCount()}")
    
    def start():
        server.listen()
        print(f"[Listening] Server is Listening now on {ip}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            write_active_connections()

    if __name__ == "__main__":
        print("[Starting] Socket Server is starting... Stand By")
        start()

except:
    print(f"{Fore.RESET}İnternet {Fore.RED}Yok{Fore.RESET}")
