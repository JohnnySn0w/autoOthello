from math import floor
from CONSTANTS import wht, blk, DIRECTIONS


#################
# utility funcs #
#################

#done
# returns player color code
def getPlayerPieceColor(player):
    if player:
        return wht
    else:
        return blk

def getRowRange(moveIndex):
    row = floor(moveIndex / 8) #rounds down bc remainder is just column num
    return (row*8, row*8+7)

def nextRow(directionRow, rowRange):
    if directionRow <= 3: #backup, up, forwardup
        #row above
        rowRange = (rowRange[0]-8, rowRange[1]-8)
    elif directionRow > 5: #backdown, down, forwarddown
        #next row
        rowRange = (rowRange[0]+8, rowRange[1]+8)
    return rowRange

#done
#flips all pieces sent
def flipPieces(board, curPlayer, toFlip):
    boardCopy = board.copy()
    toColor = getPlayerPieceColor(curPlayer) #is actually the piece character code
    for piece in toFlip:
        boardCopy[piece] = toColor
    return boardCopy

def nextSpace(board, curPlayer, direction, directionRow, rowRange, toFlip, moveIndex):
    # row will be where the move is
    if (rowRange[0] <= moveIndex <= rowRange[1]) and (0 <= moveIndex < len(board)): # if the space's index is within the correct row
        # print('current space(%d) occupied by: %s' % (moveIndex, board[moveIndex]))
        if board[moveIndex] == getPlayerPieceColor(not curPlayer): # if piece color is opposite curplayer, continue pathing
            toFlip.append(moveIndex) #add current first, so if next is empty, it gets cancelled too
            toFlip = nextSpace(board, curPlayer, direction, directionRow, nextRow(directionRow, rowRange) , toFlip, moveIndex+DIRECTIONS[direction]) # "I frickin love recursion" -Orteil42
            if not toFlip: #empty lists are falsy
                # print('toFlip reset')
                toFlip.clear()
            return toFlip
        if board[moveIndex] == getPlayerPieceColor(curPlayer): # if piece color is same curplayer, finish path
            # print('found path in direction:' + direction)
            return toFlip
        if board[moveIndex] == ' ': # if space empty, cancel the whole path
            # print('no tiles in direction(NOEND):' + direction)
            toFlip.clear()
            return toFlip
    else:
        # print('no tiles in direction(OOB):' + direction)
        toFlip.clear()
        return toFlip # cancel path, out of bounds

def validateMove(board, curPlayer, moveIndex):
    if board[moveIndex] == ' ':
        toFlip = [moveIndex] #put in the initial move bc it needs to be placed
        directionRow = 1
        for direction in DIRECTIONS: #iter all 8 directions keys, bc even if one causes flips, so may another
            spaces = []
            rowRange = nextRow(directionRow, getRowRange(moveIndex)) # current row
            spaces = (nextSpace(board, curPlayer, direction, directionRow, rowRange, spaces, moveIndex+DIRECTIONS[direction]))
            if spaces:
                toFlip.extend(spaces)
            directionRow += 1
        if len(toFlip) == 1:
            return False, []
        return True, toFlip
    return False, []

def findValidMoves(board, curPlayer):
    validMoves = []
    for spot in range(len(board)):
        isValid, toFlip = validateMove(board, curPlayer, spot)
        if isValid:
            validMoves.append(toFlip[0]) #if a valid move, the first index will be the move
    return validMoves

def miniMaxScore(board, color):
    highscore = 0
    for spot in board:
        if spot == getPlayerPieceColor(color):
            highscore += 1
            continue
        if spot == getPlayerPieceColor(not color):
            highscore -= 1
    return highscore