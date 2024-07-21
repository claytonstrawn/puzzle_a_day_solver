import numpy as np
from Piece import Piece
from constants import default_board,months,ndays

class Board(object):    
    count = 0
    def __init__(self,matrix = None,pieces = [],date = ('January',1),
                 pieces_remaining = 'abcdefgh',reset_count = False):
        self.matrix = matrix
        if matrix is None:
            self.matrix = default_board.copy()
            self.set_date(date)
        self.pieces = pieces
        self.pieces_remaining = pieces_remaining
        self.date = date
        if reset_count:
            Board.count = 1
        else:
            Board.count += 1
    
    def insert_piece(self,piece,x,y):
        embedded_piece = piece.embed_at_position(x,y)
        if embedded_piece is None:
            return None
        matrix_w_piece = self.matrix + embedded_piece
        if np.any(matrix_w_piece == 2):
            return None
        new_pieces = self.pieces+[(piece.piece_id,piece.rotation,bool(piece.flipped),x,y)]
        assert piece.piece_id in self.pieces_remaining, f"Cannot reuse piece '{piece.piece_id}'"
        new_pieces_remaining = self.pieces_remaining.replace(piece.piece_id,'')
        new_board = Board(matrix_w_piece,new_pieces,self.date,new_pieces_remaining)
        return new_board
    
    def find_first_zero(self):
        xs,ys = np.where(self.matrix == 0)
        return xs[0],ys[0]
    
    def set_date(self,date):
        if date is None:
            return
        month = date[0]
        assert month in months, "Use the full name of the month (e.g. 'January', 'February', etc.)"
        month_loc = months[month]
        day = int(date[1])
        if day > ndays[month]:
            print(f'warning: {date[0]} {date[1]} is not a valid day')
        assert day > 0 and day < 32, 'Day must be between 1 and 31'
        day_loc = (day-1)//7+2,(day-1)%7
        self.matrix[month_loc] = 1
        self.matrix[day_loc] = 1
        
    def display_pieces(self):
        for tup in self.pieces:
            piece_id,rotation,flip,x,y = tup
            board = default_board.copy()*-1
            piece = Piece(piece_id,rotation,flip)
            orig_0 = piece.matrix[0,0] == 0
            piece.matrix[0,0] = 2
            board+=piece.embed_at_position(x,y)
            print('insert piece')
            print(piece.matrix)
            if orig_0:
                piece.matrix[0,0] = 0
                print('(this one):')
                print(piece.matrix)
            print('at location')
            print(board)
            
    def __str__(self):
        return str(self.matrix)