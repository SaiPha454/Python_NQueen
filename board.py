from tkinter import *
from tkinter import PhotoImage
from utilis import NButton, Welcome, NCanvas, MenuBar, Queens, ControlPanel


class Game (Welcome, NCanvas, MenuBar, Queens, ControlPanel):

    def __init__(self, queens) :

        self.queens = queens
        self.board_size = 400
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("N-Qeen")

        self.queen_img = PhotoImage(file="queen.png")
        self.setting_img = PhotoImage(file="setting.png")

        
        self.body_frame = Frame(self.window)
        self.body_frame.grid(row=1, column=0, padx=20, pady=20)

        self.play_frame = Frame(self.body_frame)
        self.play_frame.grid(row=0, column=0)

        self.control_frame = Frame(self.body_frame, 
                          width=self.board_size,
                          )


        self.control_frame.grid(row=0, column=1, sticky="nsew")

        self.queen_frame = Frame(self.play_frame, 
                                 width=self.board_size, 
                                 height=20,
                                 pady=20
                                 )
        self.queen_frame.grid(row=0,column=0)


        Welcome.__init__(self)
        MenuBar.__init__(self)

        NCanvas.__init__(self,self.play_frame, self.board_size)
        Queens.__init__(self)
        ControlPanel.__init__(self)

        self.create_menubar()
        self.draw_board(self.queens)
        self.render_queens()
        self.create_control_panel()


gameboard = Game(8)
gameboard.window.mainloop()