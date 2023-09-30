from tkinter import *

class NButton :

    def __init__(self, parent, text, color) :
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
                           )
        self.__btn.pack(anchor=CENTER, pady=20)

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




class NCanvas :

    def __init__(self, parent, size) :
        
        self.__size = size
        self.__parent = parent

        canvas = Canvas(self.__parent,
                        width=self.__size, 
                        height=self.__size,
                        bg="white"
                        )
        canvas.grid(row=1, column=0)
        self.canvas = canvas


    def draw_board(self, queens) :

        if not hasattr(self, "canvas") :
            self.canvas.create_canvas(parent=self.__parent)

        box_size = int(self.__size/queens)

        for row in range(0,queens) :

            for col in range(0, queens):
                
                x1, y1 = row * box_size, col* box_size
                x2, y2 = x1+ box_size, y1+ box_size
                color = "white"
                if (row + col) % 2 != 0 :
                    color = "gray"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def clear_board(self) :
        self.canvas.delete(all)



class MenuBar :

    def create_menubar(self) :

        menubar = Menu(self.window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Level", command=self.change_level)
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="Settings", menu=filemenu, image=self.setting_img)
        self.window.config(menu=menubar)
    def change_level(self) :
        self.queens=5
        self.clear_board()
        self.draw_board(self.queens)
        self.render_queens()

    def exit(self) :
        exit(1)


class Queens :

    def render_queens(self) :

        parent = self.queen_frame
        for i in parent.winfo_children() :
            i.destroy()

        for i in range(0,self.queens) :
            image_label = Label(parent, 
                            image=self.queen_img,
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
