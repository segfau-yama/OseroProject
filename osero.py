class Osero:
    # 盤面
    board = [[0 for i in range(10)] for j in range(10)]
    # 手番
    player = -1
    # 盤面の生成
    def make_board(self):
        self.board = [[0 for i in range(10)] for j in range(10)]
        for i in range(0, 10):
            self.board[0][i] = 2
            self.board[9][i] = 2
            self.board[i][0] = 2
            self.board[i][9] = 2
        self.board[4][4] = 1
        self.board[5][5] = 1
        self.board[4][5] = -1
        self.board[5][4] = -1

    # 手番の表示
    def show_player(self):
        if self.player == -1:
            return "先手(黒)の手番です"
        elif self.player == 1:
            return "後手(白)の手番です"
        else:
            return "error!"

    # マスの探索
    def check_dir(self, i, j, dir_i, dir_j):
        times = 1
        while (self.board[i+dir_i*times][j+dir_j*times] == self.player*-1):
            times += 1
        if (self.board[i+dir_i*times][j+dir_j*times] == self.player):
            return times - 1
        return 0

    # 特定の場所に置くことができるか判定
    def check_plc(self, i, j):
        if self.board[i][j] == 0:
            for dir_i in range(-1, 2):
                for dir_j in range(-1, 2):
                    if self.check_dir(i, j, dir_i, dir_j):
                        return True
        return False

    # 終了判定
    def flag_fin(self):
        for i in range(1, 9):
            for j in range(1, 9):
                if self.check_plc(i, j):
                    return True
        self.player *= -1
        for i in range(1, 9):
            for j in range(1, 9):
                if self.check_plc(i, j):
                    print("置く場所がないためPlayerを変更しました")
                    return True
        return False

    # 石を配置する
    def place_stn(self, i, j):
        for dir_i in range(-1, 2):
            for dir_j in range(-1, 2):
                change_num = self.check_dir(i, j, dir_i, dir_j)
                for k in range(1, change_num + 1):
                    self.board[i + dir_i * k][j + dir_j * k] = self.player
        self.board[i][j] = self.player

    # 勝敗判定
    def judge_board(self):
        count_b = 0
        count_w = 0
        print(self.board)
        for i in range(1, 9):
            for j in range(1, 9):
                if self.board[i][j] == -1:
                    count_b += 1
                elif self.board[i][j] == 1:
                    count_w += 1
        print("黒:{} 白:{}".format(count_b, count_w))
        if count_b > count_w:
            print("黒の勝利")
            return 4, 0, count_b, count_w
        elif count_w > count_b:
            print("白の勝利")
            return 4, 1, count_b, count_w
        else:
            print("引き分け")
            return 4, 2, count_b, count_w

