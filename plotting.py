import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from Piece import Piece
from constants import months,default_board,colors_dict

"""
summary: Plot a matrix on an axis in a particular color, square by square. This can 
         either be a Piece matrix or a Board matrix (usually the default)

inputs: ax: An Axis object instance.
        matrix: NDArray, the array of 1s and 0s representing a Piece or Board
        x: int, row of top left corner.
        y: int, column of top left corner.
        color: string or other Color indicator, color for this matrix. 
        hatch: string, '/' if the piece is to be hatched, else None.
                (Pieces are hatched if they have to be flipped.)
        
outputs: None
"""
def add_matrix(ax,matrix,x,y,color,hatch):
    boxes = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i,j]:
                r = Rectangle(((y+j),6-(x+i)),1,1)
                boxes.append(r)
    pc = PatchCollection(boxes, facecolor=color, alpha=0.7,
                     edgecolor='black',hatch = hatch)
    ax.add_collection(pc)

"""
summary: Fill in all the months and days in the appropriate place in the Board, on an Axis

inputs: ax: An Axis object instance.
        
outputs: None
"""
def fill_in_text(ax):
    hoffset = 0.4
    voffset = 0.3
    for month in months:
        month_x,month_y = months[month]
        month_text = month[:3].upper()
        ax.text(month_y+hoffset,6-month_x+voffset,month_text)
    for day in range(31):
        day_x,day_y = day//7+2,day%7
        day_text = str(day+1)
        ax.text(day_y+hoffset,6-day_x+voffset,day_text)

"""
summary: Plot a Board instance using matplotlib, including call to show().

inputs: board: Board instance. May have Pieces or not.
        sol_name: string or None, add this string to the title if not None
                  It's added on as a named solution (usually a number)
        
outputs: None
"""
def plot_board(board,sol_name = None):
    ax = plt.gca()
    fill_in_text(ax)
    add_matrix(ax,default_board,0,0,'black',None)
    for i,piece_info in enumerate(board.pieces):
        piece_id,rotation,flip,x,y = piece_info
        piece = Piece(piece_id,rotation,flip)
        hatch = None if not flip else '/'
        add_matrix(ax,piece.matrix,x,y,colors_dict[piece_id],hatch)
    ax.set_xlim(0,7)
    ax.set_ylim(0,7)
    if board.date is not None:
        if sol_name is not None:
            ax.set_title(f'Solution {sol_name} for {board.date[0]} {board.date[1]}')
        else:
            ax.set_title(f'Solution for {board.date[0]} {board.date[1]}')
    plt.xticks([], [])
    plt.yticks([], [])
    plt.show()
