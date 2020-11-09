import CONSTANTS

# gui funcs

def renderAesthRow(aesthRow):
    print(aesthRow)

def renderRow(rowNumber, board):
    row = chr(rowNumber*1+65) + CONSTANTS.space + CONSTANTS.vertPipe
    for spot in board[row*8:row*8+8]:
        row += CONSTANTS.space + spot + CONSTANTS.space
    print(row)

def printScore(board):
    score = [0, 0] 
    for spot in board:
        if spot == CONSTANTS.blk:
            score[0] += 1
        if spot == CONSTANTS.wht:
            score[1] += 1
    print("Black: " + score[0] + "\nWhite: " + score[1])

def buildBoard(board):
    renderAesthRow(CONSTANTS.TIPPYTOP)
    renderAesthRow(CONSTANTS.TOP)
    renderRow(0, board)
    for row in range((board.length-8)/8):
        renderAesthRow(CONSTANTS.ALTROW)
        renderRow(row, board)
    renderAesthRow(CONSTANTS.BOTTOM)
    printScore(board)


