
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
from CONSTANTS import (DIRECTIONS, welcome, twoPlayerQuery, pieceRow, pieceColumn, wht, blk, gameEndMessage)
import GUI
import MiniMax

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def singlePlayer(ignore):
    return False

def twoPlayer(ignore):
    return True

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

#done
# returns player color code
def getPlayerPieceColor(player):
    if player:
        return wht
    else:
        return blk

#done
#flips all pieces sent
def flipPieces(board, curPlayer, toFlip):
    toColor = getPlayerPieceColor(curPlayer) #is actually the piece character code
    for piece in toFlip:
        board[piece] = toColor
    return board

def nextSpace(board, curPlayer, direction, toFlip, moveIndex):
    if 0 <= moveIndex < len(board): # if the space's index exists
        if board[moveIndex] == getPlayerPieceColor(not curPlayer): # if piece color is opposite curplayer, continue pathing
            toFlip.append(moveIndex) #add current first, so if next is empty, it gets cancelled too
            toFlip = nextSpace(board, curPlayer, direction, toFlip, moveIndex+DIRECTIONS[direction]) # "I frickin love recursion" -Orteil42
            return toFlip
        if board[moveIndex] == getPlayerPieceColor(curPlayer): # if piece color is same curplayer, finish path
            return toFlip
        if board[moveIndex] == ' ': # if space empty, cancel the whole path
            return []
    else:
        return [] # cancel path, out of bounds

def validateMove(board, curPlayer, moveIndex):
    print(moveIndex)
    toFlip = [moveIndex] #put in the initial move bc it needs to be placed
    for direction in DIRECTIONS: #iter all 8 directions keys, bc even if one causes flips, so may another
        toFlip = nextSpace(board, curPlayer, direction, toFlip, moveIndex+DIRECTIONS[direction])
    if not toFlip:
        return False, []
    return True, toFlip

def findValidMoves(board, curPlayer):
    validMoves = []
    for spot in board:
        isValid, toFlip = validateMove(board, curPlayer, spot)
        if isValid:
            validMoves.append(toFlip[0]) #if a valid move, the first index will be the move
    return validMoves


#########
# menus #
#########

def endMenu(board):
    #print score
    GUI.printScore(board)
    print(gameEndMessage)
    input('Press Any Key to Exit')
    sys.exit(0)

def mainMenu():
    board = [' ' for num in range(64)] #init all spaces to blank space
    curPlayer = False #False is black
    vsAI = False #default 2p game
    aiColor = True

    userSelect = input(welcome)
    vsAI = inputParse.get(userSelect, default)(mainMenu) # 1p or 2p
    if vsAI:
        aiPick = input(twoPlayerQuery)
        aiColor = aiChoice.get(aiPick, default)(mainMenu) # set ai color
        #implicitly thru gameMenu() logic, player color is opposite of ai color
    gameMenu(board, curPlayer, vsAI, aiColor)

def gameMenu(board, curPlayer, vsAI=False, aiColor=True, passes=0):
    clear()
    GUI.buildBoard(board)
    if passes > 0:
        print('Last player passed')
    row = input(pieceRow)
    column = input(pieceColumn)
    moveIndex = (int(row)-1*8)+int(column)-1
    valid, toFlip = validateMove(board, curPlayer, moveIndex)
    if valid:
        board = flipPieces(board, curPlayer, toFlip) # commit to move
        curPlayer = not curPlayer
        #never need to change curPlayer if AI
        if vsAI and (curPlayer and aiColor): #if 1player
            board, passed = MiniMax.AIMove(board, aiColor)
            print('ai playing')
            if passed:
                passes+=1
                if passes == 2:
                    endMenu(board)
                    return
                gameMenu(board, not curPlayer, vsAI, aiColor, passes)
                return
            print('ai played')
            gameMenu(board, not curPlayer, vsAI, aiColor)
        else: #if 2player
            gameMenu(board, not curPlayer, vsAI, aiColor)
    else: #invalid input either means a pass or an oof
        isPassing = input('Did you mean to pass?(Y/n)')
        passing = passingChoice.get(isPassing, default)(gameMenu, (board, curPlayer, vsAI, aiColor, passes))
        if passingChoice[passing.toLowerCase()]:
            passes += 1
            if passes == 2:
                endMenu(board)
                return
            gameMenu(board, not curPlayer, vsAI, aiColor, passes)
        else:
            gameMenu(board, not curPlayer, vsAI, aiColor)


def main():
    mainMenu()

main() 