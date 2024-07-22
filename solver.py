import numpy as np
from Board import Board
from Piece import Piece
from constants import no_flip,half_symmetry
from plotting import plot_board

"""
summary: Find a solution for a given Board or Date. Decide if you want to allow flips or not
         (not all boards can be solved without flips).

inputs: date: tuple, (month: string, fullname month, day: int day of month). Or None, if a Board is specified 
        board: Board, a Board with another date. One of date or board must be specified. Can be partially filled.
        allow_flips: bool, if True, then let flips be included in process, else exclude them.
        take_first: bool, if True, return the first successful Board. If False, return the list of all solution Boards.
        use_saved_solutions: bool, if True, look up the solutions in the history. This is much, much faster. If False, 
                             solve the board directly.
        verbose: bool, if True, print out the board each time.
        plot_solution: bool, if True, run plot_board on the first/only solution.
        
outputs: solved Board or list of solved Boards
"""
def solve_board(date=None,board=None,allow_flips = False,
                take_first = True,verbose = False,plot_solution = True):
    if board is None and date is not None:
        board = Board(date=date)
    if board is None and date is None:
        assert False, "One of board or date must be specified to solve."
    output = solve_board_recursor(board,allow_flips,take_first,verbose)
    flip_str = '(without flips)' if not allow_flips else '(with flips)'
    if output is None:
        #no outputs are found for this Board. Possibly because the Board is set up weird, or 
        #flips weren't allowed and they are required for this date.
        print(f'No solution found {flip_str}!')
        if not allow_flips:
            print('perhaps try with "allow_flips = True"?')
        return None
    elif isinstance(output,list):
        #just writing differently if there is only 1 solution (not plural)
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
        
"""
summary: The actual solver, called by solve_board. This solves the board recursively, i.e. try to add a piece 
         to the "top left" unoccupied space, if I succeeded, then try to add one of the remaining pieces to 
         the board with that piece already added. The board is considered solved when it runs out of pieces. 
         Return a Board if take_first is True (and propogates up), or return a list of all solved Boards. Or 
         return None if none of the remaining pieces can be placed at this unoccupied space. (failed)
         
inputs: board: Board, the current board state, may be partially filled out with Pieces
        allow_flips: bool, if True, then let flips be included in process, else exclude them.
        take_first: bool, if True, return the first successful Board. If False, return the list of all solution Boards.
        verbose: bool, if True, print out the board each time.
        
outputs: solved Board or list of solved Boards, or None 
"""
def solve_board_recursor(board,allow_flips,take_first,verbose):
    if verbose and 0:
        print(board.pieces)
        print(board)
        print(board.pieces_remaining)
    #the location to try and place the next Piece.
    x,y = board.find_first_zero()
    #if not allow_flips, this makes the last for loop do nothing.
    flips_list = [False] if not allow_flips else [False,True]
    solutions = []
    #use the list of still available pieces (gets smaller as we get deeper)
    for piece_id in board.pieces_remaining:
        #try each possible rotation
        for rotation in range(4):
            #try flipped and unflipped, if allow_flips.
            for flip in flips_list:
                if piece_id in no_flip and flip:
                    #if the piece doesn't gain anything from flipping, this is an unnecessary path, don't
                    #make a new Board.
                    continue
                elif piece_id in half_symmetry and rotation >= 2:
                    #if the piece doesn't gain anything from rotating by 180, this is an unnecessary path, don't
                    #make a new Board. (rotation 2 = rotation 0, rotation 3 = rotation 1)
                    continue
                #create a piece with these conditions.
                piece = Piece(piece_id,rotation,flip)
                #if this Piece in this orientation doesn't fill the top left corner of their matrix,
                #then shift it over to the left until when we add it, if fills that spot. 
                offset = np.where(piece.matrix[0]==1)[0][0]
                if verbose:
                    print('trying to add:')
                    print(piece_id,rotation,flip,x,y-offset)
                    print(piece)
                new_board = board.insert_piece(piece,x,y-offset)
                if new_board is None:
                    #This means that either the piece doesn't fit in the matrix, or would cover the required day,
                    #or would overlap another piece.
                    if verbose:                   
                        print('fail')
                    continue
                if new_board.pieces_remaining == '':
                    #When a board runs out of pieces, that means you successfully found a solution.
                    return new_board
                #If you get here, you successfully added this Piece to a Board but that didn't finish it. 
                #Now, you should try to add another piece by calling this function again.
                #If we are one level up from a solution, get back a single Board, else get back the list.
                returned = solve_board_recursor(new_board,allow_flips,take_first,verbose)
                if isinstance(returned,Board):
                    #the new Board had one solution, or take_first was True
                    if not take_first:
                        solutions+=[returned]
                    else:
                        return returned
                elif isinstance(returned,list):
                    #the new Board had multiple solutions remaining
                    solutions+=returned
                elif returned is None:
                    #the new Board was unsolvable.
                    continue
                else:
                    assert False, "recieved something that wasn't a Board, a list, or None"
    if len(solutions)>0:
        #we recieved a list of solutions
        return solutions
    else:
        #we did not succeed in solving down any path.
        return None
