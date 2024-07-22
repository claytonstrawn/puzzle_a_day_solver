import numpy as np
from constants import piece_matrices

"""
Class representing an individual piece, represented as a small (2x3, 3x3, or 2x4) matrix. There is a "natural" orientation
of each piece, and then it can be flipped over or rotated. The piece keeps it's ID, rotation, flipped status, and its
resulting matrix.
"""
class Piece(object):
    """
    summary: Create a new Piece, given an orientation.
    
    inputs: piece_id: char, letter representing a unique piece shape
            rotation: int, number between 0 and 3, representing a number of 90 degree turns
            flip: bool, if False, do not flip, if true, flip over.
            
    outputs: a Piece with this orientation
    """
    def __init__(self,piece_id,rotation = 0,flip = False):
        self.piece_id = piece_id
        #set up in default position, then move. 
        self.rotation = 0
        self.flipped = False
        self.matrix = piece_matrices[piece_id]
        self.rotate(rotation)
        self.flip(flip)

    """
    summary: Rotate this piece's Matrix counterclockwise by 90 degrees n times.
    
    inputs: rotation: int, number between 0 and 3, representing a number of 90 degree turns
            
    outputs: None
    """
    def rotate(self,rotation):
        self.rotation = (self.rotation+rotation)%4
        self.matrix = np.rot90(self.matrix,rotation)

    """
    summary: Flip this piece's Matrix by 180 degrees over the center line.
    
    inputs: will_flip: bool, if False, do nothing
            
    outputs: None
    """
    def flip(self,will_flip):
        if will_flip:
            self.flipped = ~self.flipped
            self.matrix = np.flip(self.matrix,axis = 0)

    """
    summary: Return a matrix with the same shape as a Board.matrix with this piece located at a
             particular position.
    
    inputs: x: int, row of upper left corner of the piece
            y: int, column of upper left corner
            
    outputs: NDArray, a 7x7 array with this piece location as 1's.
             Will return None if this piece cannot be located in the 7x7 array at that location.
    """ 
    def embed_at_position(self,x,y):
        board = np.zeros((7,7))
        piece_size_x,piece_size_y = self.matrix.shape
        try:
            board[x:x+piece_size_x,y:y+piece_size_y] += self.matrix
            return board.astype('int64')
        except ValueError:
            return None
        
    def __str__(self):
        return str(self.matrix)
    
    def __repr__(self):
        return str(self.matrix)
