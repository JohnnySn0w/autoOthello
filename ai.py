from pprint import pprint
from math import floor
from CONSTANTS import wht, blk, DIRECTIONS

debug1 = False #for minimax
debug2 = False #for a/b prune

###use list methods to ensure the list is manipulated not reassigned


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



############
# AI Funcs #
############

'''
root = { 
    children: { 
        score: -3,
        move: 26,
        children: {}
    },
}

starting function, for base case, then recursive secondary function 
that takes a root node and recurses children into root nodes

'''

def nextNode(board, aiColor, curPlayer, curDepth, maxDepth, root):
    if curDepth <= maxDepth:
        for move in findValidMoves(board, curPlayer):
            toFlip = validateMove(board, curPlayer, move)[1] #return bool, toFliip
            boardCopy = flipPieces(board, curPlayer,toFlip)
            moveNode = {
                'move': move,
                'children': [],
            }
            if curDepth == maxDepth or not findValidMoves(board, curPlayer):
                moveNode['terminal'] = True
                moveNode['score'] = miniMaxScore(boardCopy, aiColor)
            root['children'].append(moveNode)
            nextNode(boardCopy, aiColor, not curPlayer, curDepth+1, maxDepth, moveNode)
    else:
        return

def buildDecisionTree(board, aiColor, depth):
    moveTree = { 'root': True, 'children': [] } #depth 0
    curDepth = 1
    nextNode(board, aiColor, aiColor, curDepth, depth, moveTree) # ai goes in as first player
    if debug1:
        pprint(moveTree)
    return moveTree


#already have scores, move and score can be up-propogated
def evalBranch(root, depth, minORMax):
    if 'terminal' in root:
        return root['move'], root['score']
    #recurse
    elif minORMax:
        maximal = -64
        move = -1
        for child in root['children']:
            getMove, getMax = evalBranch(child, depth+1, False)
            if getMax > maximal:
                maximal = getMax
                move = getMove
                if depth == 1:
                    move = root['move']
        return move, maximal
    else:
        minimal = 64
        move = -1
        for child in root['children']:
            getMove, getMin = evalBranch(child, depth+1, True)
            if getMin < minimal:
                minimal = getMin
                move = getMove
                if depth == 1:
                    move = root['move']
        return move, minimal
    if 'root' in root:
        return root['move'], root['score']

def evaluateTree(tree, aiColor):
    # need aiColor to set initial minimizer/maxmizer and relative score checking
    # always maximizing in first layer
    nextMove, highscore = evalBranch(tree, 0, True)
    print('highest score from here is: %d' % highscore)
    # keep a running total of evaluated nodes, to demonstrate whether a/b prune is on or not
    print('tree eval')
    return nextMove

#a/b pruning will go inside of the evaluation?

# should return new board state
def AIMove(board, aiColor):
    depth = 5 # how deep should ai check moves?
    print('ai moves')
    tree = buildDecisionTree(board, aiColor, depth)
    nextMove = evaluateTree(tree, aiColor)
    valid, toFlip = validateMove(board, aiColor, nextMove)
    if debug1:
        print(nextMove) # figure out what the move is
    if valid:
        board = flipPieces(board, aiColor, toFlip)
        return board, False #need to return whether or not a pass happened
    return board, True # return false if no move made