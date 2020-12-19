import socket
import threading
import queue

#
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 55580
argument = (host, port)
sock.bind(argument)
sock.listen()
players = []

# オセロだから2人
total_player = 2

# こみ上げる怒り
# ファッキンクソバリア。引数受け取ってくれ
# バリアスレッド処理。オセロ対戦はここで実装する
def start_game():
    print('{}人になったため、ゲーム開始。'.format(total_player))
    print("loop")
    # ここにconnとaddr入れたいのにできないよ
    # オセロ未実装。チャットでテストする
    '''while True:
        try:
            # クライアント側から受信する
            res = connection.recv(4096)
            for value in players:
                if value[1][0] == address[0] and value[1][1] == address[1]:
                    print("クライアント{}:{}から{}というメッセージを受信完了".format(value[1][0], value[1][1], res))
                else:
                    value[0].send("クライアント{}:{}から{}を受信".format(value[1][0], value[1][1], res.decode()).encode("UTF-8"))
                    pass
        except Exception as e:
            print(e)
            break'''


# バリアインスタンスを作る
lock = threading.Lock()
barrier = threading.Barrier(total_player, action=start_game)

# 待機ロビー
def run(connection, address):
        # 接続完了まで10秒待つ
        try:
            if not barrier.broken:
                barrier.wait(10)
        # 例外処理。10秒待っても人が入らなかった場合、接続を終了する。
        except threading.BrokenBarrierError:
            connection.send("ゲーム開始できないため、退出しました。".encode("UTF-8"))
            connection.close()
            barrier.reset()
            print("ゲーム開始できないため、退出しました。")

# メイン
if __name__ == '__main__':
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
        thread = threading.Thread(target=run,args=(conn, addr), daemon=True)
        players.append((conn, addr))
        print('player {}さんが参加しました。'.format(len(players)))
        thread.start()

