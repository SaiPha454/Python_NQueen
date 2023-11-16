from tkinter import *
from tkinter import Toplevel
from tkinter.messagebox import showwarning

class NButton :

    def __init__(self, parent, text, color, callback = lambda : None, state="normal" ) :
        self.__parent = parent
        self.__width = 20
        self.__hieght = 2
        self.__text = text
        self.__color = color
        self.__font = ("Arial", 12)
        self.btn = Button(self.__parent,
                           width=self.__width, 
                           height=self.__hieght, 
                           text=self.__text,
                           bg=self.__color,
                           font=self.__font,
                           command=callback,
                           state=state,
                           )
        self.btn.config(disabledforeground=self.btn.cget("fg"))
        self.btn.pack(anchor=CENTER, pady=20)
    

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
                             text=f"NQueens Level : {self.queens.get()}",
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
        self.board = []
        self.solved_board = []

    def create_canvas(self) :

        canvas = Canvas(self.__parent,
                        width=self.__size, 
                        height=self.__size,
                        bg="white"
                        )
        canvas.grid(row=1, column=0)
        self.canvas = canvas
        self.create_board()        

    def create_board(self) :
        self.board = []
        self.solved_board = []
        for i in range(0, self.queens.get()) :
            row = []
            for k in range(0, self.queens.get()) :
                row.append(0)
            self.board.append(row)
            self.solved_board.append(row.copy())

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

                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=f"{row},{col}", outline="gray")

                self.palaces.append(id)
                self.canvas.tag_bind(id, "<Button-1>", self.add_queen)
            

    def reset_board(self) :

        self.palaces= []
        self.draw_board(self.queens.get())
        self.render_queens()
    
    def add_queen(self, event) :

        # Not allowed to play if the game is not started yet
        if not self.game_started :
            return
        
        rect = event.widget.find_overlapping(event.x, event.y, event.x+5, event.y+5)
        row_col = self.canvas.itemcget(rect,"tags")
        row_col = row_col.replace(" current","").split(",")

        if len(row_col) < 2:
            return
        row, col = row_col
        row = int(row)
        col = int(col)
        if not self.isSafe(self.board , row, col) :
            self.canvas.itemconfig(rect, outline="#ff0f0f", width=4)
            self.root.after(500, lambda: self.reset_warning_border(rect))
            return

        rect = self.canvas.coords(self.canvas.find_withtag(rect[0])) 
    
        x = rect[0] + (rect[2] - rect[0])/2
        y = rect[1] + (rect[3] - rect[1])/2
        queenid = self.canvas.create_image(x, y, image = self.queen_img, anchor =CENTER , tags=(row, col))
        self.canvas.tag_bind(queenid, "<Button-3>", self.remove_queen)
        self.board[row][col] = 1

        self.pop_queens()



    def reset_warning_border(self, rect):
        self.canvas.itemconfig(rect, width=1, outline="gray")
        

    def remove_queen(self, event) :

        row_col = self.canvas.gettags(CURRENT)

        if not self.game_started :
            return
        queen = event.widget.find_overlapping(event.x, event.y, event.x+2, event.y+2)
        print(queen)
        self.canvas.delete((queen[1],))
        
        if len(row_col) < 2 :
            return
        print(row_col)
        row = int(row_col[0])
        col = int(row_col[1])
        self.board[row][col] = 0
        self.append_queens()

    def solve(self):
         col = 0
         self.backtrack(col)
         print(self.solved_board)
         rectId = 1
         for row in range(self.queens.get()) :
             
            for col in range(self.queens.get()) :
                if self.solved_board[row][col] == 1 :
                    self.canvas.itemconfig((rectId,), outline="#4FBF26", width=5)
                rectId+=1
    def backtrack(self, col) :
        
        if col >= self.queens.get() :
            return True
        for i in range(self.queens.get()):
            if self.isSafe(self.solved_board, i, col) :
                self.solved_board[i][col] = 1

                if (self.backtrack(col+1)):
                    return True
                self.solved_board[i][col]=0
        return False
        
    def isSafe(self, board, row, col) :
        row_safe = self.row_check(board, row)
        col_safe = self.col_check(board, col)
        diagonal_safe = self.diagonal_check(board, row, col)
        return row_safe and col_safe and diagonal_safe
    
    def row_check(self, board, row) :

        return not board[row].__contains__(1)
    
    def col_check(self, board, col):

        status = True
        for r in range(0, len(board)) :

            for c in range(0, len(board[r])) :
                if c == col :
                    if board[r][c] == 1 :
                        return False
                    break
        return status
    
    def diagonal_check(self, board, row, col) :

        upper_right = True
        upper_left = True
        lower_right = True
        lower_left = True

        temp_row = row +1
        temp_col = col +1

        #check lower_right
        while temp_row < self.queens.get() and temp_col < self.queens.get() :

            if board[temp_row][temp_col] == 1:
                lower_right = False
                break
            temp_row += 1
            temp_col += 1

        #check lower_left
        temp_row = row +1
        temp_col = col -1
        while temp_row < self.queens.get() and temp_col >=0 :
            if board[temp_row][temp_col] == 1:
                lower_left = False
                break
            temp_col -= 1
            temp_row += 1

        #check upper_right
        temp_row = row -1
        temp_col = col +1
        while temp_row >=0 and temp_col < self.queens.get() :
            if board[temp_row][temp_col] == 1:
                upper_right = False
                break
            temp_col += 1
            temp_row -= 1

        #check upper_left
        temp_row = row -1
        temp_col = col -1
        while temp_row >=0 and temp_col >=0 :
            if board[temp_row][temp_col] == 1:
                upper_left = False
                break
            temp_col -= 1
            temp_row -= 1
        
        return upper_left and upper_right and lower_left and lower_right


