from copy import copy
from operator import itemgetter
from collections import OrderedDict
from utils import *

# find_flank_indices(row, color)
# flip_pieces(row, index_of_move, color)
# index_mapper(ordered_hash_map)

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
            loc_val_map = {(i,j): value for j, value in enumerate(row)}
            grid_map.update(loc_val_map)
        return grid_map
    
    def set_grid_element(self, row_index, col_index, color):
        self.grid[row_index][col_index] = color

    def get_diagonals(self):
        diagonals = []
        grid_map = self.get_grid_map()
        main_diagonal = {(x, y): grid_map[(x, y)] for x, y in grid_map.keys() if x == y}
        diagonals.append(main_diagonal)

        other_diagonals = []
        more_diagonals = ['above_main','below_main']
        for diag_type in more_diagonals:
            var_start = 1
            anchor_range = range(0,8)
            while var_start <= 7:
                var = copy(var_start)
                curr_diagonal = {}
                for k in anchor_range:
                    try:
                        if diag_type == 'above_main':
                            curr_diagonal.update({(k, var): grid_map[(k, var)]})
                        elif diag_type == 'below_main':
                            curr_diagonal.update({(var, k): grid_map[(var, k)]})
                        else:
                            raise ValueError('Not a correct diagonal identified on the gameboard.')
                    except KeyError:
                        pass
                    finally:
                        var += 1
                other_diagonals.append(curr_diagonal)
                var_start += 1
        diagonals.extend(other_diagonals)

        return diagonals                                   

    def get_opposite_diagonals(self):
        diagonals = []
        grid_map = self.get_grid_map()
        main_diagonal = {(x, y) : grid_map[(x, y)] for x, y in grid_map.keys() if y == 7 - x}
        diagonals.append(main_diagonal)

        other_diagonals = []
        more_diagonals = ['above_main','below_main']
        for diag_type in more_diagonals:
            if diag_type == 'above_main':
                var_start = 6
                anchor_range = range(0,8)
            elif diag_type == 'below_main':
                var_start = 1
                anchor_range = list(range(0,8))
                anchor_range.reverse()
            else:
                raise ValueError('Not a correct diagonal identified on the gameboard.')
            while (var_start >= 0 and diag_type == 'above_main') or (var_start <= 7 and diag_type == 'below_main'):
                var = copy(var_start)
                curr_diagonal = {}
                for k in anchor_range:
                    try:
                        if diag_type == 'above_main':
                            curr_diagonal.update({(k, var): grid_map[(k, var)]})
                        elif diag_type == 'below_main':
                            curr_diagonal.update({(var, k): grid_map[(var, k)]})
                        else:
                            raise ValueError('Not a correct diagonal identified on the gameboard.')
                    except KeyError:
                        pass
                    finally:
                        if diag_type == 'above_main':
                            var -= 1
                        elif diag_type == 'below_main':
                            var += 1
                        else:
                            raise ValueError('Not a correct diagonal identified on the gameboard.')
                other_diagonals.append(curr_diagonal)
                if diag_type == 'above_main':
                    var_start -= 1
                elif diag_type == 'below_main':
                    var_start += 1
                else:
                    raise ValueError('Not a correct diagonal identified on the gameboard.')
        diagonals.extend(other_diagonals)
        
        return diagonals

    def get_axis(self, direction=None):
        if direction is None or not direction in ['horizontal','vertical']:
            raise ValueError('Use a valid direction, as in "vertical" or "horizontal".')
        axis = []
        grid_map = self.get_grid_map()
        anchor_range = range(0,8)
        for label in anchor_range:
            var_range = range(0,8)
            curr_section = {}
            for v in var_range:
                if direction == 'horizontal':
                    curr_section.update({(label, v): grid_map[(label, v)]})
                if direction == 'vertical':
                    curr_section.update({(v, label): grid_map[(v, label)]})
            axis.append(curr_section)
        
        return axis
                   
    def _sort_cross_sections(self, sections, use_x=True, use_y=False):
        cross_sections = []
        for section in sections:
            section_list = [(k[0], k[1], v) for k, v in section.items()]
            if use_x and use_y:
                raise ValueError('Only allows either use_x OR use_y, not both.')
            else:
                if use_x:
                    section_sorted = sorted(section_list, key=itemgetter(0))
                elif use_y:
                    section_sorted = sorted(section_list, key=itemgetter(1))
                else:
                    raise ValueError('Identify one argument from use_x or use_y as True, but not both.')
            cross_section = OrderedDict()
            for x, y, value in section_sorted:
                cross_section[(x, y)] = value
            cross_sections.append(cross_section)
        return cross_sections            

    def get_cross_sections(self, slice_types=['vertical','horizontal','diagonals','opposite_diagonals']):
        all_sections = {}
        for curr_type in slice_types:
            if curr_type == 'vertical':
                elements = self.get_axis(direction=curr_type)
                aligned = self._sort_cross_sections(elements)
            elif curr_type == 'horizontal':
                elements = self.get_axis(direction=curr_type)
                aligned = self._sort_cross_sections(elements, use_x=False, use_y=True)
            elif curr_type == 'diagonals':
                elements = self.get_diagonals()
                aligned = self._sort_cross_sections(elements)
            elif curr_type == 'opposite_diagonals':
                elements = self.get_opposite_diagonals()
                aligned = self._sort_cross_sections(elements)
            else:
                raise ValueError('Invalid input for slice_types: not in "vertical", "horizontal", "diagonals", "opposite_diagonals"')
            all_sections[curr_type] = aligned
        return all_sections


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
             
    def make_move(self, flanks):
        # handle TypeError ValueError with user input
        eligible_move = False
        while not eligible_move:
            r = input('Enter row num to place piece: ')
            c = input('Enter col num to place piece: ')
            move_coords = (int(r), int(c))
            if move_coords in flanks:
                eligible_move = True
            else:
                print('Select from possible flanks!')
        self.game_board.grid[int(r)][int(c)] = self.color
        cross_sections = self.game_board.get_cross_sections()
        for k, cross_section in cross_sections.items():
            for row in cross_section:
                if move_coords in row:
                    spaces = list(row.values())
                    idx_to_pair = index_mapper(row)
                    for i, pair in idx_to_pair.items():
                        if move_coords == pair:
                            move_index = i
                            break
                    flipped = flip_pieces(spaces, move_index, self.color)
                    for idx, piece in enumerate(flipped):
                        row, col = idx_to_pair[idx]
                        self.game_board.set_grid_element(row, col, piece)


