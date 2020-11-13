from CONSTANTS import (
    blk, wht, space, vertPipe, TIPPYTOP, TOP, BOTTOM, ALTROW, perMoveQuery
)

# gui funcs

def renderRow(rowNumber, board):
    row = chr(rowNumber*1+65) + space + vertPipe
    for spot in board[rowNumber*8:rowNumber*8+8]:
        row += space + spot + space + vertPipe
    print(row)

def printScore(board):
    score = [0, 0] 
    for spot in board:
        if spot == blk:
            score[0] += 1
        if spot == wht:
            score[1] += 1
    print(blk + " Black: " + str(score[0]) + "\n" + wht + " White: " + str(score[1]))
    return score

def buildBoard(board):
    print(TIPPYTOP)
    print(TOP)
    renderRow(0, board)
    for row in range(1,8):
        print(ALTROW)
        renderRow(row, board)
    print(BOTTOM)
    printScore(board)


