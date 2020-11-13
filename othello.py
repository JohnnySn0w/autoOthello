
''' autoOthello, an implementation of Othello that supports 2 players, and also has 1 player mode vs an AI player who uses MiniMax, optionally with A/B pruning
 * Name: Michael Mahan
 * Student ID: 102-36-293
 * November 10, 2020
 * Assignment 3
 * Class: CSC-475
 * Professor: Dr. Mike O'Neal
'''
import sys
import re
from CONSTANTS import (DIRECTIONS, welcome, twoPlayerQuery, perMoveQuery, pieceRow, pieceColumn, wht, blk, gameEndMessage)
from GUI import printScore, buildBoard
from ai import AIMove
from UtilityFuncs import getPlayerPieceColor, findValidMoves, validateMove, flipPieces, miniMaxScore, clear

#########################
# dict resolution funcs #
#########################
def singlePlayer(ignore):
    return True

def twoPlayer(ignore):
    return False

def AIBlk(ignore):
    return False

def AIWht(ignore):
    return True

def preMoveD1(debugs):
    return { 'debug1': not debugs['debug1'], 'debug2': debugs['debug2']}

def preMoveD2(debugs):
    return { 'debug1': debugs['debug1'], 'debug2': not debugs['debug2']}

def preMoveD3(debugs):
    return { 'debug1': True, 'debug2': True}

def preMoveD4(debugs):
    return { 'debug1': False, 'debug2': False}

def preMoveD5(debugs):
    return { 'debug1': not debugs['debug1'], 'debug2': not debugs['debug2']}

def preMoveMove(debugs):
    return debugs

def default(redoFunc, params=()):
    clear()
    redoFunc(*params)

inputParse = {
    '1': singlePlayer,
    '2': twoPlayer,
    'one': singlePlayer,
    'two': twoPlayer,
    'one player': singlePlayer,
    'two players': twoPlayer,
}

aiChoice = {
    'blk': AIBlk,
    'wht': AIWht,
    'black': AIBlk,
    'white': AIWht,
    'first': AIBlk,
    'second': AIWht,
    '1': AIBlk,
    '2': AIWht,
}

passingChoice = {
    'y': True,
    'yes': True,
    'correct': True,
    'affirmative': True,
    'n': False,
    'no': False,
    'negative': False,
    'incorrect': False,
}

preMoveParse = {
    'move': preMoveMove,
    'debug1': preMoveD1,
    '1': preMoveD1,
    'debug2': preMoveD2,
    '2': preMoveD2,
    'bothon': preMoveD3,
    'on': preMoveD3,
    'bothoff': preMoveD4,
    'off': preMoveD4,
    'swap': preMoveD5,
}


def initBoard():
    board = [' ' for num in range(64)] #init all spaces to blank space
    #white black 
    #black white
    board[27] = wht
    board[28] = blk
    board[35] = blk
    board[36] = wht
    return board

def aiTurn(board, curPlayer, vsAI, aiColor, passes, debugs):
    curScore = miniMaxScore(board, aiColor)
    if (passes > 0) and (curScore > 0): # if human passes, and ai has advantage, ai win
        return endMenu(board)
    board, passed, debugs = AIMove(board, aiColor, debugs)
    if passed:
        passes+=1
        if passes == 2:
            endMenu(board)
            return
        gameMenu(board, not curPlayer, vsAI, aiColor, passes, debugs)
    gameMenu(board, not curPlayer, vsAI, aiColor, 0, debugs)

#########
# menus #
######### 

def moveMenu(debugs):
    chosen = input(perMoveQuery).lower()
    return preMoveParse.get(chosen, preMoveParse['move'])(debugs)

def endMenu(board):
    #print score
    printScore(board)
    print(gameEndMessage)
    again = input('Play Again?(y/N): ')
    again = passingChoice.get(again.lower(), False)
    if again:
        mainMenu()
    sys.exit(0)

def mainMenu():
    clear()
    board = initBoard()
    curPlayer = False #False is black
    vsAI = False #default 2p game
    aiColor = True

    userSelect = input(welcome)
    vsAI = inputParse.get(userSelect.lower(), default)(mainMenu) # 1p or 2p
    if vsAI:
        aiPick = input(twoPlayerQuery)
        aiColor = aiChoice.get(aiPick.lower(), default)(mainMenu) # set ai color
        #implicitly thru gameMenu() logic, player color is opposite of ai color
    gameMenu(board, curPlayer, vsAI, aiColor)

def gameMenu(board, curPlayer, vsAI=False, aiColor=True, passes=0, debugs={ 'debug1': False, 'debug2': False }):
    # clear()
    buildBoard(board)
    if ' ' not in board:
        endMenu(board)
    if passes > 0:
        print('Last player passed')
    print('Current Player is: ' + getPlayerPieceColor(curPlayer))
    if vsAI and (curPlayer != aiColor):
            debugs = moveMenu(debugs)
    if vsAI and (curPlayer == aiColor): #if 1player
        # runs if ai goes after player skips
        aiTurn(board, curPlayer, vsAI, aiColor, passes, debugs)
    else:
        row = input(pieceRow).upper()
        column = input(pieceColumn)
        valid = False

        # input sanitize row
        if re.match(r'^[A-Ha-h]$', row):
            row = ord(row) - 64
        else:
            row = -1

        # input sanitize column
        if re.match(r'^[1-8]$', column):
            column = int(column)
        else:
            column = -1

        if (1 <= row <= 8) and (1<= column <= 8):
            moveIndex = (row-1)*8+(column-1)
            valid, toFlip = validateMove(board, curPlayer, moveIndex)

        if valid:
            board = flipPieces(board, curPlayer, toFlip) # commit to move
            curPlayer = not curPlayer
            if vsAI and (curPlayer and aiColor): #if 1player
                aiTurn(board, curPlayer, vsAI, aiColor, passes, debugs)
            else: #if 2player
                gameMenu(board, curPlayer, vsAI, aiColor)
        else: #invalid input either means a pass or an oof
            isPassing = input('Invalid Move. Did you mean to pass?(Y/n)')
            passing = passingChoice.get(isPassing, True)
            if passing:
                passes += 1
                if passes == 2:
                    endMenu(board)
                    return
                gameMenu(board, not curPlayer, vsAI, aiColor, passes, debugs)
            else:
                gameMenu(board, curPlayer, vsAI, aiColor, 0, debugs)


def main():
    mainMenu()

if __name__ == "__main__":
    main()