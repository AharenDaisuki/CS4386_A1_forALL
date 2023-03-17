import copy
import datetime
import time
from math import inf as infinity
import random
import numpy as np

TIME_LIMIT = 10
TOLERANCE = 0.7

##########################################
# CS4386 Semester B, 2022-2023
# Assignment 1
# Name: LI Xiaoyang
# Student ID: 56638660
##########################################

class Utils:
    @staticmethod
    def is_game_over(state):
        '''return if game is over'''
        for row in state:
            for cell in row:
                if cell is None:
                    return False
        return True
    
    @staticmethod
    def transpose(state):
        ret = [[],[],[],[],[],[]]
        for row in range(0, 6):
            for col in range(0, 6):
                ret[col].append(state[row][col])
        return ret
    
    @staticmethod
    def is_black_cell(cell):
        '''return if cell is black'''
        return (cell[0] + cell[1]) % 2 == 0
    
    # @staticmethod
    # def is_black_cell(x,y):
    #     return (x+y)%2 == 0

    @staticmethod
    def make_a_move(state, move, player):
        '''make a move and update state'''
        ret = [row.copy() for row in state]
        x, y = move[0], move[1]
        ret[x][y] = player
        return ret
    
    @staticmethod
    def heuristic(x, y, state, player):
        '''return all preferred moves'''
        def isOccupied(row, col, state):
            return state[row][col] != None
        def row_penalty(row, state, isPlayerX):
            black, white = 0, 0
            for col in range(0, 6):
                if isOccupied(row,col,state): 
                    if Utils.is_black_cell([row,col]):
                        black += 1
                    else:
                        white += 1
            if isPlayerX:
                if black == 3 and white<black: 
                    return -6
            else:
                if white == 3 and black < white:
                    return -6
            if ((isPlayerX and row%2==1) or (not isPlayerX and row%2==0)):             
                if(not isOccupied(row, 0, state) and isOccupied(row, 1, state) and not isOccupied(row, 2, state) and isOccupied(row, 3, state)):
                    return -3
                if(not isOccupied(row, 0, state) and not isOccupied(row, 1, state) and isOccupied(row, 2, state) and isOccupied(row, 3, state) and not isOccupied(row, 4, state)):
                    return -3
                if(not isOccupied(row, 0, state) and isOccupied(row, 1, state) and isOccupied(row, 2, state) and not isOccupied(row, 3, state) and not isOccupied(row, 4, state)):
                    return -3    
                if(not isOccupied(row, 1, state) and isOccupied(row, 2, state) and not isOccupied(row, 3, state) and isOccupied(row, 4, state) and not isOccupied(row, 5, state)):
                    return -3
                if(not isOccupied(row, 2, state)and not isOccupied(row, 3, state) and isOccupied(row, 4, state) and isOccupied(row, 5, state)):
                    return -3
                if(not isOccupied(row, 2, state) and isOccupied(row, 3, state) and isOccupied(row, 4, state) and not isOccupied(row, 5, state)):
                    return -3
            if ((isPlayerX and row%2==0) or (not isPlayerX and row%2==1)):
                if (isOccupied(row, 0, state) and not isOccupied(row, 1, state) and isOccupied(row, 2, state) and not isOccupied(row, 3, state)):
                    return -3
                if(not isOccupied(row, 0, state) and not isOccupied(row, 1, state) and isOccupied(row, 2, state) and isOccupied(row, 3, state) and not isOccupied(row, 4, state)):
                    return -3
                if(not isOccupied(row, 0, state) and isOccupied(row, 1, state) and isOccupied(row, 2, state) and not isOccupied(row, 3, state) and not isOccupied(row, 4, state)):
                    return -3
                if(not isOccupied(row, 1, state) and isOccupied(row, 2, state) and not isOccupied(row, 3, state) and isOccupied(row, 4, state) and not isOccupied(row, 5, state)):
                    return -3
                if(not isOccupied(row, 2, state) and not isOccupied(row, 3, state) and isOccupied(row, 4, state) and isOccupied(row, 5, state)):
                    return -3                                
                if(not isOccupied(row, 2, state) and isOccupied(row, 3, state) and isOccupied(row, 4, state) and not isOccupied(row, 5, state)):
                    return -3                                    
            return 0
        def col_penalty(col, state, isPlayerX):
            trans_state = Utils.transpose(state)
            return row_penalty(col, trans_state, isPlayerX)
        h = 0
        symbole = player
        isPlayerX = (symbole=='X')
        if state[x][y] != None:
            return -np.inf
        if isPlayerX and not Utils.is_black_cell([x,y]):
            return -np.inf
        if not isPlayerX and Utils.is_black_cell([x,y]):
            return -np.inf
        result = Utils.make_a_move(state, [x,y], player)
        # print(result)
        h += Utils.reward(result, [x, y])
        # print("after reward: " + str(h))
        h += row_penalty(x, result, isPlayerX)
        # print("after row penalty: " + str(h))
        h += col_penalty(y, result, isPlayerX)
        # print("after column penalty: " + str(h))
        return h
    
    @staticmethod
    def heuristic_moves(state, player):
        max_util = -np.inf
        utility = []
        cells = []
        for row in range(0, 6):
            utility.append([])
            for col in range(0, 6):
                utility[row].append(Utils.heuristic(row,col,state,player))
                if utility[row][col] > max_util:
                    max_util = utility[row][col]
        # print("max utility: " + str(max_util))
        for row in range(0, 6):
            for col in range(0, 6):
                if (utility[row][col] == max_util):
                    cells.append([row, col])
        assert(len(cells) > 0)
        # print(cells)
        return cells


       
    @staticmethod
    def get_all_moves(state, player):
        '''return all possible moves'''
        cells = []
        isPlayerX = (player=='X') # is player 1?
        isPlayerO = (player=='O') # is player 2?
        if isPlayerX:
            for x, row in enumerate(state):
                for y, cell in enumerate(row):
                    if cell is None and Utils.is_black_cell([x, y]):
                        cells.append([x, y])
        elif isPlayerO:
            for x, row in enumerate(state):
                for y, cell in enumerate(row):
                    if cell is None and not Utils.is_black_cell([x, y]):
                        cells.append([x, y]) 
        return cells
    
    @staticmethod
    def all_moves(state, player, heuristic):
        return Utils.heuristic_moves(state, player) if heuristic else Utils.get_all_moves(state, player)


    @staticmethod
    def reward(grid, move):
        #print("xy:",x,y)
        x, y = move[0], move[1]
        score=0

        #1.check horizontal
        if((grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5]  != None)):  
            score+=6
            #print("horizontal 6")
        else:
            if (grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] == None):
                if y==0 or y==1 or y==2:
                    score+=3
                    #print("1horizontal 3")
            elif (grid[x][0] == None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] == None):
                if y==1 or y==2 or y==3:
                    score+=3
                    #print("2horizontal 3")
            elif  (grid[x][1] == None) and (grid[x][2] != None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] == None):
                if y==2 or y==3 or y==4:
                    score+=3
                    #print("3horizontal 3")
            elif  (grid[x][2] == None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] != None):
                if y==3 or y==4 or y==5:
                    score+=3
                    #print("4horizontal 3")
                
        #2.check vertical
        if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y]!= None) and (grid[5][y]!= None)):
            score+=6
            #print("vertical 6")
        else:
            if (grid[0][y] != None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] == None):
                if x==0 or x==1 or x==2:
                    score+=3
                    #print("1vertical 3")
            elif (grid[0][y] == None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] != None) and (grid[4][y] == None):
                if x==1 or x==2 or x==3:
                    score+=3
                    #print("2vertical 3")
            elif (grid[1][y] == None) and (grid[2][y] != None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] == None):
                if x==2 or x==3 or x==4:
                    score+=3
                    #print("3vertical 3")
            elif  (grid[2][y] == None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] != None):
                if x==3 or x==4 or x==5:
                    score+=3
                    #print("4vertical 3")
        return score
    
    @staticmethod
    def playerBinToSymbol(binary):
        return 'X' if binary==1 else 'O'
    
    @staticmethod
    def playerSymbolToBin(symbol):
        return 1 if symbol=='X' else 0

    
