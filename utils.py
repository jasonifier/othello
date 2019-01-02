from copy import copy

def set_to_None(n):
    '''
    Set n variables to the value of None.
    
    :param n: int
    :return: list (containing None), or None
    '''
    if n <= 0:
        raise ValueError('Cannot set zero or less variables.')
    elif n == 1:
        return None
    else:
        return [None] * int(n)


def find_flank_indices(row, color):
    '''
    Given a row of elements in the set {'_', 0, 1} return the
    indices of flanking chances.

    :param row: list
    :param color: int
    :return: list
    '''
    flanker, other, open_spot = set_to_None(3)
    flank_spots = set()
    for i, element in enumerate(row):
        if element == color:
            flanker = i
            if open_spot is None:
                other = set_to_None(1)
            elif (open_spot) and (other is None):
                open_spot = set_to_None(1)
        elif (element != color) and (element in [0,1]):
            other = i
        elif element == '_':
            open_spot = i
            if not (flanker is None) and not (other is None):
                flank_spots.add(open_spot)
            flanker, other = set_to_None(2)
        else:
            raise ValueError('Unaccounted game element on board.')

        if not (other is None) \
           and not (flanker is None) \
           and not (open_spot is None):
            flank_spots.add(open_spot)
            if flanker > open_spot:
                other, open_spot = set_to_None(2)
            else:
                flanker, other, open_spot = set_to_None(3)

    return list(flank_spots)


def get_between_positions(pos_1, pos_2):
    '''
    Provide 2 indices and get a list of the indices between them.

    :param pos_1: int
    :param pos_2: int
    '''
    greater = pos_1 if pos_1 > pos_2 else pos_2
    lesser = pos_1 if pos_1 < pos_2 else pos_2
    return list(range(lesser + 1, greater))


def shift_and_flip_action(cross_section, color, idx, start_idx):
    '''
    With the current row and index of interest, return a boolean
    indicating whether shift should continue.

    :param cross_section: CrossSection instance
    :param color: int
    :param idx: int
    :param start_idx: int
    :return: bool
    '''
    shift = True
    try:
        row = cross_section.get_row()
        if row[idx] == '_':
            shift = False
        elif row[idx] == color:
            conquered = get_between_positions(idx, start_idx)
            for i in conquered:
                cross_section.flip_piece(i, color)
            shift = False
    except IndexError:
        shift = False

    return shift


def flip_pieces(row, index_of_move, color):
    '''
    Given a section of pieces where a player moved, flip the pieces of
    opposing color to finish the turn.

    :param row: list
    :param index_of_move: int
    :return list:
    '''
    c = CrossSection(row)
    c.place_piece(index_of_move, color)
    shift_right = True
    shift_left = True
    start = copy(index_of_move)
    i_right = copy(index_of_move)
    i_left = copy(index_of_move)
    while shift_right or shift_left:
        if shift_right:
            i_right += 1
            shift_right = shift_and_flip_action(c, color, i_right, start)
        if shift_left:
            i_left -= 1
            shift_left = shift_and_flip_action(c, color, i_left, start)
    return c.get_row()


class CrossSection(object):

    def __init__(self, board_section):
        self.row = board_section

    def flip_piece(self, index, to_color):
        row = self.get_row()
        row[index] = to_color
        self.set_row(row)

    def place_piece(self, index, color):
        row = self.get_row()
        row[index] = color
        self.set_row(row)

    def set_row(self, data):
        self.row = data

    def get_row(self):
        return self.row
