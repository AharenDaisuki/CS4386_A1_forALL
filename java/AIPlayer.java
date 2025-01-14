package com;
import java.util.ArrayList;
public class AIPlayer {
	String name="AI2";
	String symbole;
	boolean isAI=true;
    int score=0;

	public boolean get_isAI(){
		return isAI;
	}
	public void add_symbole(String symbole1){
		symbole=symbole1;
	}
	public void add_isAI(boolean isAI1){
		isAI=isAI1;
	}
	public String get_symbole(){
		return symbole;
	}
	
	public void add_score(int score1){
		score=score+score1;
	
	}
	public int get_score(){
		return score;
	}

    @SuppressWarnings("unchecked")
    public int[] get_move(ArrayList state, String symbole){
		Boolean isPlayerX = (symbole.equals("X"));
		Boolean isPlayerO = (symbole.equals("O"));
    	ArrayList moveList= new ArrayList();
	    for (int row=0;row<6;row++){
            for (int column=0;column<6;column++){	
            	ArrayList this_row=(ArrayList)state.get(row);
            	if (this_row.get(column)==null){
            		int[] move = new int[2];
					move[0]=row;
					move[1]=column;
					if (isPlayerX && (row+column)%2==0){
						// System.out.println(move);
						moveList.add(move);	
					} else if (isPlayerO && (row+column)%2==1){
						// System.out.println(move);
						moveList.add(move);
					}
                }
            }
        }
		//System.out.println(state);
		//System.out.println(moveList);
        int rand = (int)(Math.random() * moveList.size());
        return (int[]) moveList.get(rand);
    }
}