class MonteCarloTreeNode:
    def __init__(self, player, state, action=None, parent=None, w = 0, n = 0):
        '''
        player: player binary code (1=>'X' 0=>'O')
        state: current state
        action: last action, None for root
        parent: parent node, None for root
        w: utility
        n: #games played
        '''
        self.children = []
        self.player = player
        self.state = state
        self.action = action 
        self.parent = parent
        self.w = w
        self.n = n

    def __str__(self):
        return "move: {}, utility: ({}/{}) = {}".format(self.action, self.w, self.n, self.w/self.n)    
    
class Timer:
    def __init__(self, time_limit, tol):
        self.tic = time.time()
        self.time_limit = time_limit
        self.tol = tol

    def tac(self):
        return time.time() - self.tic

    def check(self):
        return self.tac() > self.time_limit - self.tol
    
class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score = 0
        self.move_n = 0
        self.heuristic = True

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name

    def get_isAI(self):
        return self.isAI

    def get_symbole(self):
        return self.symbole

    def get_score(self):
        return self.score

    def add_score(self,score):
        self.score+=score

    # deprecated
    # def available_cells(self,state,player):
    #     cells = []
    #     for x, row in enumerate(state):
    #         for y, cell in enumerate(row):
    #             if (cell is None):
    #                 cells.append([x, y])
    #     return cells
    
    def mcts(self, player, state, timer):
        def ucb(node, c = np.sqrt(0.5)):
            '''return ucb of node'''
            # TODO: modify c
            return np.inf if node.n == 0 else node.w/node.n + c * np.sqrt(np.log(node.parent.n) / node.n)

        def select(node):
            '''select a leaf node'''
            if node.children:
                return select(max(node.children, key=lambda x : ucb(x)))
            return node
        
        def expand(node):
            '''expand the leaf node by adding all possible moves'''
            parent_state = node.state
            parent_player = node.player
            #child_player = parent_player ^ 1
            # assert(parent_player==1 and child_player==0 or parent_player==0 and child_player==1)
            if not node.children and not Utils.is_game_over(parent_state):
                move_list = Utils.all_moves(parent_state, Utils.playerBinToSymbol(parent_player), self.heuristic)
                for move in move_list:
                    child_state = Utils.make_a_move(parent_state, move, Utils.playerBinToSymbol(parent_player))
                    node.children.append(
                        MonteCarloTreeNode(
                            player=parent_player^1, 
                            state=child_state,
                            action=move,
                            parent=node,
                            w = 0,
                            n = 0
                        )
                    )
            return select(node)
        
        def simulate(state, player):
            '''return simulate result in terms of player'''
            tmp_state, tmp_player = state, player
            child_score, enemy_score = 0, 0
            while not Utils.is_game_over(tmp_state):
                player_symbol = Utils.playerBinToSymbol(tmp_player)
                games = Utils.get_all_moves(tmp_state, player_symbol)
                move = random.choice(games) # TODO: add heuristic
                tmp_state = Utils.make_a_move(tmp_state, move, player_symbol)
                if tmp_player==player:
                    child_score += Utils.reward(tmp_state, move)
                elif tmp_player==player^1:
                    enemy_score += Utils.reward(tmp_state, move)
                tmp_player ^= 1 # interchange player
            if child_score > enemy_score:
                return 1
            elif child_score < enemy_score:
                return -1
            return 0

        
        def backpropagate(node, utility):
            '''update path'''
            # TODO: definition?
            if utility < 0:
                node.w -= utility
            node.n += 1
            if node.parent:
                backpropagate(node.parent, -utility)

        # initial game state
        root = MonteCarloTreeNode(player=Utils.playerSymbolToBin(player), state=state, w=0, n=0)
        iterative_n = 0
        while True:
            leaf = select(root)
            child = expand(leaf)
            result = simulate(child.state, child.player)
            backpropagate(child, result)
            iterative_n += 1
            if timer.check():
                break

        # print(root)
        # for child in root.children:
        #     print('**************************')
        #     print(child)
        #     print('**************************')        

        # print('iteration:' + str(iterative_n))
        # assert(len(root.children) > 0)
        optimal_solution = max(root.children, key=lambda x : x.w/x.n)
        # print(optimal_solution)
        return optimal_solution.action
            
    def get_move(self,state,player):
        '''return a move'''
        # print('mcts with heuristic')
        timer = Timer(TIME_LIMIT, TOLERANCE)
        # first move
        if self.move_n == 0:
            self.move_n += 1
            return random.choice(Utils.all_moves(state, player, self.heuristic))
                      
        move = self.mcts(player, state, timer)
        # move_list = Utils.all_moves(state, player, self.move_n)
        # move = random.choice(move_list)
        self.move_n += 1
        return move       