class LevelConfigBox : 

    def __init__(self) -> None:
        self.__level = IntVar()
        self.__level.set(self.queens.get())
        self.timer_on = BooleanVar()
        self.timer_on.set(True)
        self.__timer_limit_mn = IntVar()
        self.__timer_limit_mn.set(self.timer_limit_mn)
    
    def create_level_config_box(self):

        self.__level.set(self.queens.get())
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

        NButton( level_window,"Set", "#4287f5", self.change_level)

    def change_level(self) :

        try :
            level = self.__level.get()
            if level < 4 or level > 9 :
                showwarning("Invalid Level", "The level is limted between 4 and 9!", parent =self.__level_window )
            else :
                self.queens.set(level)
                self.reset_board()
                self.reset_level_label()
                self.__level_window.destroy()
                self.reset_timer()
                self.start_button.btn.config(state="normal")
                self.solved = False
                self.game_started = False
        except TclError:
            showwarning("Invalid input", "The level input must be integer")
    

    def create_timer_config_box(self):

        self.__timer_limit_mn.set(self.timer_limit_mn)
        timer_window = Toplevel(self.window)
        self.__timer_window = timer_window
        timer_window.geometry("400x300")
        timer_window.resizable(False, False)
        timer_window.title("Timer Setting")

        timer_checkbox  = Checkbutton(timer_window,
                    variable= self.timer_on,
                    text="Set timer",
                    command=self.on_check,
                    )

        timer_checkbox.pack(pady=15)

        label = Label(timer_window, text="Duration :", font=("Arial", 14))
        label.pack(pady= 10)

        timer_input = Entry(timer_window, 
                          textvariable=self.__timer_limit_mn,
                          width=8,
                          font=("Arial", 14),
                          state= "normal" if self.timer_on.get() else "disabled"
                           )
        timer_input.pack(padx=10, pady=10)
        self.timer_input = timer_input 
        self.timer_btn = NButton( timer_window,"Set", "#4287f5", self.set_timer, state= "normal" if self.timer_on.get() else "disabled")
    
    def on_check(self) :
        
        if self.timer_on.get() :
            self.timer_btn.btn.config(state="normal")
            self.timer_input.config(state="normal")
        else:
            self.timer_btn.btn.config(state="disabled")
            self.timer_input.config(state="disabled")

    def set_timer(self) :
        try :
            if self.__timer_limit_mn.get() <= 0 :
                showwarning("Invalid input", "The time input must be integer greater than 0")
                return
            self.timer_limit_mn = self.__timer_limit_mn.get()
            self.__timer_window.destroy()
        except TclError:
            showwarning("Invalid input", "The time input must be integer in minute")


class TimerConfigBox : 

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
            self.reset_timer()



