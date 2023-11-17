from tkinter import *
from utilis import  NCanvas, MenuBar, Queens, ControlPanel, Level_Label

class Game (NCanvas, MenuBar, Queens, ControlPanel, Level_Label):

    def __init__(self) :

        Level_Label.__init__(self)
        NCanvas.__init__(self)
        Queens.__init__(self)
        ControlPanel.__init__(self)
        MenuBar.__init__(self)

        self.create_menubar()
        self.draw_board()
        self.render_queens()
        self.create_control_panel()
        self.render_level_label()