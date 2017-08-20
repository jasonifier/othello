def print_board():
    for i,row in enumerate(game_board):
        row_num = 'Row ' + str(i) + ' ->'
        print(row_num, row)

flank_collect = []

def lateral_flank(p,r,c):
    global flank_collect
    while True:
        c += 1
        if game_board[r][c] == 2:
            flank_collect.append((r,c))
        else:
            break

def flip_pieces(flanks, p):
    for r,c in flanks:
        game_board[r][c] = p
    
def move(p):
    global game_board
    r = int(input("Enter row: "))
    c = int(input("Enter column: "))
    if game_board[r][c] == 0:
        game_board[r][c] = p
    lateral_flank(p,r,c)
    flip_pieces(flank_collect,p)
    return print_board()

game_board=list()
for i in range(8):
    game_board.append(list())
for i in range(8):
    for j in range(8):
        game_board[i].append(0)
print_board()
print()

game_board[3][3] = 1
game_board[3][4] = 2
game_board[4][3] = 2
game_board[4][4] = 1

print_board()

result = move(1)
print(result)
print(flank_collect)