class MenuBar(LevelConfigBox) :


    def __init__(self) -> None:

        super().__init__()

    def create_menubar(self) :

        menubar = Menu(self.window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Level", command=self.create_level_config_box)
        filemenu.add_command(label="Timer", command=self.create_timer_config_box)
        filemenu.add_command(label="Exit", command=self.exit)

        menubar.add_cascade(label="Settings", menu=filemenu, image=self.setting_img)
        self.window.config(menu=menubar)

        super().__init__()

    def exit(self) :
        exit(1)


class Queens :

    def __init__(self) -> None:
        self.col = 0
        self.breaker = 5
        self.left_queens = []

    def render_queens(self) :

        self.left_queens = []
        parent = self.queen_frame
        for i in parent.winfo_children() :
            i.destroy()

        for i in range(0,self.queens.get()) :
            self.append_queens()

    def pop_queens(self):
        
        if len(self.left_queens) == 0 :
            return
        self.left_queens[len(self.left_queens)-1].destroy()
        self.left_queens.pop()

        if len(self.left_queens) == 0 :
            self.root.after_cancel(self.timer_id)
            self.success()
    
    def append_queens(self) :

        if len(self.left_queens) > self.queens.get() :
            return
        
        image_label = Label(self.queen_frame, 
                            image=self.queen_icon,
                            width=40,
                            height=40,
                            )
        self.left_queens.append(image_label)
        image_label.grid(row=0, column=len(self.left_queens))

class ControlPanel:
    
    def __init__(self, root):
        self.mn = 0
        self.sec = 0
        self.game_started = False
        self.solved = False
        self.root = root


    def create_control_panel(self ) :
        btn_frame = Frame(self.control_frame, 
                            width=self.board_size,
                            padx=50,
                            pady=50
                            )

        btn_frame.grid(row=0, column=0, sticky="nsew")
        
        self.timer = Label(btn_frame, text=f"{self.mn:02}:{self.sec:02}")
        self.timer.pack(anchor=CENTER, pady=20)

        self.start_button = NButton(btn_frame, "Start Game", "#4CAF50", callback=self.start_game)
        NButton(btn_frame, "Reset", "#4CAF50",callback=self.reset_game)
        self.give_up_button = NButton(btn_frame, "Give Up", "#FF5733", callback=self.give_up)
    
    def start_game(self) :
        
        if self.solved :
            self.reset_board()
        if not self.game_started :
            self.reset_timer()
            self.solved = False
            self.game_started = True
            self.update_timer()
        self.start_button.btn.config(state="disabled")
    

    def reset_game(self) :

        self.reset_timer()
        self.solved = False
        self.game_started = False
        self.reset_board()
        self.start_button.btn.config(state="normal")
    
    def give_up(self) :

        if self.game_started :
            self.end_game()
            self.solve()

    def end_game(self) :
        self.solved = True
        self.game_started= False
        self.root.after_cancel(self.timer_id)
        
    def reset_timer(self):
        self.mn = 0
        self.sec = 0
        self.timer.config(text=f"{self.mn:02}:{self.sec:02}")

    def update_timer(self) :

        #To prevent auto counting on change level
        if not self.game_started :
            return

        self.sec +=1
        if self.sec == 60:
            self.sec = 0
            self.mn += 1
        self.timer.config(text=f"{self.mn:02}:{self.sec:02}")
        if self.timer_on.get() and  self.mn >= self.timer_limit_mn :
            self.time_up()
            return
        self.timer_id = self.root.after(500, self.update_timer)
    
    def time_up(self) :

        self.end_game()
        game_over_window = Toplevel(self.window)
        game_over_window.geometry("400x200")
        game_over_window.resizable(False, False)
        game_over_window.title("Time Up")

        label = Label(game_over_window, text="Game Over!!!", font="Arial 25 bold", fg="red")
        label.pack(pady= 50)
        self.center_game_over_window(game_over_window)

        
    def success(self):

        game_success_window = Toplevel(self.window)
        game_success_window.geometry("400x200")
        game_success_window.resizable(False, False)
        game_success_window.title("Win Game")

        label = Label(game_success_window, text=f"Congraduations!!! \nYou have solved the {self.queens.get()} Queens Problem.", 
                      font="Arial 14 bold", fg="green")
        label.pack(pady= 50)
        self.center_game_over_window(game_success_window)

    def center_game_over_window(self, top_window) :

        root_x = self.window.winfo_rootx()
        root_y = self.window.winfo_rooty()
        root_width = self.window.winfo_width()
        root_height = self.window.winfo_height()

        window_width = top_window.winfo_reqwidth()
        window_height = top_window.winfo_reqheight()

        x = root_x + (root_width - window_width) // 4
        y = root_y + (root_height - window_height) // 4
        
        top_window.geometry("+%d+%d" % (x, y))
        top_window.update_idletasks()
        top_window.grab_set()