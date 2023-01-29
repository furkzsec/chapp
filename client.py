import socket
import requests
from colorama import Fore
from threading import Thread

HEADER = 64
ip = socket.gethostbyname(socket.gethostname())
port = 1337
addr = (ip,port)
format = "utf-8"
ks = "///**//"
disconnect_message = "DISCONNECT_SERVER_CODE"
username_message = "EXAMPLE_APP_USERNAME_FIELD"

if requests.get('https://google.com'):
    print
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

def send(msg):
    message = msg.encode(format)
    msg_lenth = str(len(message)).encode(format)
    header = msg_lenth + b'' * (HEADER - len(msg_lenth))
    client.send(header)
    client.send(message)

def main(username , to_username):
    while True:
        message = input("Message : ")
        if message == "disconnect":
            send(f"{username}{ks}{disconnect_message}")
        send(f"{username}{ks}{to_username}{ks}{message}")

def listen(username):
    connected = True
    while connected:
        max_lenth = client.recv(HEADER).decode(format)
        if max_lenth:
            max_lenth = int(max_lenth)
            msg = client.recv(max_lenth).decode(format)
            messages = msg.split(ks)
            if len(messages) > 2:
                if messages[1] == username:
                    print(f"\n{messages[0]} -->  {messages[2]}")
                else:
                    print("security issue check server.py")

if __name__ == "__main__":
    username = input("Please write your username : ")
    if username:
        send(f"{username}{ks}{username_message}")
        to_username = input(f"who you will send message : ")
        print("you can write your message and press enter\n")
        main_thread = Thread(target=main, args=(username,to_username,))
        listen_thread = Thread(target=listen, args=(username,))
        main_thread.daemon = True
        main_thread.start()
        listen_thread.start()
