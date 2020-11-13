from pprint import pprint
from CONSTANTS import wht, blk, DIRECTIONS
from UtilityFuncs import (findValidMoves, validateMove, flipPieces, miniMaxScore)

###use list methods to ensure the list is manipulated not reassigned

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

def buildDecisionTree(board, aiColor, depth, debug1):
    moveTree = { 'root': True, 'children': [] } #depth 0
    curDepth = 1
    nextNode(board, aiColor, aiColor, curDepth, depth, moveTree) # ai goes in as first player
    if debug1:
        pprint(moveTree)
    return moveTree


#already have scores, move and score can be up-propogated
def evalBranch(root, depth, minORMax, movesEvaluated, debug2, a=0, b=0):
    if 'terminal' in root:
        return root['move'], root['score'], movesEvaluated + 1
    #recurse
    elif minORMax:
        maximal = -64
        move = -1
        for child in root['children']:
            getMove, getMax, movesEvaluated = evalBranch(child, depth+1, False, movesEvaluated, debug2, a, b)
            if getMax > maximal:
                maximal = getMax
                move = getMove
                if depth == 1:
                    move = root['move']
            if debug2:
                a = max((a, maximal))
                if a >= b:
                    break
        return move, maximal, movesEvaluated+1
    else:
        minimal = 64
        move = -1
        for child in root['children']:
            getMove, getMin, movesEvaluated = evalBranch(child, depth+1, True, movesEvaluated, debug2, a, b)
            if getMin < minimal:
                minimal = getMin
                move = getMove
                if depth == 1:
                    move = root['move']
            if debug2:
                b = max((b, minimal))
                if b <= a:
                    break
        return move, minimal, movesEvaluated+1
    if 'root' in root:
        return root['move'], root['score'], movesEvaluated

def evaluateTree(tree, aiColor, debug2):
    # need aiColor to set initial minimizer/maxmizer and relative score checking
    # always maximizing in first layer
    movesEvaluated = -1
    nextMove, highscore, movesEvaluated = evalBranch(tree, 0, True, movesEvaluated, debug2)
    print('Number of moves evaluated: %d' % movesEvaluated)
    print('highest score from here is: %d' % highscore)
    # keep a running total of evaluated nodes, to demonstrate whether a/b prune is on or not
    return nextMove

#a/b pruning will go inside of the evaluation?

# should return new board state
def AIMove(board, aiColor, debugs):
    depth = 2 # how deep should ai check moves? 5 for a reasonable challenge and speed, 6 is a slow killer, 7 is too slow to bother(and will likely win)
    # multithreading the move tree analysis would probs help speed a lot
    print('ai moves')
    tree = buildDecisionTree(board, aiColor, depth, debugs['debug1'])
    nextMove = evaluateTree(tree, aiColor, debugs['debug2'])
    valid, toFlip = validateMove(board, aiColor, nextMove)
    if debugs['debug1']:
        print("Ai's move to: %d" % nextMove) # figure out what the move is
    if valid:
        board = flipPieces(board, aiColor, toFlip)
        return (board, False, debugs) #need to return whether or not a pass happened
    return (board, True, debugs) # return false if no move made