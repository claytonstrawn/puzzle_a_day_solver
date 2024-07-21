import numpy as np
from Board import Board
from Piece import Piece
from constants import no_flip,half_symmetry
from plotting import plot_board

def solve_board(date=None,board=None,allow_flips = False,
                take_first = True,verbose = False,plot_solution = True):
    if board is None and date is not None:
        board = Board(date=date)
    if board is None and date is None:
        assert False, "One of board or date must be specified to solve."
    output = solve_board_recursor(board,allow_flips,take_first,verbose)
    flip_str = '(without flips)' if not allow_flips else '(with flips)'
    if output is None:
        print(f'No solution found {flip_str}!')
        if not allow_flips:
            print('perhaps try with "allow_flips = True"?')
        return None
    elif isinstance(output,list):
        if len(output) == 1:
            print(f"1 solution found {flip_str}.")
        else:
            print(f"{len(output)} solutions found {flip_str}.")
    elif isinstance(output,Board):
        print(f"Solution found {flip_str}.")
    if plot_solution:
        if isinstance(output,list):
            plot_board(output[0],1)
        if isinstance(output,Board):
            plot_board(output)
    return output
        

def solve_board_recursor(board,allow_flips,take_first,verbose):
    if verbose and 0:
        print(board.pieces)
        print(board)
        print(board.pieces_remaining)
    x,y = board.find_first_zero()
    flips_list = [False] if not allow_flips else [False,True]
    solutions = []
    for piece_id in board.pieces_remaining:
        for rotation in range(4):
            for flip in flips_list:
                if piece_id in no_flip and flip:
                    continue
                elif piece_id in half_symmetry and rotation >= 2:
                    continue
                piece = Piece(piece_id,rotation,flip)
                offset = np.where(piece.matrix[0]==1)[0][0]
                if verbose and 0:
                    print(piece_id,rotation,flip,x,y-offset)
                    print(piece)
                new_board = board.insert_piece(piece,x,y-offset)
                if new_board is None:
                    if verbose and 0:                     
                        print('fail')
                    continue
                if new_board.pieces_remaining == '':
                    return new_board
                returned = solve_board_recursor(new_board,allow_flips,take_first,verbose)
                if isinstance(returned,Board):
                    if not take_first:
                        solutions+=[returned]
                    else:
                        return returned
                elif isinstance(returned,list):
                    solutions+=returned
                elif returned is None:
                    continue
    if len(solutions)>0:
        return solutions
    else:
        return None