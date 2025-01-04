import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class conundrum {   
    
    static String[] dict = new String[29133];

    public static ArrayList<String> filter(int size, ArrayList<String> arraylist){ //returns arraylist of words that are of a certain size
        ArrayList<String> filter = new ArrayList<>(); 
        for(int i = 0; i < arraylist.size();i++){
            if((arraylist.get(i)).length() == size){
                filter.add(arraylist.get(i));
            }
        }
        return filter;  

    }
    public static void preparray() throws FileNotFoundException{ //scans the list of 9-letter words
        File file = new File("9letterwords.txt");
        Scanner scanner = new Scanner(file);
        int counter = 0;
        while(scanner.hasNextLine()){
            String word = scanner.nextLine();
            dict[counter] = word;
            counter++;
        }
    }

    public static String subtract(String word, String longer) throws FileNotFoundException{ //removes the letters from a string for the other string

        StringBuilder newString = new StringBuilder(longer);
        for(int i = 0; i < word.length(); i++){
            char chamr = word.charAt(i);
            int index = newString.indexOf(String.valueOf(chamr));
            newString.deleteCharAt(index);
        }
        return newString.toString();
    } 


    public static void twoSolve(String solution, int choice) throws FileNotFoundException{
        ArrayList<String> displays = new ArrayList<>(); 
        displays = letters.solver(solution);
        ArrayList<String> displays2 = new ArrayList<>();
        displays = filter(choice + 5, displays); //finds a 5 or 6-letter word that fits inside the solution word
        int seed = (int) Math.random()*displays.size(); //chooses among the 5/6-letter words
        boolean found = false;
        String result = "";
        while(!found){
            for(int i = seed; i < displays.size(); i++){ //goes through the remaining words, regenerates a new word if no solution is found

                String current = displays.get(seed);

                displays2 = letters.solver( subtract(current, solution)); //fills the arraylist with words from the subtracted word to finda nother word
                displays2 = filter(9-(choice + 5),displays2); //filters out to find a word that makes the 9-letter word complete
                if(displays2.size()>0){ 
                    found = true;
                    String current2 = displays2.get((int)(Math.random()*displays2.size()));
                    result = current + current2; 
                    break;

                }
                seed++;
                
            }
            if(found == false){
                solution = dict[(int) (Math.random()*2933)];
                displays = letters.solver(solution);
                seed = (int) (Math.random()*displays.size());  
                displays = filter(choice + 5, displays);
            }   
       
        }
        System.out.println("The result is " + result + ". The solution is " + solution);

    }


    public static void threeSolve(String solution) throws FileNotFoundException{ //i doubt I'm gonna finish this, will likely leave it at 2
        ArrayList<String> displays = new ArrayList<>();
        displays = letters.solver(solution);
        ArrayList<String> displays2 = new ArrayList<>();
        displays = filter(3, displays);
        int i = (int) Math.random() * displays.size();
        boolean notfound = false;
        while(!notfound){ 

        }
    }

    public static void main(String[] args) throws FileNotFoundException{
        letters.hashprepper();
        preparray();
        String solution = dict[(int) (Math.random()*2933)];
        int choice = 0;
        twoSolve(solution, choice);

    }
}
