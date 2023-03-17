#include <stdio.h>
#include <iostream>
#include <cassert>

#include <stdlib.h>
#include <string.h>
using namespace std;

#define INF 0x7fffff
#define isOccupied(row, col, state) (state[row][col]=='X'||state[row][col]=='O')
#define isBlack(row, col) ((row+col)%2==0)

class AIPlayer{
public:
    AIPlayer():name("AI"), symbole('O'),isAI(true),score(0){

    }

    int add_symbole(char symbole1){
    
        symbole = symbole1;
        //cout<<"aiplayer"<<symbole<<endl;
        return 0;
    }
    char get_symbole(){
    	return symbole;
    }
    bool get_isAI(){
    	return isAI;
    }
    int add_score(int score1){
    	score=score+=score1;
    	return 0;
    }
    int add_isAI(bool isAI1){
		isAI=isAI1;
    	return 0;
    }
    int get_score(){
    	return score;
    }

	int* get_move(char state[6][6], char symbole){
		static int** moveList = new int*[36];
        static int** utility = new int*[6];
        int num = 0;
        int max_utility = -INF;

        for (int row=0;row<6;row++){
            int *col = new int[6];
            utility[row] = col;
            for (int column=0;column<6;column++){
                utility[row][column] = util(row, column, state);
                if (utility[row][column] > max_utility){
                    max_utility = utility[row][column];
                }
                //printf("u[%d][%d] = %d\n", row, column, utility[row][column]); 
            }
        }
        //printf("max utility: %d\n", max_utility);
        // assert(max_utility > -INF);
	    for (int row=0;row<6;row++){
            for (int column=0;column<6;column++){
                if (utility[row][column] == max_utility){
                    int *move = new int[2];
                    move[0] = row; move[1] = column;
                    moveList[num++] = move;
                }	
            }
        }
        // for (int i=0; i<num; i++) {
        //     printf("(%d, %d)\n", moveList[i][0], moveList[i][1]);
        // }
        return moveList[rand() % num];
	}

    int row_reward(int row, int col, char state[6][6]){
        if (isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&isOccupied(row, 5, state)){
            return 6;
        }else if (isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&(col==0||col==1||col==2)){
            return 3;
        }else if(!isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&!isOccupied(row, 4, state)&&(col==1||col==2||col==3)){
            return 3;
        }else if(!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&!isOccupied(row, 5, state)&&(col==2||col==3||col==4)){
            return 3;
        }else if(!isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&isOccupied(row, 5, state)&&(col==3||col==4||col==5)){
            return 3;
        }
        return 0;
    }

