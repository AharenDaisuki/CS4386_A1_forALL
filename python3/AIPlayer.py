import copy
import datetime
import time
from math import inf as infinity
import random
import numpy as np
from multiprocessing import Pool

PARALLEL_SIMULATION_N = 4
MAX_ITERATION_TIME = 10

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
    def is_black_cell(cell):
        '''return if cell is black'''
        return (cell[0] + cell[1]) % 2 == 0

    @staticmethod
    def make_a_move(state, move, player):
        '''make a move and update state'''
        ret = [row.copy() for row in state]
        x, y = move[0], move[1]
        ret[x][y] = player
        return ret
    
    @staticmethod
    def all_moves(state, player):
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
    def reward(state, move):
        '''evaluate last move immediately after move'''
        def check_row(state, row):
            if state[row][0]!=None and state[row][1]!=None and state[row][2]!=None and state[row][3]!=None and state[row][4]!=None and state[row][5]!=None:
                return 6
            if state[row][0]!=None and state[row][1]!=None and state[row][2]!=None and state[row][3]==None:
                return 3
            if state[row][0]==None and state[row][1]!=None and state[row][2]!=None and state[row][3]!=None and state[row][4]==None:
                return 3
            if state[row][1]==None and state[row][2]!=None and state[row][3]!=None and state[row][4]!=None and state[row][5]==None:
                return 3 
            if state[row][2]==None and state[row][3]!=None and state[row][4]!=None and state[row][5]!=None:
                return 3  
            return 0
        def check_col(state, col):
            if state[0][col]!=None and state[1][col]!=None and state[2][col]!=None and state[3][col]!=None and state[4][col]!=None and state[5][col]!=None:
                return 6
            if state[0][col]!=None and state[1][col]!=None and state[2][col]!=None and state[3][col]==None:
                return 3
            if state[0][col]==None and state[1][col]!=None and state[2][col]!=None and state[3][col]!=None and state[4][col]==None:
                return 3
            if state[1][col]==None and state[2][col]!=None and state[3][col]!=None and state[4][col]!=None and state[5][col]==None:
                return 3 
            if state[2][col]==None and state[3][col]!=None and state[4][col]!=None and state[5][col]!=None:
                return 3  
            return 0
        utility = 0
        row, col = move[0], move[1]
        utility += check_row(state, row)
        utility += check_col(state, col)
        return utility
    
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
        self.move_n = 0 # TODO: record #move
        self.root = None # TODO: maintain a root node
        self.enemy_score = 0 # TODO: maintain enemy score

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

    def _update_root(self, node):
        self.root = node     

    def _add_enemy_score(self, score):
        self.enemy_score += score     

    def _get_enemy_score(self):
        return self.enemy_score    

    def _get_move_n(self):
        return self.move_n

    def _confirm_move(self, move):
        for child in self.root.children:
            if move == child.action:
                # assert(child.player ^ 1 == self.root.player)
                self._update_root(child)
        self.move_n += 1  
    
    # deprecated
    # def available_cells(self,state,player):
    #     cells = []
    #     for x, row in enumerate(state):
    #         for y, cell in enumerate(row):
    #             if (cell is None):
    #                 cells.append([x, y])
    #     return cells
    
    def mcts(self, timer):
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
            # def expand_child(parent_state, parent_player, move, node):
            #     child_state = Utils.make_a_move(parent_state, move, Utils.playerBinToSymbol(parent_player))
            #     node.children.append(
            #             MonteCarloTreeNode(
            #                 player=parent_player^1, 
            #                 state=child_state,
            #                 action=move,
            #                 parent=node,
            #                 w = 0,
            #                 n = 0
            #             )
            #         )
            #     print(len(node.child))
            #     return
                
            parent_state = node.state
            parent_player = node.player
            #child_player = parent_player ^ 1
            # assert(parent_player==1 and child_player==0 or parent_player==0 and child_player==1)
            if not node.children and not Utils.is_game_over(parent_state):
                # all_moves = Utils.all_moves(parent_state, Utils.playerBinToSymbol(parent_player)) 
                # move_n = len(all_moves)
                # pool = Pool(move_n)
                # for move in all_moves:
                #     pool.apply_async(expand_child, args=(parent_state, parent_player, move, node))
                # pool.close()
                # pool.join()

                for move in Utils.all_moves(parent_state, Utils.playerBinToSymbol(parent_player)):
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
            my_score = self.get_score()
            enemy_score = self._get_enemy_score()
            root_player = self.root.player
            tmp_state, tmp_player = state, player
            while not Utils.is_game_over(tmp_state):
                player_symbol = Utils.playerBinToSymbol(tmp_player)
                games = Utils.all_moves(tmp_state, player_symbol)
                        # assert(len(games) > 0)
                move = random.choice(games)
                tmp_state = Utils.make_a_move(tmp_state, move, player_symbol)
                if tmp_player==root_player:
                    my_score += Utils.reward(tmp_state, move)
                elif tmp_player==root_player^1:
                    enemy_score += Utils.reward(tmp_state, move)
                tmp_player ^= 1 # interchange player
            if my_score > enemy_score:
                return 1
            elif my_score < enemy_score:
                return -1
            return 0
                    
        # def multi_simulate(state, player):
        #     '''simulate 4 games in a row'''
        #     # def simulate(state, player):
        #     #     '''return simulate result in terms of player'''
        #     #     my_score = self.get_score()
        #     #     enemy_score = self._get_enemy_score()
        #     #     tmp_state, tmp_player = state, player
        #     #     while not Utils.is_game_over(tmp_state):
        #     #         player_symbol = Utils.playerBinToSymbol(tmp_player)
        #     #         games = Utils.all_moves(tmp_state, player_symbol)
        #     #         # assert(len(games) > 0)
        #     #         move = random.choice(games)
        #     #         tmp_state = Utils.make_a_move(tmp_state, move, player_symbol)
        #     #         if tmp_player==self.root.player:
        #     #             my_score += Utils.reward(tmp_state, move)
        #     #         elif tmp_player==self.root.player^1:
        #     #             enemy_score += Utils.reward(tmp_state, move)
        #     #         tmp_player ^= 1 # interchange player
        #     #     if my_score > enemy_score:
        #     #         return 1
        #     #     elif my_score < enemy_score:
        #     #         return -1
        #     #     return 0
            
        #     my_score = self.get_score()
        #     enemy_score = self._get_enemy_score()
        #     root_player = self.root.player
        #     pool = Pool(PARALLEL_SIMULATION_N)
        #     simulation_ret = [pool.apply_async(simulate, args=(state, player, my_score, enemy_score, root_player)) for i in range(0, PARALLEL_SIMULATION_N)]
        #     pool.close()
        #     pool.join()
        #     # print([s.get() for s in simulation_ret])
        #     return [s.get() for s in simulation_ret]

        
        def backpropagate(node, utility):
            node_player = node.player
            root_player = self.root.player
            if node_player==root_player^1:
                if utility > 0:
                    node.w += utility
            elif node_player==root_player:
                if utility < 0:
                    node.w += -utility
            node.n += 1
            if node.parent:
                backpropagate(node.parent, utility)

        # initial game state
        root = self.root
        iterative_n = 0
        while True:
            leaf = select(root)
            child = expand(leaf)
            result = simulate(child.state, child.player)
            backpropagate(child, result)
            iterative_n += 1
            if timer.check():
                break
        
        total_n = 0
        # for child in root.children:
        #     total_n += child.n
        #     print('**************************')
        #     print('move: ' + str(child.action))
        #     print(child)
        #     print('**************************')
        # print('root #games: ' + str(root.n))
        # print('child #games: ' + str(total_n))        

        # print('iteration:' + str(iterative_n))
        assert(len(root.children) > 0)
        optimal_solution = max(root.children, key=lambda x : x.w/x.n)

        # print(optimal_solution)
        return optimal_solution.action
            
    def get_move(self,state,player):
        '''return a move'''
        timer = Timer(10, 1.2)
        player_bin = Utils.playerSymbolToBin(player)
        # assert(player_bin==1 or player_bin==0)  
        flag, last_move = False, None
        if self._get_move_n()==0:
            self._update_root(MonteCarloTreeNode(player=player_bin, state=state, w=0, n=0))
            if player_bin==0:
                for x, row in enumerate(state):
                    for y, cell in enumerate(row):
                        if Utils.is_black_cell([x, y]) and state[x][y]!=None:
                            flag, last_move = True, [x, y]
        else:
            # print(self.root.state)
            # print(state)
            for row in range(0, 6):
                for column in range(0, 6):
                    if self.root.state[row][column]==None and state[row][column]==Utils.playerBinToSymbol(player_bin^1):
                        flag, last_move = True, [row, column]
            # flag, last_move = Utils.enemyMove(self.root.state, state, player_bin)

        if flag:
            self._add_enemy_score(Utils.reward(state, last_move))
            # print('enemy: ' + str(last_move) + '=>' + str(self.enemy_score))
            # my root => enemy
            if self._get_move_n() > 0:
                for child in self.root.children:
                    if child.action == last_move:
                        self._update_root(child)    
        # time offset in seconds                

        # assert(self.root != None)
        # assert(self.root.player == player_bin)
        move = self.mcts(timer)
        self._confirm_move(move)
        return move       
