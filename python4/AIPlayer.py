import copy 
from math import inf as infinity
import random   
# from mcts import MCTS_ZHOU_JUNCHEN_56641511
import time
import numpy as np


class Algorithm_ZHOU_Junchen_56641511:
    def __init__(self,player,state):
        self.my_dict = dict()
        self.cellsforplayer=[]
        self.player=player
        self.state=state
        
    def getplayer(self):
        return self.player
    #检查该行有几个位置被占
    def checkRowPosOccupied(self,row):
        count=0
        for j in range(6):
            if self.state[row][j] is not None:
                count+=1
        return count
    #检查该行有几列位置被占
    def checkColPosOccupied(self,col):
        count=0
        for i in range(6):
            if self.state[i][col] is not None:
                count+=1
        return count
    
    def countRemainingRowCells(self,row):
        count_player1=0
        count_player2=0
        if row%2==1: #奇数行
            for col in range(6):
                if col%2==0 and self.state[row][col] is  None:
                    count_player2+=1
                if col%2==1 and self.state[row][col] is None:
                    count_player1+=1
        else:#偶数行
            for col in range(6):
                if col%2==0 and self.state[row][col] is None:
                    count_player1+=1
                if col%2==1 and self.state[row][col] is None:
                    count_player2+=1
        if ((count_player1>count_player2) and self.player == 0) or ((count_player2>count_player1) and self.player==1):#player1并且player1空的多,player2并且player2空的多
            return 0
        if ((count_player1<count_player2) and self.player==0) or ((count_player2<count_player1) and self.player==1):#player1并且player1空的少
            return 1
        if count_player1==count_player2:#两者相等
            return 2
    
    def countRemainingColCells(self,col):
        count_player1=0
        count_player2=0
        if col%2==1: #奇数列
            for row in range(6):
                if row%2==0 and self.state[row][col] is  None: #player2,white
                    count_player2+=1
                if row%2==1 and self.state[row][col] is None:#player1,black
                    count_player1+=1
        else:#偶数列
            for row in range(6):
                if row%2==0 and self.state[row][col] is None:#player1
                    count_player1+=1
                if row%2==1 and self.state[row][col] is None:#player2
                    count_player2+=1
        if ((count_player1>count_player2) and self.player == 0) or ((count_player2>count_player1) and self.player==1):#player1并且player1空的多,player2并且player2空的多
            return 0
        if ((count_player1<count_player2) and self.player==0) or ((count_player2<count_player1) and self.player==1):#player1并且player1空的少
            return 1
        if count_player1==count_player2:#两者相等
            return 2
        
    def availabelCells(self):
        if self.player==0:
            for x, row in enumerate(self.state):
                for y, cell in enumerate(row):
                    if (cell is None) and  ((x+y)%2==0):
                        self.cellsforplayer.append(tuple([x, y]))
        else:
            for x, row in enumerate(self.state):
                for y, cell in enumerate(row):
                    if (cell is None) and  ((x+y)%2==1):
                        self.cellsforplayer.append(tuple([x, y]))
        return self.cellsforplayer  
        

            
    def detail(self):
        
        if self.is_game_over():
            return
        else:
            availablecells=self.cellsforplayer
            for availablecell in availablecells:
                score=0
                occupos_row=self.checkRowPosOccupied(availablecell[0])
                occupos_col=self.checkColPosOccupied(availablecell[1])
                if occupos_row==0:
                    score+=0
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:                        
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==1:
                    score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=True)
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==2:
                    score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=True)
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score                    
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==3:
                    score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=True)
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==4:
                    score+=self.checkAndScore4(rl=availablecell[0],isrow=True)
                    if occupos_col==0:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==5:
                    score+=self.checkAndScore5()
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score
                if occupos_row==6:
                    score+=self.checkAndScore5()
                    if occupos_col==0:
                        score+=0
                        self.my_dict[availablecell]=score
                    if occupos_col==1:
                        score+=self.checkAndScore1(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==2:
                        score+=self.checkAndScore2(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==3:
                        score+=self.checkAndScore3(row=availablecell[0],col=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==4:
                        score+=self.checkAndScore4(rl=availablecell[1],isrow=False)
                        self.my_dict[availablecell]=score
                    if occupos_col==5:
                        score+=self.checkAndScore5()
                        self.my_dict[availablecell]=score
                    else:
                        score+=0
                        self.my_dict[availablecell]=score



    def is_game_over(self):
        availcells=self.availabelCells()
        if len(availcells)==0:
            return True
        else:
            return False
    def findPositionWhen1Occupied(self,num,isrow):
        if isrow:
            for x,row in enumerate(self.state):
                for y,cell in enumerate(row):           
                    if cell is not None:
                        return num,y
        else:
            for x,row in enumerate(self.state):
                for y,cell in enumerate(row):           
                    if cell is not None:
                        return x,num
    def checkAndScore1(self,row,col,isrow):
        # score=0
        # if isrow:
        #     _,col_occupied=self.findPositionWhen1Occupied(row,isrow=True)
        #     if abs(col-col_occupied)==1 or 2:
        #         score-=1
        # else:
        #     row_occupied,_=self.findPositionWhen1Occupied(col,isrow=False)
        #     #print(row_occupied)
        #     if abs(row_occupied-row)==1 or 2:
        #         score-=1
        #     #print(score)
        return 0
    def findtwoPositionsWhen2CEllsOccupied(self,row,col,isrow):
        res=[]
        if isrow:
            for x,row in enumerate(self.state):
                for y,cell in enumerate(row):
                    if cell is not None:
                        res.append(y)
        else:
            for x,row in enumerate(self.state):
                for y,cell in enumerate(row):
                    if cell is not None:
                        res.append(x)
        return res[0],res[1]
    def checkAndScore2(self,row,col,isrow):
        score=0

        if isrow:
            if ((col+1)<6 and (col+2)<6 and ((self.state[row][col+1] is not None) and (self.state[row][col+2] is not None))) or ((col-1)>=0 and (col+1)<6 and ((self.state[row][col-1] is not None) and (self.state[row][col+1] is not None))) or ((col-1)>=0 and (col-2)>=0 and ((self.state[row][col-1] is not None and (self.state[row][col-2]) is not None))):
                score+=3
            if self.countRemainingRowCells(row=row)==1:
                score-=4
            y1,y2=self.findtwoPositionsWhen2CEllsOccupied(row=row,col=col,isrow=True)
            # if (abs(y1-col)==1 or 2) or (abs(y2-col)==1 or 2):
            #     score-=1
        
        else:
            if((row+1)<6 and (row+2)<6 and ((self.state[row+1][col] is not None) and (self.state[row+2][col] is not None)))or ((row-1)>=0 and (row+1)<6 and ((self.state[row-1][col] is not None) and (self.state[row+1][col] is not None))) or ((row-1)>=0 and (row-2)>=0 and ((self.state[row-1][col] is not None and (self.state[row-2][col]) is not None))):
                score+=3
            if self.countRemainingColCells(col=col)==1:
                score-=4
            x1,x2=self.findtwoPositionsWhen2CEllsOccupied(row=row,col=col,isrow=False)
            # if (abs(x1-row)==1 or 2) or (abs(x2-row)==1 or 2):
            #     score-=1
        return score
    
    def existCoutinuous3(self,row,col,isrow):
        
        if isrow:
            if ((col+1)<6 and (col+2)<6 and ((self.state[row][col+1] is not None) and (self.state[row][col+2] is not None)) and (col-1)==-1 and self.state[row][col+3] is None)or((col+1)<6 and (col+2)<6 and ((self.state[row][col+1] is not None) and (self.state[row][col+2] is not None)) and (col-1)!=-1 and (col+3)<6 and self.state[row][col-1]is None and self.state[row][col+3] is None) or((col+1)<6 and (col+2)<6 and ((self.state[row][col+1] is not None) and (self.state[row][col+2] is not None)) and col+3==6 and self.state[row][col-1] is None) or((col-1)>=0 and (col+1)<6 and (self.state[row][col-1] is not None)  and (self.state[row][col+1] is not None) and col-2==-1 and self.state[row][col+2] is None) or((col-1)>=0 and (col+1)<6 and (self.state[row][col-1] is not None)  and (self.state[row][col+1] is not None) and col-2!=-1 and col+2<6 and self.state[row][col+2] is None and self.state[row][col-2] is None) or ((col-1)>=0 and (col+1)<6 and (self.state[row][col-1] is not None)  and (self.state[row][col+1] is not None) and col+2==6 and self.state[row][col-2] is None) or((col-1)>=0 and (col-2)>=0 and (self.state[row][col-1] is not None and (self.state[row][col-2]) is not None) and col-3==-1 and self.state[row][col+1] is None) or((col-1)>=0 and (col-2)>=0 and (self.state[row][col-1] is not None and (self.state[row][col-2]) is not None) and col-3!=-1 and col+1<6 and self.state[row][col+1] is None and self.state[row][col-3] is None) or((col-1)>=0 and (col-2)>=0 and (self.state[row][col-1] is not None and (self.state[row][col-2]) is not None) and col+1==6 and self.state[row][col-3] is None):
                return True
            else:
                return False
        else:
            if ((row+1)<6 and (row+2)<6 and (self.state[row+1][col] is not None) and (self.state[row+2][col] is not None) and (row-1)==-1 and self.state[row+3][col] is None)or((row+1)<6 and (row+2)<6 and (self.state[row+1][col] is not None) and (self.state[row+2][col] is not None) and (row-1)!=-1 and row+3<6 and self.state[row+3][col] is None and self.state[row-1][col] is None)or((row+1)<6 and (row+2)<6 and (self.state[row+1][col] is not None) and (self.state[row+2][col] is not None) and (row+3)==6 and self.state[row-1][col] is None)or((row-1)>=0 and (row+1)<6 and (self.state[row-1][col] is not None) and (self.state[row+1][col] is not None) and row-2==-1 and self.state[row+2][col] is None) or((row-1)>=0 and (row+1)<6 and (self.state[row-1][col] is not None) and (self.state[row+1][col] is not None) and row-2!=-1 and row+2<6 and self.state[row+2][col] is None and self.state[row-2][col]is None) or((row-1)>=0 and (row+1)<6 and (self.state[row-1][col] is not None) and (self.state[row+1][col] is not None) and row+2==6 and self.state[row-2][col] is None) or((row-1)>=0 and (row-2)>=0 and (self.state[row-1][col] is not None and (self.state[row-2][col]) is not None) and row-3==-1 and self.state[row+1][col] is None) or((row-1)>=0 and (row-2)>=0 and (self.state[row-1][col] is not None and (self.state[row-2][col]) is not None) and row-3!=-1 and row+1<6 and self.state[row+1][col] is None and self.state[row-3][col] is None) or((row-1)>=0 and (row-2)>=0 and (self.state[row-1][col] is not None and (self.state[row-2][col]) is not None) and row+1==6 and self.state[row-3][col] is None ):
                return True
            else:
                return False



    def checkAndScore3(self,row,col,isrow):#return score
        score=0
        if isrow:
            res_row=self.countRemainingRowCells(row=row)
            if res_row==0:
                if self.existCoutinuous3(row=row,col=col,isrow=isrow):
                    score+=3
                else:
                    score+=0
                #score+=0
            if res_row==1:
                score-=6
        else:
            res_col=self.countRemainingColCells(col=col)
            if res_col==0:
                if self.existCoutinuous3(row=row,col=col,isrow=isrow):
                    score+=3
                else:
                    score+=0
            if res_col==1:
                score-=6
        return score    

    def checkAndScore4(self,rl,isrow):#return score
        score=0
        if isrow:
            res_row=self.countRemainingRowCells(rl)
            if res_row==0:
                score+=6
            if res_row==2:
                score-=6
        else:
            res_col=self.countRemainingColCells(rl)
            if res_col==0:
                score+=6
            if res_col==2:
                score-=6
        return score

    def checkAndScore5(self):#return score
        score=6
        return score
        
    def bestaction(self):
        self.detail()
        v = max(self.my_dict.values())
        res=[]

        for key in self.my_dict.keys():
            if self.my_dict[key]==v:
                res.append(key)
        print(self.my_dict)
        if len(res)==1:
            # print(res)
            return list(res[0])
        else:
            # print(res)
            return list(random.choice(res))
        
    def possibleactions(self):
        self.detail()
        v = max(self.my_dict.values())
        res=[]
        for key in self.my_dict.keys():
            if self.my_dict[key]==v:
                res.append(key)
        return res       

        
class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."
    def get_move(self,state,player):
        
        if player=="X":
            sign=0
        else:
            sign=1
        games = Algorithm_ZHOU_Junchen_56641511(state=state,player=sign)
        possibleactions=games.possibleactions()
        random_move=RunMCTS_ZHOU_JUNCHEN_56641511(state=state,player=sign,myleagalactions=possibleactions)
        #random_move = games.bestaction()
        #games=self.available_cells(state=state)
        #random_move=random.choice(games)
        return random_move
    def available_cells(self,state):
        cells=[]
        for x,row in enumerate(state):
            for y,cell in enumerate(row):
                if(cell is None):
                    cells.append([x,y])
        return cells
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

class MonteCarloTreeSearchNode_ZHOU_JUNCHEN_56641511():
    def __init__(self, state,parent=None):
        self.state = state
        self.parent = parent
        self.children = dict()
        self._number_of_visits = 0
        self._Q=0        #wins
    
  
    def getq(self):
        return self._Q
    
    def getn(self):
        return self._number_of_visits
    
    def getchildren(self):
        return self.children
    
    def getparent(self):
        return self.parent
    
    def getstate(self):
        return self.state
    
    def UpdateChilderenAccordingtoActions(self,actions,player):
        for action in actions:
            if action not in self.children.keys():
                newstate=self.move(action=action,player=player,state=self.state)
                self.children[action]=MonteCarloTreeSearchNode_ZHOU_JUNCHEN_56641511(state=newstate,parent=self)

    def select(self):#return a node
        childs_arr=dict()
        for child in self.getchildren().values():
            childs_arr[child]=child.getUCBValue()
        return max(childs_arr, key=lambda x: childs_arr[x])


    def getUCBValue(self):
        myparent=self.getparent()
        if self.getn()==0:
            return infinity
        else:
            UCBValue=self.getq()+(2**0.5)*np.sqrt(np.log(myparent.getn())/self.getn())
        return UCBValue

    def update(self,leaf_value, node):
        node._number_of_visits+=1
        node._Q= 1.0*(leaf_value) / node._number_of_visits
        if not node.is_root():
            node.update(leaf_value=-leaf_value, node=node.parent)

    def is_leaf(self):
        if self.children=={}:
            return True
        return False
    def is_root(self):
        if self.parent==None:
            return True
        return False
    def move (self,action,state,player):
        newstate=copy.deepcopy(state)
        newstate[action[0]][action[1]]=player
        return newstate

    

class MCTS_ZHOU_JUNCHEN_56641511():
    def __init__(self,state,mylegalactions,myAIplayer):
        self.state=state
        self.mylegalactions=mylegalactions
        self.myAIplayer=myAIplayer
        self.root=MonteCarloTreeSearchNode_ZHOU_JUNCHEN_56641511(state=state,parent=None)
        #self.num_of_play_out=num_of_play_out

    def MCTS_Process(self):
        self.root.UpdateChilderenAccordingtoActions(actions=self.mylegalactions,player=self.myAIplayer)
        node=self.root.select()
        rollout_process=rollout_ZHOU_JUNCHEN_56641511(state=self.state,player=self.myAIplayer)
        rollout_process.runrollout()
        leaf_value=rollout_process.getwins()
        #回溯
        node.update(leaf_value=leaf_value,node=self.root)
        

    def getbestaction(self):
        for k, v in self.root.children.items():
            if self.root.select()==v:
                return k
        # return self.root.select()

class rollout_ZHOU_JUNCHEN_56641511():
    #player input is 1 or 0 
    #0 is meaning black and 1 is meaning white
    def __init__(self,state,player):
        self.state=state
        self.player=player
        self.myAIplayer_score=0
        self.OpponentPlayer_score=0
        self.myAIplayer_wins=0

    def runrollout(self):
        count = 0
        while not self.isend(self.state):
            self.state = self.playchess(player=self.player if count == 0 else 1 - self.player,state=self.state)
            count = 1 - count
        if self.myAIplayer_score>self.OpponentPlayer_score:
            self.myAIplayer_wins+=1
        if self.myAIplayer_score==self.OpponentPlayer_score:
            self.myAIplayer_wins+=0
        if self.myAIplayer_score<self.OpponentPlayer_score:
            self.myAIplayer_wins-=1

    def getwins(self):
        return self.myAIplayer_wins
            
    def playchess(self,player,state):

        if player==self.player:
            myPossibleActions=Algorithm_ZHOU_Junchen_56641511(player=self.player,state=state).possibleactions()
            mychoice=random.choice(myPossibleActions)
            state=self.move(mychoice,state,player=self.player)
            #print(state, mychoice)
            self.myAIplayer_score+=self.alignement(state=state,x=mychoice[0],y=mychoice[1])
        else:
            opponentAvailableCells=self.getOpponentAvailableCells(state=state,myAIplayer=self.player)
            opponentchoice=random.choice(opponentAvailableCells)
            state=self.move(opponentchoice,state=state,player=1-self.player)
            self.OpponentPlayer_score+=self.alignement(state=state,x=opponentchoice[0],y=opponentchoice[1])
        return state
    
    def getOpponentAvailableCells(self,state,myAIplayer):
        availablecells=[]
        if myAIplayer==0:       
            for x,row in enumerate(state):
                for y,cell in enumerate(row):
                    if (cell is None)and((x+y)%2==1):
                        availablecells.append(tuple([x,y]))
            return availablecells
        else:
            for x,row in enumerate(state):
                for y,cell in enumerate(row):
                    if (cell is None)and((x+y)%2==0):
                        availablecells.append(tuple([x,y]))
        return availablecells  

    def move (self,action,state,player):
        newstate=copy.deepcopy(state)
        newstate[action[0]][action[1]] = 'X' if player==0 else 'O'
        return newstate

    def isend(self,state):
        for x,row in enumerate(state):
            for y,cell in enumerate(row):
                if  cell is None:
                    return False
        return True

    def alignement(self, state,x,y):
        #print("xy:",x,y)
        score=0

        #1.check horizontal
        if((state[x][0] != None) and (state[x][1] != None) and  (state[x][2]!= None) and (state[x][3] != None) and (state[x][4] != None) and (state[x][5]  != None)):  
            score+=6
            #print("horizontal 6")
        else:
            if (state[x][0] != None) and (state[x][1] != None) and  (state[x][2]!= None) and (state[x][3] == None):
                if y==0 or y==1 or y==2:
                    score+=3
                    #print("1horizontal 3")
            elif (state[x][0] == None) and (state[x][1] != None) and  (state[x][2]!= None) and (state[x][3] != None) and (state[x][4] == None):
                if y==1 or y==2 or y==3:
                    score+=3
                    #print("2horizontal 3")
            elif  (state[x][1] == None) and (state[x][2] != None) and  (state[x][3]!= None) and (state[x][4] != None) and (state[x][5] == None):
                if y==2 or y==3 or y==4:
                    score+=3
                    #print("3horizontal 3")
            elif  (state[x][2] == None) and  (state[x][3]!= None) and (state[x][4] != None) and (state[x][5] != None):
                if y==3 or y==4 or y==5:
                    score+=3
                    #print("4horizontal 3")
                
        #2.check vertical
        if((state[0][y] != None) and (state[1][y] != None) and (state[2][y] != None) and (state[3][y] != None) and (state[4][y]!= None) and (state[5][y]!= None)):
            score+=6
            #print("vertical 6")
        else:
            if (state[0][y] != None) and (state[1][y] != None) and  (state[2][y]!= None) and (state[3][y] == None):
                if x==0 or x==1 or x==2:
                    score+=3
                    #print("1vertical 3")
            elif (state[0][y] == None) and (state[1][y] != None) and  (state[2][y]!= None) and (state[3][y] != None) and (state[4][y] == None):
                if x==1 or x==2 or x==3:
                    score+=3
                    #print("2vertical 3")
            elif (state[1][y] == None) and (state[2][y] != None) and  (state[3][y]!= None) and (state[4][y] != None) and (state[5][y] == None):
                if x==2 or x==3 or x==4:
                    score+=3
                    #print("3vertical 3")
            elif  (state[2][y] == None) and  (state[3][y]!= None) and (state[4][y] != None) and (state[5][y] != None):
                if x==3 or x==4 or x==5:
                    score+=3
                    #print("4vertical 3")


        return score



#state会辩护 喂数据喂的对吗
def RunMCTS_ZHOU_JUNCHEN_56641511(state,player,myleagalactions):
    time_start = time.time()
    time_end = time.time()
    
    while time_end-time_start<9.0:
        mcts=MCTS_ZHOU_JUNCHEN_56641511(state=state,myAIplayer=player,mylegalactions=myleagalactions)
        mcts.MCTS_Process()
        time_end=time.time()
    print("final: ", mcts.getbestaction())
    return mcts.getbestaction()
           


         