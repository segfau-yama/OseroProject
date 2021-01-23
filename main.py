import socket
import threading
import queue
from osero import Osero
import logging
import re

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
# サーバー関連
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 12345
argument = (host, port)
sock.bind(argument)
sock.listen()
q = queue.Queue()
clients = []
# オセロ関連
total_player = 2
# バリアインスタンスを作る
lock = threading.Lock()
barrier = threading.Barrier(total_player, timeout=20)

# 対戦ルームオセロ処理
def match():
    osero = Osero()
    # 盤面の生成
    osero.make_board()
    room = []
    now_turn = 1
    logging.debug('start')
    for i in range(2):
        room.append(q.get())
    # 終了までループ
    try:
        while (osero.flag_fin()):
            name = int(-0.5 * osero.player + 0.5)
            print("player:{}".format(osero.player))
            #カンマで区切ったデータを送信
            new_board = re.sub("\]|\[|\s","",str(osero.board))
            if now_turn == 1:
                for i in range(2):
                    room[i].send(("5," + str(i) + "," + str(name) + "," + new_board).encode())
            else:
                for i in range(2):
                    room[i].send(("3," + str(name) + "," + new_board).encode())
            # クライアントからデータを受け取る
            while True:
                i = room[name].recv(1024)
                j = room[name].recv(1024)
                i = int(i.decode())
                j = int(j.decode())
                print("i:{} j:{}".format(i, j))
                if osero.check_plc(i, j):
                    break
                else:
                    room[name].send("6".encode())
            # 石を配置する
            osero.place_stn(i, j)
            # 手番を入れ替える
            osero.player *= -1

            now_turn += 1
        # 盤面の表示
        print(osero.board)
        # 勝利判定
        judge_board = re.sub("\)|\(|\s", "", str(osero.judge_board()))
        new_board = re.sub("\]|\[|\s", "", str(osero.board))
        for i in range(2):
            print(judge_board)
            room[i].send((judge_board + "," + new_board).encode())
    except Exception as e:
        print(e)
        room[0].close()
        room[1].close()
    except room[0] == room[1]:
        print("error")

def roby(connection, address):
    logging.debug('start')
    print('address:{}'.format(address))
    try:
        if not barrier.broken:
            start = barrier.wait()
            q.put(connection)
            # バリアとおったやつだけ実行
            if start == 0:
                m = threading.Thread(target=match, daemon=True)
                m.start()
    # 送受信処理
    except threading.BrokenBarrierError:
        connection.send("ゲーム開始できないため、退出しました。".encode())
        connection.close()
        barrier.reset()
        print("ゲーム開始できないため、退出しました。")

    logging.debug('end')
# メイン
if __name__ == '__main__':
    players = []
    while True:
        # 接続要求を受信。アドレスと接続情報を取得
        try:
            conn, addr = sock.accept()
        # エラー処理。キーボード入力があればプログラムを閉じる
        except KeyboardInterrupt:
            sock.close()
            exit()
            break

        # プレイヤー追加処理。スレッドで待機ロビーを作る
        p = threading.Thread(target=roby, args=(conn, addr), name="player{}".format(len(clients)))
        players.append(p)
        p.start()

        clients.append((conn, addr))
        print('player {}さんが参加しました。'.format(len(clients)))

