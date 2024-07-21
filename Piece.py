import numpy as np
from constants import piece_matrices

class Piece(object):
    def __init__(self,piece_id,rotation = 0,flip = False):
        self.piece_id = piece_id
        self.rotation = 0
        self.flipped = False
        self.matrix = piece_matrices[piece_id]
        self.rotate(rotation)
        self.flip(flip)
        
    def rotate(self,rotation):
        self.rotation = (self.rotation+rotation)%4
        self.matrix = np.rot90(self.matrix,rotation)
        
    def flip(self,will_flip):
        if will_flip:
            self.flipped = ~self.flipped
            self.matrix = np.flip(self.matrix,axis = 0)
        
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