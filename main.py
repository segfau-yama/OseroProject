from osero import Osero

osero = Osero()

#盤面の生成
osero.make_board()
#終了までループ
while(osero.flag_fin()):
    # 盤面の表示
    print(osero.board)
    # 手番の表示
    osero.show_player()

    while True:
        i = int(input("i:"))
        j = int(input("j:"))
        # 石の場所が正しければループを抜ける
        if osero.check_plc(i, j):
            break

    # 石を配置する
    osero.place_stn(i, j)
    # 手番を入れ替える
    Osero.player *= -1

#盤面の表示
print(osero.board)
#勝利判定
osero.judge_board()
