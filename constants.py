import numpy as np
import matplotlib.pyplot as plt

default_board = np.array([[0,0,0,0,0,0,1],\
                          [0,0,0,0,0,0,1],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,0,0,0,0],\
                          [0,0,0,1,1,1,1]])
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
no_flip = 'bcg'
half_symmetry = 'ac'

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
colors_dict = {}
for i,piece in enumerate(piece_matrices):
    colors_dict[piece] = colors[i]

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
