import java.io.FileNotFoundException;
public class solveletters {
    public static void main(String[] args) throws FileNotFoundException{
        letters.hashprepper();
        String[] solutions = (letters.solver(args[0])).toArray(new String[0]);
        String solution = "";
        for(int i = 0; i < solutions.length; i ++){
            solution = solution + solutions[i] + ",";
        }
        System.out.println(solution);
    }
    
}
