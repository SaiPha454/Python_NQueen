from tkinter import *
from utilis import   ConfigurationBar

class App (ConfigurationBar):

    def __init__(self) :

        super().__init__()
        
    def start(self):

        self.render_level_label()
        self.create_menubar()
        self.create_canvas()
        self.draw_board()
        self.render_queens()
        self.create_control_panel()
        self.window.mainloop()

App().start()