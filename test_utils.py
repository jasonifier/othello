from copy import copy
import sys
from utils import *

row = input('Enter a row: ').split()
mod_row = []
for k in row:
    try:
        mod_row.append(int(k))
    except ValueError:
        mod_row.append(k)
row = copy(mod_row)
print()

print(str(find_flank_indices(row, 0)))
print()
x = input('Which index to use? ')

print(' '.join([str(element) for element in flip_pieces(row, int(x), 0)]))
