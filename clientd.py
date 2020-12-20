# クライアントを作成

import socket
import threading

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('127.0.0.1', 12345))
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    while True:
        data = s.recv(1024)
        print(data.decode())
        # サーバにメッセージを送る
        i = input("i:")
        j = input("j:")
        s.send(i.encode())
        s.send(j.encode())

