from othello import findValidMoves, getPlayerPieceColor


debug1 = False #for minimax
debug2 = False #for a/b prune

###use list methods to ensure the list is manipulated not reassigned

def miniMaxScore(board, maximizer):
    highscore = 0
    for spot in board:
        if spot == getPlayerPieceColor(maximizer):
            highscore += 1
            continue
        if spot == getPlayerPieceColor(not maximizer):
            highscore -= 1
    return highscore

def buildDecisionTree(board, aiColor, depth):
    moveTree = []
    subTree = []
    for layer in depth:
        for newRoot in moveTree[layer]:
            for move in findValidMoves(board, aiColor):
                newRoot.append([miniMaxScore(board, aiColor), move])

def evaluateTree(tree):
    pass


#a/b pruning will go inside of the evaluation

# should return new board state
def AIMove(board, aiColor):
    depth = 2 # how deep should ai check moves?
    print('ai moves')
    buildDecisionTree(board, aiColor, depth)
    return board, True #need to return whether or not a pass happened