    int col_reward(int row, int col, char state[6][6]){
        if (isOccupied(0, col, state)&&isOccupied(1, col, state)&&isOccupied(2, col, state)&&isOccupied(3, col, state)&&isOccupied(4, col, state)&&isOccupied(5, col, state)){
            return 6;
        }else if (isOccupied(0, col, state)&&isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)&&(row==0||row==1||row==2)){
            return 3;
        }else if(!isOccupied(0, col, state)&&isOccupied(1, col, state)&&isOccupied(2, col, state)&&isOccupied(3, col, state)&&!isOccupied(4, col, state)&&(row==1||row==2||row==3)){
            return 3;
        }else if(!isOccupied(1, col, state)&&isOccupied(2, col, state)&&isOccupied(3, col, state)&&isOccupied(4, col, state)&&!isOccupied(5, col, state)&&(row==2||row==3||row==4)){
            return 3;
        }else if(!isOccupied(2, col, state)&&isOccupied(3, col, state)&&isOccupied(4, col, state)&&isOccupied(5, col, state)&&(row==3||row==4||row==5)){
            return 3;
        }
        return 0; 
    }

    int row_penalty(int row, char state[6][6], bool isPlayerX){
            // is my player x?
            // black
            int black = 0;
            int white = 0;
            for (int col=0; col < 6; col++) {
                if (isOccupied(row,col,state)) {
                    if (isBlack(row,col)) {
                        black++;
                    } else {
                        white++;
                    }
                }
            }
            if (isPlayerX) {
                if (black == 3 && white < black) {
                    return -6;
                }
            } else {
                if (white == 3 && black < white) {
                    return -6;
                }
            }
            if ((isPlayerX && row%2==1) || (!isPlayerX && row%2==0)) {                
                if (!isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&!isOccupied(row, 2, state)&&isOccupied(row, 3, state)){
                    return -3;
                }
                if(!isOccupied(row, 0, state)&&!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&!isOccupied(row, 4, state)){
                    return -3;
                }
                if(!isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&!isOccupied(row, 4, state)){
                    return -3;
                }                
                if(!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&!isOccupied(row, 5, state)){
                    return -3;
                }
                if(!isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&isOccupied(row, 5, state)){
                    return -3;
                }
                if(!isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&!isOccupied(row, 5, state)){
                    return -3;
                }
            }
            if ((isPlayerX && row%2==0) || (!isPlayerX && row%2==1)) {
                if (isOccupied(row, 0, state)&&!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)){
                    return -3;
                }
                if(!isOccupied(row, 0, state)&&!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&!isOccupied(row, 4, state)){
                    return -3;
                }
                if(!isOccupied(row, 0, state)&&isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&!isOccupied(row, 4, state)){
                    return -3;
                } 
                if(!isOccupied(row, 1, state)&&isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&!isOccupied(row, 5, state)){
                    return -3;
                }
                if(!isOccupied(row, 2, state)&&!isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&isOccupied(row, 5, state)){
                    return -3;                                
                }
                if(!isOccupied(row, 2, state)&&isOccupied(row, 3, state)&&isOccupied(row, 4, state)&&!isOccupied(row, 5, state)){
                    return -3;                                
                }
            }
            return 0;
    }

    int col_penalty(int col, char state[6][6], bool isPlayerX){
            int black = 0;
            int white = 0;
            for (int row=0; row < 6; row++) {
                if (isOccupied(row, col, state)) {
                    if (isBlack(row,col)) {
                        black++;
                    } else {
                        white++;
                    }
                } 
            }
            if (isPlayerX) {
                if (black == 3 && white < black) {
                    return -6;
                }
            } else {
                if (white == 3 && black < white) {
                    return -6;
                }
            }
            if ((isPlayerX && col%2==1) || (!isPlayerX && col%2==0)) {               
                if (!isOccupied(0, col, state)&&isOccupied(1, col, state)&&!isOccupied(2, col, state)&&isOccupied(3, col, state)){
                    return -3;
                }
                if(!isOccupied(0, col, state)&&!isOccupied(1, col, state)&&isOccupied(2, col, state)&&isOccupied(3, col, state)&&!isOccupied(4, col, state)){
                    return -3;
                }
                if(!isOccupied(0, col, state)&&isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)&&!isOccupied(4, col, state)){
                    return -3;
                }                
                if(!isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)&&isOccupied(4, col, state)&&!isOccupied(5, col, state)){
                    return -3;
                }
                if(!isOccupied(2, col, state)&&!isOccupied(3, col, state)&&isOccupied(4, col, state)&&isOccupied(5, col, state)){
                    return -3;
                }
                if(!isOccupied(2, col, state)&&isOccupied(3, col, state)&&isOccupied(4, col, state)&&!isOccupied(5, col, state)){
                    return -3;
                }
            }
            if ((isPlayerX && col%2==0) || (!isPlayerX && col%2==1)) {
                if (isOccupied(0, col, state)&&!isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)){
                    return -3;
                }
                if(!isOccupied(0, col, state)&&!isOccupied(1, col, state)&&isOccupied(2, col, state)&&isOccupied(3, col, state)&&!isOccupied(4, col, state)){
                    return -3;
                }
                if(!isOccupied(0, col, state)&&isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)&&!isOccupied(4, col, state)){
                    return -3;
                } 
                if(!isOccupied(1, col, state)&&isOccupied(2, col, state)&&!isOccupied(3, col, state)&&isOccupied(4, col, state)&&!isOccupied(5, col, state)){
                    return -3;
                }
                if(!isOccupied(2, col, state)&&!isOccupied(3, col, state)&&isOccupied(4, col, state)&&isOccupied(5, col, state)){
                    return -3;                                
                }
                if(!isOccupied(2, col, state)&&isOccupied(3, col, state)&&isOccupied(4, col, state)&&!isOccupied(5, col, state)){
                    return -3;                                
                }
            }
            return 0; 
    }

    int util(int row, int col, char state[6][6]){
        // points
        //printf("move: (%d %d)\n", row, col);
        int ret = 0;
        char symbole = this->get_symbole();
        bool isPlayerX = (symbole=='X');
        bool isPlayerO = (symbole=='O');
        if (isOccupied(row, col, state)) {
            return -INF;
        }
        if (isPlayerX && !isBlack(row,col)){
            return -INF;
        }
        if (isPlayerO && isBlack(row,col)){
            return -INF;
        }
        // move
        state[row][col] = symbole;
        // reward
        ret += row_reward(row, col, state); //printf("after row reward: %d\n", ret);
        ret += col_reward(row, col, state); //printf("after col reward: %d\n", ret);
        // penalty
        ret += row_penalty(row, state, isPlayerX); //printf("after row penalty: %d\n", ret);
        ret += col_penalty(col, state, isPlayerX); //printf("after col penalty: %d\n", ret);
        // backward
        state[row][col] = ' ';
        return ret;
    }

private:
	string name;
	char symbole;
    bool isAI;
    int score;
};



extern "C" {

    AIPlayer py;

    char get_symbole(){
        return py.get_symbole();
    }

    int add_symbole(char symbole1){

        return py.add_symbole(symbole1);
    }

    bool get_isAI(){
        return py.get_isAI();
    }
    int add_score(int score1){

        return py.add_score(score1);
    }
    int add_isAI(bool isAI1){

        return py.add_isAI(isAI1);
    }
    int get_score(){
        return py.get_score();
    }

    int* get_move(char state[6][6], char symbole){

        return py.get_move(state,symbole);

    }
}
