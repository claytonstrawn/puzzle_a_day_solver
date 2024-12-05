import numpy as np
import matplotlib.pyplot as plt

#This matrix represents the default shape of the Board. The 1s on the right are because there are only 6 months per row
#and the 1s on the bottom are because there are 31 = 4*7 + 3 days per month so there are 4 extra slots.
#total empty locations = 49 - 6 = 43, total pieces = 5*7 + 6 = 41, leaving 2 blanks (month and day)
default_board = np.array([[0,0,0,0,0,0,1],\
                          [0,0,0,0,0,0,1],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,1,1,1,1]])
#This dictionary connects the piece_ids (characters) to the basic matrix shapes of the 8 pieces.
#They are generally in order of difficulty to place (by my estimation from playing the game manually)
#This means they will be added in this order, hopefully saving time.
piece_matrices = {
          'a': np.array([[1,1,0],\
                         [0,1,0],\
                         [0,1,1]]),\
          'b': np.array([[1,0,1],\
                         [1,1,1]]),\
          'c': np.array([[1,1,1],\
                         [1,1,1]]),\
          'd': np.array([[0,0,1,1],\
                         [1,1,1,0]]),\
          'e': np.array([[1,1,1,1],\
                         [0,0,1,0]]),\
          'f': np.array([[1,1,1,1],\
                         [1,0,0,0]]),\
          'g': np.array([[1,1,1],\
                         [0,0,1],\
                         [0,0,1]]),\
          'h': np.array([[1,1,0],\
                         [1,1,1]])
         }
#These three pieces never gain anything by flipping over. They are the same shape either way.
#This is used to skip trying the piece again flipped over.
no_flip = 'bcg'

#These two pieces gain nothing by rotating 180 degrees. They are the same shape either way.
#This is used to skip trying the piece again flipped over.
half_symmetry = 'ac'

#This is used to set the colors in the plot so no matter the piece order each piece keeps a consistent 
#color.
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
colors_dict = {}
for i,piece in enumerate(piece_matrices):
    colors_dict[piece] = colors[i]

#Dictionary mapping month with its location on the Board
months = {'January':(0,0),
          'February':(0,1),
          'March':(0,2),
          'April':(0,3),
          'May':(0,4),
          'June':(0,5),
          'July':(1,0),
          'August':(1,1),
          'September':(1,2),
          'October':(1,3),
          'November':(1,4),
          'December':(1,5),
         }

#Dictionary mapping month with the number of days in that month.
#So you can skip or warn for days that don't exist.
ndays = {'January':31,
          'February':29,
          'March':31,
          'April':30,
          'May':31,
          'June':30,
          'July':31,
          'August':31,
          'September':30,
          'October':31,
          'November':30,
          'December':31,
         }