class Othello(object):
    
    def __init__(self, game_board, player_one, player_two):
        self.p1 = player_one
        self.p2 = player_two
        self.game_board = game_board
        self.mover = None
        self.move_count = 0

    def play(self):
        '''
        Initiate game play of Othello with one gameboard and 2 players.
        '''
        remove_logs()
        othello_logger('START OF GAME.')
        while not self._game_over():
            self.start_turn()
            self.game_board.display()
            flanks = self.get_flanks()
            if flanks:
                self.mover.make_move(flanks)
            else:
                print('No flanks for this turn!')
            self.switch_turn()  
        self.game_board.display()
        scores = self.calculate_scores()
        winner = max(scores.items(), key=itemgetter(1))[0]
        print('WINNER:', winner) 
 
    def _game_over(self):
        board_count = 0
        for hrow in self.game_board.grid:
            for element in hrow:
                if element == 0 or element == 1:
                    board_count += 1
        if board_count == 64:
            return True
        else:
            return False

    def calculate_scores(self):
        scores = {'PLAYER ONE': 0, 'PLAYER TWO': 0}
        for hrow in self.game_board.grid:
            for element in hrow:
                if element == 1:
                    scores['PLAYER ONE'] += 1
                elif element == 0:
                    scores['PLAYER TWO'] += 1
                else:
                    raise ValueError('Board should only contain boolean values (0 or 1).')
        return scores

    def start_turn(self):
        if self.p1.turn:
            self.mover = self.p1
        else:
            self.mover = self.p2
        self.display_current_active_player()
        self.move_count += 1
        log_string = 'MOVE: ' + str(self.move_count)
        print(log_string)
        othello_logger('\n' + log_string)
        if self.p1.turn:
            othello_logger('PLAYER: ONE')
        if self.p2.turn:
            othello_logger('PLAYER: TWO')
          

    def get_flanks(self):
        cross_sections = self.game_board.get_cross_sections()
        flanks = set()
        for k, section in cross_sections.items():
            for row in section:
                pieces = list(row.values())
                idx_to_pair = index_mapper(row)
                flank_chances = find_flank_indices(pieces, self.mover.color)
                if flank_chances:
                    pairs = [idx_to_pair[idx] for idx in flank_chances]
                    for pair in pairs:
                        flanks.add(pair)
        print(list(flanks))
        return list(flanks)

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
#    print()
#    cross_sections = g.get_cross_sections()
#    for key, section in cross_sections.items():
#        print(key)
#        print(len(section))
#        print(section)
#        print()
