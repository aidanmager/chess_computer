class Piece:
    def __init__(self, color):
        if color not in ('w', 'b', ''):
            raise Exception('invalid color given')
        self.color = color
        # self.hex_code = '\u25A1'
        self.hex_code = ' '
        self.name = 'Empty'
        self.pts = 0
        self.double_move_on_turn = -1 # only used by PAWN
        self.moves = []
        self.has_moved = False
    
    def get_hex(self):
        return self.hex_code 
    
    def get_name(self)->str:
        return self.name

    def get_pts(self)->int:
        return self.pts
    
    def get_color(self):
        return self.color
    
    def get_moves(self):
        return self.moves
    
    def mark_as_moved(self):
        self.has_moved = True
    
    def get_has_moved(self):
        return self.has_moved

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2659' if self.color=='w' else '\u265F'
        self.name = 'PAWN'
        self.pts = 1
        self.moves = [
            (-1,0), (-2,0), (-1,1), (-1,-1)
        ] if self.color=='w' else [
            (1,0),(2,0),(1,1),(1,-1)
        ]

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2656' if self.color=='w' else '\u265C'
        self.name = 'ROOK'
        self.pts = 5
        self.moves = [
            (1,0),  (2,0),  (3,0),  (4,0),  (5,0),  (6,0),  (7,0),
            (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0),
            (0,1),  (0,2),  (0,3),  (0,4),  (0,5),  (0,6),  (0,7),
            (0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)
        ]

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2657' if self.color=='w' else '\u265D'
        self.name = 'BISHOP'
        self.pts = 3
        self.moves = [
            (1,1),   (2,2),   (3,3),   (4,4),   (5,5),   (6,6),   (7,7),
            (1,-1),  (2,-2),  (3,-3),  (4,-4),  (5,-5),  (6,-6),  (7,-7),
            (-1,1),  (-2,2),  (-3,3),  (-4,4),  (-5,5),  (-6,6),  (-7,7),
            (-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)
        ]

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2658' if self.color=='w' else '\u265E'
        self.name = 'KNIGHT'
        self.pts = 3
        self.moves = [
            (1,2), (1,-2), (-1,2), (-1,-2),
            (2,1), (2,-1), (-2,1), (-2,-1)
        ]

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2655' if self.color=='w' else '\u265B'
        self.name = 'QUEEN'
        self.pts = 10
        self.moves = [
            (1,1),   (2,2),   (3,3),   (4,4),   (5,5),   (6,6),   (7,7),
            (1,-1),  (2,-2),  (3,-3),  (4,-4),  (5,-5),  (6,-6),  (7,-7),
            (-1,1),  (-2,2),  (-3,3),  (-4,4),  (-5,5),  (-6,6),  (-7,7),
            (-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7),
            (1,0),  (2,0),  (3,0),  (4,0),  (5,0),  (6,0),  (7,0),
            (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0),
            (0,1),  (0,2),  (0,3),  (0,4),  (0,5),  (0,6),  (0,7),
            (0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)
        ]

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hex_code = '\u2654' if self.color=='w' else '\u265A'
        self.name = 'KING'
        self.pts = 0
        self.moves = [
            (1,0), (1,1), (0,1),
            (-1,0), (-1,-1), (0,-1),
            (1,-1), (-1,1),
            (0,3),(0,-4) # castling
        ]
 
    def mark_as_moved(self):
        super().mark_as_moved()
        self.moves = [
            (1,0), (1,1), (0,1),
            (-1,0), (-1,-1), (0,-1),
            (1,-1), (-1,1)
        ] # remove castling priveleges
