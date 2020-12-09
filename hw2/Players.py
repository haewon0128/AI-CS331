'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import sys
from OthelloBoard import *
class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def successor(self, board, sym):
        successors = []
        for i in range(4):
            for j in range(4):
                if board.is_legal_move(i, j, sym):
                    tempboard = board.cloneOBoard()
                    tempboard.play_move(i, j, sym)
                    successors.append([tempboard,i, j])
                

        return successors


    def utility(self, board):
        
        return board.count_score(self.symbol) - board.count_score(self.oppSym)

    def maximize(self, board):
        sym = self.symbol
        succ = self.successor(board,sym)
        if len(succ) == 0:
            return None, self.utility(board)
        
        value = -(sys.maxsize)
        argmax = None
        
        for x in succ:
            state, uti = self.minimize(x[0])
            if uti>value:
                value = uti
                argmax = x


        return argmax, value

    
    def minimize(self, board):
        sym = self.oppSym
        succ = self.successor(board,sym)
        if len(succ) == 0:
                return None, self.utility(board)

        
        value = (sys.maxsize)
        argmax = None
   
        for x in succ:
            state, uti = self.maximize(x[0])
            if uti<value:
                value = uti
                argmax = x


        return argmax, value
    
    def minimax_decision(self, board):
    
        argmax, value = self.maximize(board)
        return (argmax[1], argmax[2])

    def get_move(self, board):
        print("calculating.. wait.... please..")
        return (self.minimax_decision(board))
        


        





