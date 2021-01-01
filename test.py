# -*- coding:utf-8 -*-
import tkinter

# メインウィンドウ作成
app = tkinter.Tk()
app.geometry("600x400")

def pushed(b):
    b["text"] = "●"
def osero_board():
    # 青色のキャンバス作成
    button1 = tkinter.Button(
        app,
        bg="green",
        command=lambda: pushed(button1),
        text="〇",
        font=("", 20)

    )
    return button1
def osero_wall():
    # 青色のキャンバス作成
    canvas1 = tkinter.Canvas(
        app,
        width=60,
        height=60,
        bg="black"
    )
    return canvas1

for i in range(10):
    for j in range(10):
        # ウィジェットの配置
        if i == 0 or j == 0 or i == 9 or j == 9:
            osero_wall().grid(
                column=i,
                row=j
            )
        else:
            osero_board().grid(
                column=i,
                row=j,
                sticky=tkinter.NE+tkinter.NW+tkinter.S
            )

# メインループ
app.mainloop()