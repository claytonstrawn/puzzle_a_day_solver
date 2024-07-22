import numpy as np
from Piece import Piece
from constants import default_board,months,ndays

"""
Class representing the overall board with all pieces placed, and the date.
The 'Board.count' class variable tracks how many boards have been made. Reset 
after each task to track the boards made for that task.
"""
class Board(object):
    count = 0
    """
    summary: Create a new Board. If given a matrix and pieces, then create a prefilled Board.
    Else, create a new Board with matrix = 1 only at the date and the weird shape edges.
    
    inputs: matrix: NDArray, the representation of the open and filled spaces. Open = 0, filled = 1 (shape edge, piece, or date to fill). 
            pieces: list of tuples, each tuple is 5 elements. (piece_id: char, rotation: int, flip: bool, x: int, y: int)
                    where piece_id is between a and h, rotation = 0,1,2,3, flip = True or False, x, y are position of upper
                    left corner of Piece in matrix.
            date: Tuple, The month, day that are marked 1 in the matrix representing the day this solution is for. 
            pieces_remaining: String, all the pieces that have not yet been used.
            reset_count: bool, if True then this board resets Board.count to 1
            
    outputs: a Board with these pieces at these positions.
    """
    def __init__(self,matrix = None,pieces = [],date = ('January',1),
                 pieces_remaining = 'abcdefgh',reset_count = False):
        self.matrix = matrix
        if matrix is None:
            #need to copy the default board to not mess with the original
            self.matrix = default_board.copy()
            self.set_date(date)
        self.pieces = pieces
        self.pieces_remaining = pieces_remaining
        self.date = date
        if reset_count:
            Board.count = 1
        else:
            Board.count += 1

    """
    summary: Add a Piece into this board's matrix at a particular place.
    
    inputs: piece: Piece, with a particular matrix representing its values, etc.
            x: int, row of location in Matrix
            y: int, entry in location in Matrix, row
            
    outputs: a new Board with this Piece added in.
    """
    def insert_piece(self,piece,x,y):
        embedded_piece = piece.embed_at_position(x,y)
        if embedded_piece is None:
            return None
        matrix_w_piece = self.matrix + embedded_piece
        if np.any(matrix_w_piece == 2):
            return None
        new_pieces = self.pieces+[(piece.piece_id,piece.rotation,bool(piece.flipped),x,y)]
        #subtract this piece from the available pieces.
        assert piece.piece_id in self.pieces_remaining, f"Cannot reuse piece '{piece.piece_id}'"
        new_pieces_remaining = self.pieces_remaining.replace(piece.piece_id,'')
        new_board = Board(matrix_w_piece,new_pieces,self.date,new_pieces_remaining)
        return new_board

    """
    summary: Find the top left location that needs to be filled by a Piece.
    
    inputs: None
            
    outputs: x: int, row of first zero.
             y: int, column of first zero.
    """
    def find_first_zero(self):
        xs,ys = np.where(self.matrix == 0)
        return xs[0],ys[0]

    """
    summary: Mark the specific month, day given with 1's in the matrix.
    
    inputs: date: Tuple, (month: String, day: int). Month is a full name of a month with capital letter,
                  day is between 1 and 31. If date is None, then just matrix as all 0s besides the edges.
            
    outputs: None
    """
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

    """
    summary: Print list of instructions for filling in a board as text (defunct with plot_board)
    
    inputs: None
            
    outputs: None
    """
    def display_pieces(self):
        for tup in self.pieces:
            piece_id,rotation,flip,x,y = tup
            board = default_board.copy()*-1
            piece = Piece(piece_id,rotation,flip)
            orig_0 = piece.matrix[0,0] == 0
            #put a 2 in the top left corner, to help id where the piece should go.
            piece.matrix[0,0] = 2
            board+=piece.embed_at_position(x,y)
            print('insert piece')
            print(piece.matrix)
            #the 2 is supposed to replace a 1, but if it replaces a 0 there is a possible ambiguity
            if orig_0:
                piece.matrix[0,0] = 0
                print('(this one):')
                print(piece.matrix)
            print('at location')
            print(board)
            
    def __str__(self):
        return str(self.matrix)
