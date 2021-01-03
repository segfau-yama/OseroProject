# クライアントを作成

import socket
import threading
p = -1
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('127.0.0.1', 12345))
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    while True:
        print("aaaa")
        data = s.recv(1024)
        data_d = data.decode()
        print(data_d)
        try:
            my = int(data_d[0])
            now_player = int(data_d[1])
            print("now_player:{}".format(now_player))
            print("my:{}".format(my))
            osero_board = data_d
        except:
            print("error")

        # サーバにメッセージを送る
        if my == now_player:
            while True:
                i = input("i:")
                j = input("j:")
                if str(i+j).isdecimal() and 1 <= int(i) <= 8 and 1 <= int(j) <= 8:
                    break
            s.send(str(i).encode())
            s.send(str(j).encode())
        else:
            print("wait....")