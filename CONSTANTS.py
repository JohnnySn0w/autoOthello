DIRECTIONS = {
    'diagBackUp': -7,
    'up': -6,
    'diagForwardUp': -5,
    'left': -1,
    'right': 1,
    'diagForwardDown': 5,
    'down': 6,
    'diagBackDown': 7,
}

# pieces of the board
blk = u"\u25CF" 
wht = u"\u25CB"
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
TIPPYTOP = (space*3) + (str(num) + ' ' for num in range(8)) 
TOP = (space*2) + tL + (horizPipe + topT)*7 +horizPipe + tR
BOTTOM = (space*2) + bL + (horizPipe + topT)*7 +horizPipe + bR
ALTROW = (space*2) + leftT + (horizPipe + cross)*7 + horizPipe + rightT

#menu messages
welcome = "AutoOthello supports both two player and single player experiences.\nPlease indicate how many players there will be(1 or 2):"
twoPlayerQuery = "Will AI go first or second? (black always goes first)"
pieceRow = "What row would you like to place your piece on?(A-H)"
pieceColumn = "What column would you like to place your piece on?(1-8)"
gameEndMessage = "GAME END"