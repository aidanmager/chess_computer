from chess_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.ROWS = 8
        self.COLS = 8
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.whites_turn = True
        self.turn = 1
        self.col_dict = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3,
            'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        self.row_dict = {
            '1': 7, '2': 6, '3': 5, '4': 4,
            '5': 3, '6': 2, '7': 1, '8': 0
        }

        self.reverse_dict = {
            (0,0): 'A8', (0,1): 'B8', (0,2): 'C8', (0,3): 'D8',
            (0,4): 'E8', (0,5): 'F8', (0,6): 'G8', (0,7): 'H8',

            (1,0): 'A7', (1,1): 'B7', (1,2): 'C7', (1,3): 'D7',
            (1,4): 'E7', (1,5): 'F7', (1,6): 'G7', (1,7): 'H7',

            (2,0): 'A6', (2,1): 'B6', (2,2): 'C6', (2,3): 'D6',
            (2,4): 'E6', (2,5): 'F6', (2,6): 'G6', (2,7): 'H6',

            (3,0): 'A5', (3,1): 'B5', (3,2): 'C5', (3,3): 'D5',
            (3,4): 'E5', (3,5): 'F5', (3,6): 'G5', (3,7): 'H5',

            (4,0): 'A4', (4,1): 'B4', (4,2): 'C4', (4,3): 'D4',
            (4,4): 'E4', (4,5): 'F4', (4,6): 'G4', (4,7): 'H4',

            (5,0): 'A3', (5,1): 'B3', (5,2): 'C3', (5,3): 'D3',
            (5,4): 'E3', (5,5): 'F3', (5,6): 'G3', (5,7): 'H3',

            (6,0): 'A2', (6,1): 'B2', (6,2): 'C2', (6,3): 'D2',
            (6,4): 'E2', (6,5): 'F2', (6,6): 'G2', (6,7): 'H2',

            (7,0): 'A1', (7,1): 'B1', (7,2): 'C1', (7,3): 'D1',
            (7,4): 'E1', (7,5): 'F1', (7,6): 'G1', (7,7): 'H1',
        }

        self.reset_board()

    
    # Takes a move (ie E4, H5, B3) and returns the row, col coordinates
    def translate_move(self, s:str):
        if len(s) != 2:
            raise Exception('Invalid move given (length not 2)')
        
        return self.row_dict[s[1]], self.col_dict[s[0]]
    
    def get_pts(self):
        white_pts = 0
        black_pts = 0
        for ROW in range(self.ROWS):
            for COL in range(self.COLS):
                piece = self.board[ROW][COL]
                color = piece.get_color()
                pts = piece.get_pts()
                if color == 'w':
                    white_pts += pts
                elif color == 'b':
                    black_pts += pts
        return white_pts, black_pts

    # Resets the board to the starting position
    def reset_board(self):
        for ROW, ROW_pawn, color in [(0, 1, 'b'), (7, 6, 'w')]:
            self.board[ROW][0] = Rook(color)
            self.board[ROW][1] = Knight(color)
            self.board[ROW][2] = Bishop(color)
            self.board[ROW][3] = Queen(color)
            self.board[ROW][4] = King(color)
            self.board[ROW][5] = Bishop(color)
            self.board[ROW][6] = Knight(color)
            self.board[ROW][7] = Rook(color)
            for i in range(self.COLS):
                self.board[ROW_pawn][i] = Pawn(color)

        for ROW in [2, 3, 4, 5]:
            for COL in range(self.COLS):
                self.board[ROW][COL] = Piece('')
        
        print(self.to_str())
    
    def to_str(self)->str:
        result = f"\nIt is {'WHITE' if self.whites_turn else 'BLACK'}\'s turn {self.turn}\n"
        result += '  ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗\n'
        border  = '  ╟───┼───┼───┼───┼───┼───┼───┼───╢\n'
        for ROW in range(self.ROWS):
            result += f'{self.ROWS - ROW} ║' # row nums
            for COL in range(self.COLS):
                result += ' ' + self.board[ROW][COL].get_hex()
                result += ' │' if COL < self.COLS-1 else ' ║'
            result += '\n'
            if ROW < self.ROWS-1:
                result += border
        result += '  ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝\n'
        result += '    A   B   C   D   E   F   G   H  \n' 
        return result
    
    # returns true if there are no pieces in the way for the given path
    # Assumes start_row, end_row, start_col, end_col are all in bounds
    def is_valid_path(self, piece_name:str, piece_color:str, 
                            start_row:int, start_col:int, 
                            end_row:int, end_col:int)->bool:
        if piece_name == 'KNIGHT':
            if self.square_is_empty(end_row, end_col):
                return True
            target_piece_color = self.board[end_row][end_col].get_color()
            if target_piece_color == piece_color:
                return False  # cannot take own piece
            return True
        
        if piece_name == 'PAWN':
            if abs(end_row - start_row) == 2: # double pawn move allowed only on starting square
                mid_row = int((start_row + end_row)/2)
                if not self.square_is_empty(mid_row, start_col):
                    return False
                return (piece_color == 'w' and start_row == 6) or (piece_color == 'b' and start_row == 1) # pawn on starting square, so double move allowed
            
            if abs(end_col - start_col) > 0: # diagonal pawn move
                #check en passant
                offset = 1 if piece_color == 'w' else 0
                en_passant_piece = self.board[start_row][end_col]

                if en_passant_piece.double_move_on_turn + offset == self.turn and en_passant_piece.get_color() != piece_color: # if opposing pawn double moved last turn
                    return True

                if self.square_is_empty(end_row, end_col):
                    return False
                target_piece_color = self.board[end_row][end_col].get_color()
                if target_piece_color == piece_color:
                    return False  # cannot take own piece
                return True
            
            return self.square_is_empty(end_row, end_col) # single pawn move only cares if square is empty (cannot take)

        if piece_name == 'KING' and end_col in (0,7) and start_col == 4: # king trying to castle
            if self.board[end_row][end_col].get_has_moved(): 
                return False # rook has moved, so castling prohibited

            if end_col == 7: #castling short
                cols_to_check = [5,6]
            else: # castling long
                cols_to_check = [1,2,3]
            
            for col in cols_to_check:
                if not self.square_is_empty(start_row, col):
                    return False
            return True
        
        d_row = end_row - start_row # rows to move
        d_col = end_col - start_col # cols to move
        num_moves = max(abs(d_row), abs(d_col)) - 1 # subtract 1 because the the target square needs to be handled specially (can take)
        if num_moves < 0:
            return True # if there are no moves to make

        m_row = int(d_row/abs(d_row)) if d_row != 0 else 0 # rate of row change (either -1, 0 ,1)
        m_col = int(d_col/abs(d_col)) if d_col != 0 else 0 # rate of col change (either -1, 0 ,1)

        curr_row, curr_col = start_row, start_col
        for i in range(num_moves):
            curr_row += m_row
            curr_col += m_col
            if not self.square_is_empty(curr_row, curr_col):
                return False

        # path to target square is valid at this point

        if self.square_is_empty(end_row, end_col):
            return True # target square is empty

        target_piece_color = self.board[end_row][end_col].get_color()
        if target_piece_color == piece_color:
            return False  # cannot take own piece

        return True

    # selects a piece on the board and returns an array with all possible valid moves
    # if selected square is empty, will return an empty array
    def select(self, square:str):
        row, col = self.translate_move(square)
        if row < 0 or row >= 8 or col < 0 or col >= 8:
            raise Exception('Selected square is out of bounds.')
        
        piece = self.board[row][col]
        piece_name = piece.get_name()
        piece_color = piece.get_color()

        print(f'You selected a {piece_name} on {square}')

        turn = 'w' if self.whites_turn else 'b'        
        if piece_color != turn or piece_name == 'Empty':
            return []
        
        all_moves = piece.get_moves()
        valid_moves = []
        for move_row, move_col in all_moves:
            dest_row = row + move_row
            dest_col = col + move_col

            if dest_row < 0 or dest_row >= 8 or dest_col < 0 or dest_col >= 8:
                # print('     not valid. out of bounds')
                continue  # destination square is out of bounds
            
            # print(f'Checking if move {self.reverse_dict[(dest_row, dest_col)]} is valid.')
            if self.is_valid_path(piece_name, piece_color, row, col, dest_row, dest_col):
                valid_moves.append(self.reverse_dict[(dest_row, dest_col)])

        print(f'Valid Moves: {", ".join(valid_moves)}\n')
        return valid_moves
    
    # Assumes 0 <= row, col < 8
    def square_is_empty(self, row:int, col:int)->bool:
        # if row >= self.ROWS or col >= self.COLS:
        #     raise Exception('Square is out of bounds')
        return self.board[row][col].get_name() == 'Empty'
    
    def get_turn(self):
        return 'w' if self.whites_turn else 'b'


    def move(self, start_square:str, dest_square:str):
        piece_row, piece_col = self.translate_move(start_square)
        dest_row, dest_col = self.translate_move(dest_square)

        piece_to_move = self.board[piece_row][piece_col]
        piece_to_move_name = piece_to_move.get_name()
        piece_to_move_color = piece_to_move.get_color()

        if piece_to_move_name == 'Empty':
            print('That square is empty. Try again.')
            return
            # raise Exception('That square is empty')
        
        if piece_to_move_color != self.get_turn():
            print('Wrong color piece. Try again.')
            return
            # raise Exception('Wrong color piece')

        d_row, d_col = dest_row - piece_row, dest_col - piece_col
        if (d_row, d_col) not in piece_to_move.get_moves():
            print('That piece cannot move like that ever. Try again.')
            return
            # raise Exception('That piece cannot move like that ever')
        
        if not self.is_valid_path(piece_to_move_name, piece_to_move_color, piece_row, piece_col, dest_row, dest_col):
            print('Invalid move. Try again.')
            return
            # raise Exception('Invalid move')

        print(f'Moving {piece_to_move_name} {start_square} to {dest_square}...')

        if piece_to_move_name == 'KING' and dest_col in (0,7) and piece_col == 4: #castling
            offset = -1 if dest_col == 7 else 1
            self.board[piece_row][piece_col-offset] = self.board[dest_row][dest_col] # move rook
            self.board[dest_row][dest_col] = Piece('') # remove old rook
            dest_col += offset
        
        if piece_to_move_name == 'PAWN' and abs(dest_col - piece_col) > 0 and self.square_is_empty(dest_row, dest_col):
            self.board[piece_row][dest_col] = Piece('') # taking en passant

        # move piece
        self.board[dest_row][dest_col] = piece_to_move
        self.board[piece_row][piece_col] = Piece('')

        if piece_to_move_name == 'PAWN' and abs(d_row) == 2:
            piece_to_move.double_move_on_turn = self.turn # toggle en passant if double move

        piece_to_move.mark_as_moved()

        self.whites_turn = not self.whites_turn
        if self.whites_turn:
            self.turn += 1

        print(self.to_str())