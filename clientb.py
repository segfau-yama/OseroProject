# クライアントを作成

import socket
import re

p = -1

def replace(board):
    replace_board = [rep.replace("0", "＊").replace("2", "■").replace("-1", "●").replace("1", "○") for rep in board]
    return replace_board

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('127.0.0.1', 12345))
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    while True:
        data = s.recv(1024)
        data_d = data.decode()
        data_d = data_d.split(",")
        flag = int(data_d[0])
        if flag == 5:
            my = int(data_d[1])
            now_player = int(data_d[2])
            #print("now_player:{}".format(now_player))
            #print("my:{}".format(my))
            osero_board = data_d[3:]
            re_board = replace(osero_board)
            for i in range(100):
                if i%10 == 0 and i != 0:
                    print()
                print(re_board[i] + "　", end='')
            print()
        elif flag == 3:
            now_player = int(data_d[1])
            #print("now_player:{}".format(now_player))
            #print("my:{}".format(my))
            osero_board = data_d[2:]
            re_board = replace(osero_board)
            for i in range(100):
                if i % 10 == 0 and i != 0:
                    print()
                print(re_board[i] + "　", end='')
            print()
        elif flag == 4:
            winner = int(data_d[1])
            if winner == 1:
                print("先手の勝ち")
            elif winner == 0:
                print("後手の勝ち")
            else:
                print("引き分け")
            s.close()
            s.close()
            break
        # サーバにメッセージを送る
        if my == now_player or flag == 6:
            while True:
                print("あなたの番です。")
                i = input("i:")
                j = input("j:")
                if re.fullmatch("[1-8]", i) and re.fullmatch("[1-8]", j):
                    break
                else:
                    print("場所が違います。")
            s.send(str(i).encode())
            s.send(str(j).encode())
        else:
            print("思考中・・・")