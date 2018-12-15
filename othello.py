from copy import copy

class GameBoard(object):
    
    def __init__(self):
        self.hdim = 8
        self.vdim = 8
        row = ['_'] * self.vdim

        start_grid = []
        for _ in range(self.hdim):
            start_grid.append(copy(row))
        self.grid = start_grid        

        self.black_piece = 1
        self.white_piece = 0

    def display(self):
        '''
        Method to print the current grid to the screen.
        '''
        for row in self.grid:
            row_str = ' '.join([str(element) for element in row])
            print(row_str)

    def prepare(self):
        '''
        Prepare board by alternating color pieces in a
        2x2 box positioned in the center of the board.
        '''
        self.grid[3][4] = self.white_piece
        self.grid[4][3] = self.white_piece
        self.grid[3][3] = self.black_piece
        self.grid[4][4] = self.black_piece


class Player(object):
    
    def __init__(self, game_board, move_first=None):
        self.game_board = game_board
        if move_first is None:
            raise ValueError('identify player as first or second mover with "move_first" keyword (boolean)')
        elif move_first:
            self.color = game_board.black_piece
            self.turn = 1
        else:
            self.color = game_board.white_piece
            self.turn = 0

    def see_board(self):
        try:
            self.game_board.display()
        except AttributeError as e:
            print(e, 'Not a GameBoard.')
             
    def make_move(self):
        # handle TypeError Value Error with user input
        r = input('Enter row num to place piece: ')
        c = input('Enter col num to place piece: ')
        self.game_board.grid[int(r)][int(c)] = self.color


g = GameBoard()
g.prepare()
g.display()
p1 = Player(g, move_first=True)
p2 = Player(g, move_first=False)
print(p1.turn)
print(p2.turn)
p1.make_move()
p1.see_board()
p2.see_board()
p2.make_move()
p2.see_board()
p1.see_board()
#def print_board():
#    for i,row in enumerate(game_board):
#        row_num = 'Row ' + str(i) + ' ->'
#        print(row_num, row)

#flank_collect = []

#def lateral_flank(p,r,c):
#    global flank_collect
#    while True:
#        c += 1
#        if game_board[r][c] == 2:
#            flank_collect.append((r,c))
#        else:
#            break
#
#def flip_pieces(flanks, p):
#    for r,c in flanks:
#        game_board[r][c] = p
#    
#def move(p):
#    global game_board
#    r = int(input("Enter row: "))
#    c = int(input("Enter column: "))
#    if game_board[r][c] == 0:
#        game_board[r][c] = p
#    lateral_flank(p,r,c)
#    flip_pieces(flank_collect,p)
#    return print_board()
#
#game_board=list()
#for i in range(8):
#    game_board.append(list())
#for i in range(8):
#    for j in range(8):
#        game_board[i].append(0)
#print_board()
#print()
#
#game_board[3][3] = 1
#game_board[3][4] = 2
#game_board[4][3] = 2
#game_board[4][4] = 1

#print_board()

#result = move(1)
#print(result)
#print(flank_collect)
