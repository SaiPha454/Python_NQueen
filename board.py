
from tkinter import *

class Board(object):

    def __init__(self) -> None:
        self.board_size = 400
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("N-Queen")
        self.queens = IntVar()
        self.queens.set(8)
        self.palaces = []

        self.queen_icon = PhotoImage(file="queen_icon.png")
        self.queen_img = PhotoImage(file="queen.png")
        self.setting_img = PhotoImage(file="setting.png")

        #default timer limit is 3 minutes
        self.timer_limit_mn = 1

        self.body_frame = Frame(self.window)
        self.body_frame.grid(row=2, column=0, padx=20, pady=20)

        self.play_frame = Frame(self.body_frame)
        self.play_frame.grid(row=0, column=0)

        self.control_frame = Frame(self.body_frame, 
                          width=self.board_size,
                          )

        self.control_frame.grid(row=0, column=1, sticky="nsew")

        self.queen_frame = Frame(self.play_frame, 
                                 width=self.board_size, 
                                 height=20,
                                 pady=20,
                                 )
        self.queen_frame.grid(row=0,column=0, rowspan=1, columnspan=6)

