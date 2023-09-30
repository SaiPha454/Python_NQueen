
class NQueen :

    def __init__(self, queens):
        
        self.queen = queens
        self.board = self.get_board(queens)
    
    def get_board(self, queens) :
        boards = []
        for i in range(0, queens) :
            row = []
            for k in range(0, queens) :
                row.append(0)
            boards.append(row)
        return boards
    
    def isSafe(self, row, col) :

        row_exist = False
        col_exist = False
        diagonal_exist = False
        n = len(self.board)

        current_row = self.board[row]
        if current_row.__contains__(1) :
            row_exist = True

        for i in range(0, len(self.board)) :

            for k in range(0, len(self.board[i])) :
                if k == col :
                    if self.board[i][k] == 1 :
                        col_exist = True
                    break

        rev_next_col = col
        next_col = col

        for i in range(row, n) :
            if next_col < n :
                if self.board[i][next_col] == 1 :
                    diagonal_exist = True
                    break
            if rev_next_col > -1 :
                if self.board[i][rev_next_col] == 1 :
                    diagonal_exist = True
                    break
            rev_next_col -= 1
            next_col += 1

        rev_next_col = col
        next_col = col

        for i in range(row, -1, -1) :

            if next_col < n :
                if self.board[i][next_col] == 1 :
                    diagonal_exist = True
                    break
            if rev_next_col > -1 :
                if self.board[i][rev_next_col] == 1 :
                    diagonal_exist = True
                    break
            rev_next_col -= 1
            next_col += 1


        return not (row_exist or col_exist or diagonal_exist)
    

    def add_queen(self, row, col) :

        if not self.isSafe(row= row, col=col) :
            return False
        else :
            self.board[row][col] = 1
            return True
    def rm_queen(self, row, col) :

        self.board[row][col] = 0


    def solution(self) :

        self.board = self.get_board(self.queen)

        n = self.queen
        board = self.board
        col = 0
        
        while col < len(board) :

            available = False

            for row in range(0, len(board)) :

                if self.isSafe(row, col) :

                    board[row][col] = 1
                    available = True
                    break


            if available == False :
                cur_col = col -1
                while cur_col > -1 :

                    row = 1

                    for i in range(n) :

                        if board[i][cur_col] == 1 :
                            row += i
                        board[i][cur_col] = 0



                    for i in range(row, n) :

                        if self.isSafe(i, cur_col) :
                            board[i][cur_col] = 1
                            available = True
                            break

                    if available :
                        col = cur_col
                        break
                    cur_col = cur_col-1

            col += 1
        if not (1 in board[0]) :
            return False
        else :
            return board