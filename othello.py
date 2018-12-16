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

    def get_possible_flanks(self):
        '''
        Retrieve the possible flanks on the board for
        the current player.  These are the only possible
        moves available for any player at any time.
        These update at the start of every turn.
        '''
        return None      

    def get_grid_map(self):
        grid_map = {}
        for i, row in enumerate(self.grid):
            loc_val_map = {(i,j): value for j, value in enumerate(row) if value != '_'}
            grid_map.update(loc_val_map)
        return grid_map
    

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
        # handle TypeError ValueError with user input
        r = input('Enter row num to place piece: ')
        c = input('Enter col num to place piece: ')
        self.game_board.grid[int(r)][int(c)] = self.color


class Othello(object):
    
    def __init__(self, game_board, player_one, player_two):
        self.p1 = player_one
        self.p2 = player_two
        self.game_board = game_board
        self.mover = None

    def play(self):
        '''
        Initiate game play of Othello with one gameboard and 2 players.
        '''
        for _ in range(6):
            # play a sample round where each player
            # gets three turns to place pieces on the board
            self.start_turn()
            self.game_board.display()
            self.mover.make_move()
            self.switch_turn()
    
    def start_turn(self):
        if self.p1.turn:
            self.mover = self.p1
        else:
            self.mover = self.p2
        self.display_current_active_player()

    def switch_turn(self):
        if self.p1.turn:
            self.p1.turn = 0
            self.p2.turn = 1
        else:
            self.p2.turn = 0
            self.p1.turn = 1

    def display_current_active_player(self):
        if self.mover == self.p1:
            print('\nTURN: PLAYER ONE\n')
        else:
            print('\nTURN: PLAYER TWO\n')


if __name__ == '__main__':
    g = GameBoard()
    g.prepare()
    p1 = Player(g, move_first=True)
    p2 = Player(g, move_first=False)
    othello = Othello(g, p1, p2)
    othello.play()
    print(g.get_grid_map())
