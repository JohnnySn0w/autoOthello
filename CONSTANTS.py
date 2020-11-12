DIRECTIONS = {
    'diagBackUp': -9,
    'up': -8,
    'diagForwardUp': -7,
    'left': -1,
    'right': 1,
    'diagForwardDown': 7,
    'down': 8,
    'diagBackDown': 9,
}

# pieces of the board
wht = u"\u25CF" 
blk = u"\u25CB"
vertPipe = '│'
horizPipe = '─'
tL = '┌'
bL = '└'
tR = '┐'
bR = '┘'
topT = '┬'
botT = '┴'
leftT = '├'
rightT = '┤'
space = ' '
cross = '┼'

# starting index of each row
rows = {
    'A': 0,
    'B': 8,
    'C': 16,
    'D': 24,
    'E': 32,
    'F': 40,
    'G': 48,
    'H': 64,
}

#these rows are always the same
TIPPYTOP = (space*3) + ' 1   2   3   4   5   6   7   8'
TOP = (space*2) + tL + (horizPipe*3 + topT)*7 +horizPipe*3 + tR
BOTTOM = (space*2) + bL + (horizPipe*3 + botT)*7 +horizPipe*3 + bR
ALTROW = (space*2) + leftT + (horizPipe*3 + cross)*7 + horizPipe*3 + rightT

#menu messages
welcome = "AutoOthello supports both two player and single player experiences.\nPlease indicate how many players there will be(1 or 2):"
twoPlayerQuery = "Will AI go first or second? (black always goes first)"
pieceRow = "What row would you like to place your piece on?(A-H)"
pieceColumn = "What column would you like to place your piece on?(1-8)"
gameEndMessage = "GAME END"

# ai related switches
debug1 = False #for minimax
debug2 = False #for a/b prune
abOn = { 'isABOn': False } #making this a dict lets it be passed by obj ref, and can be consistently accessed.