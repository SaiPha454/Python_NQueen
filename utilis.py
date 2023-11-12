from tkinter import *
from tkinter import Toplevel
from tkinter.messagebox import showwarning

class NButton :

    def __init__(self, parent, text, color, callback = lambda : None ) :
        self.__parent = parent
        self.__width = 20
        self.__hieght = 2
        self.__text = text
        self.__color = color
        self.__font = ("Arial", 12)
        self.__btn = Button(self.__parent,
                           width=20, 
                           height=2, 
                           text=self.__text,
                           bg=self.__color,
                           font=("Arial", 12),
                           command=callback
                           )
        self.__btn.pack(anchor=CENTER, pady=20)
    
    def click(self) :
        print("Click Button")
    

class Welcome :

    def __init__(self, text= "Welcome To NQUEENS") :

        welcome_frame = Frame(self.window)
        welcome_frame.grid(row=0, 
                           column=0, 
                           sticky="nsew", 
                           pady=15,
                           columnspan=2
                           )
        welcome_text = Label(welcome_frame, 
                             text=text,
                             font=("Arial", 16)
                             )
        welcome_text.pack(anchor=CENTER)


class Level_Label :

    def __init__(self) :

        self.welcome_frame = Frame(self.window)
        self.welcome_frame.grid(row=1, 
                           column=0, 
                           sticky="nsew", 
                           pady=15,
                           columnspan=2
                           )

    def render_level_label(self) :
        
        self.welcome_text = Label(self.welcome_frame, 
                             text=f"Level : {self.queens.get()}",
                             font=("Arial", 14)
                             )
        self.welcome_text.pack(anchor=CENTER)

    def reset_level_label(self) :

        self.welcome_text.destroy()
        self.render_level_label()


class NCanvas :

    def __init__(self, parent, size) :
        
        self.__size = size
        self.__parent = parent

        self.create_canvas()

    def create_canvas(self) :

        canvas = Canvas(self.__parent,
                        width=self.__size, 
                        height=self.__size,
                        bg="white"
                        )
        canvas.grid(row=1, column=0)
        self.canvas = canvas

    def draw_board(self, queens) :

        

        self.create_canvas()

        box_size = self.__size/queens

        for row in range(0,queens) :

            for col in range(0, queens):
                
                x1, y1 = row * box_size, col* box_size
                x2, y2 = x1+ box_size, y1+ box_size
                color = "white"
                if (row + col) % 2 != 0 :
                    color = "gray"

                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.palaces.append(id)
        
        for i in self.palaces :
            self.canvas.tag_bind(i, "<Button-1>", self.add_queen)

    def reset_board(self) :

        self.palaces= []
        self.draw_board(self.queens.get())
        self.render_queens()
    
    def add_queen(self, event) :

        rect = event.widget.find_overlapping(event.x, event.y, event.x+5, event.y+5)
        rect = self.canvas.coords(self.canvas.find_withtag(rect[0]))
        x = rect[0] + (rect[2] - rect[0])/2
        y = rect[1] + (rect[3] - rect[1])/2
        self.canvas.create_image(x, y, image = self.queen_img, anchor =CENTER)

class LevelConfigBox :

    def __init__(self) -> None:
        self.__level = IntVar()
        self.__level.set(self.queens.get())
    
    def create_level_config_box(self):

        level_window = Toplevel(self.window)
        self.__level_window = level_window
        level_window.geometry("400x300")
        level_window.resizable(False, False)
        level_window.title("Level Setting")

        label = Label(level_window, text="Level :", font=("Arial", 14))
        label.pack(pady= 10)

        level_box = Entry(level_window, 
                          textvariable=self.__level,
                          width=15,
                          font=("Arial", 14)
                          )
        level_box.pack(padx=10, pady=10)

        level_button = NButton( level_window,"Set", "#4287f5", self.change_level)

    def change_level(self) :

        level = self.__level.get()
        if level < 4 or level > 9 :
            showwarning("Invalid Level", "The level is limted between 4 and 9!", parent =self.__level_window )
        else :
            self.queens.set(level)
            self.reset_board()
            self.reset_level_label()
            self.__level_window.destroy()


class MenuBar(LevelConfigBox) :

    def create_menubar(self) :

        menubar = Menu(self.window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Level", command=self.create_level_config_box)
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="Settings", menu=filemenu, image=self.setting_img)
        self.window.config(menu=menubar)

        super().__init__()

    def exit(self) :
        exit(1)


class Queens :

    def render_queens(self) :

        parent = self.queen_frame
        for i in parent.winfo_children() :
            i.destroy()

        for i in range(0,self.queens.get()) :
            image_label = Label(parent, 
                            image=self.queen_icon,
                            width=50,
                            height=40,
                            )
            image_label.grid(row=0, column=i)

class ControlPanel:
    
    def create_control_panel(self ) :
        btn_frame = Frame(self.control_frame, 
                            width=self.board_size,
                            padx=50,
                            pady=50
                            )

        btn_frame.grid(row=0, column=0, sticky="nsew")
        
        timer = Label(btn_frame, text="00:00")
        timer.pack(anchor=CENTER, pady=20)

        start_btn = NButton(btn_frame, "Start Game", "#4CAF50")
        end_btn = NButton(btn_frame, "Give Up", "#FF5733")
