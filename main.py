import socket
import threading
import queue
from osero import Osero
import logging

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
# サーバー関連
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 12345
argument = (host, port)
sock.bind(argument)
sock.listen()
q = queue.Queue()
clients = []

# オセロ関連
osero = Osero()
total_player = 2
count = 1
room = []
# 盤面の生成
osero.make_board()
# バリアインスタンスを作る
lock = threading.Lock()
barrier = threading.Barrier(total_player, timeout=5)

# 対戦ルームオセロ処理
def match():
    logging.debug('start')
    # 終了までループ
    for i in range(2):
        room.append(q.get())
        print(room[i])
    name = 1
    while (osero.flag_fin()):
        name = int(-0.5 * Osero.player + 0.5)
        print("player:{}".format(Osero.player))
        room[0].send((str(0) + str(name) + "\n" + str(osero.board)).encode())
        room[1].send((str(1) + str(name) + "\n" + str(osero.board)).encode())

        #クライアント
        i = room[name].recv(1024)
        j = room[name].recv(1024)
        i = int(i.decode())
        j = int(j.decode())
        print("i:{} j:{}".format(i, j))
        # 石を配置する
        osero.place_stn(i, j)
        # 手番を入れ替える
        Osero.player *= -1


    # 盤面の表示
    print(osero.board)
    # 勝利判定
    osero.judge_board()


def roby(connection, address):
    logging.debug('start')
    print('address:{}'.format(address))
    try:
        if not barrier.broken:
            start = barrier.wait()
            q.put(connection)
            # バリアとおったやつだけ実行
            if start == 0:
                m = threading.Thread(target=match, args=(), daemon=True)
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

