
''' autoOthello, an implementation of Othello that supports 2 players, and also has 1 player mode vs an AI player who uses MiniMax, optionally with A/B pruning
 * Name: Michael Mahan
 * Student ID: 102-36-293
 * November 10, 2020
 * Assignment 3
 * Class: CSC-475
 * Professor: Dr. Mike O'Neal
'''
import os
import sys
import re
from CONSTANTS import (DIRECTIONS, welcome, twoPlayerQuery, pieceRow, pieceColumn, wht, blk, gameEndMessage)
import GUI
from ai import AIMove, getPlayerPieceColor, findValidMoves, validateMove, flipPieces

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def singlePlayer(ignore):
    return True

def twoPlayer(ignore):
    return False

def AIBlk(ignore):
    return False

def AIWht(ignore):
    return True

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

def initBoard():
    board = [' ' for num in range(64)] #init all spaces to blank space
    #white black 
    #black white
    board[27] = wht
    board[28] = blk
    board[35] = blk
    board[36] = wht
    return board

#########
# menus #
######### 

def endMenu(board):
    #print score
    GUI.printScore(board)
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
    print(vsAI)
    if vsAI:
        aiPick = input(twoPlayerQuery)
        aiColor = aiChoice.get(aiPick.lower(), default)(mainMenu) # set ai color
        #implicitly thru gameMenu() logic, player color is opposite of ai color
    gameMenu(board, curPlayer, vsAI, aiColor)

def gameMenu(board, curPlayer, vsAI=False, aiColor=True, passes=0):
    clear()
    GUI.buildBoard(board)
    if passes > 0:
        print('Last player passed')
    print('Current Player is: ' + getPlayerPieceColor(curPlayer))
    print('vsai: %s curPlayer %s aiColor %s' % (vsAI, curPlayer, aiColor))
    if vsAI and (curPlayer == aiColor): #if 1player
            board, passed = AIMove(board, aiColor)
            print('ai playing')
            if passed:
                passes+=1
                if passes == 2:
                    endMenu(board)
                    return
                gameMenu(board, not curPlayer, vsAI, aiColor, passes)
            print('ai played')
            gameMenu(board, not curPlayer, vsAI, aiColor)
    else:
        row = input(pieceRow).upper()
        column = input(pieceColumn)
        valid = False
        # print(findValidMoves(board, curPlayer))

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
                board, passed = AIMove(board, aiColor)
                print('ai playing')
                if passed:
                    passes+=1
                    if passes == 2:
                        endMenu(board)
                        return
                    gameMenu(board, not curPlayer, vsAI, aiColor, passes)
                print('ai played')
                gameMenu(board, not curPlayer, vsAI, aiColor)
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
                gameMenu(board, not curPlayer, vsAI, aiColor, passes)
            else:
                gameMenu(board, curPlayer, vsAI, aiColor)


def main():
    mainMenu()

main() 