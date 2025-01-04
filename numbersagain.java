import java.util.ArrayList;
final class node{
    node left;
    node right;
    int value;
    int operation;
    boolean leaf;
    String[] operations = {"", "+", "-", "*", "/"};
    node(node left, node right, int operation){
        this.left = left;
        this.right = right;
        this.operation = operation;
        leaf = false;
        switch (operation){
            case 1 -> value = left.getvalue() + right.getvalue();
            case 2 -> value = left.getvalue() - right.getvalue();
            case 3 -> value = left.getvalue() * right.getvalue();
            case 4 -> value = left.getvalue() / right.getvalue();
        
    }
    /*if(left.getvalue() == 100 && right.getvalue() == 15){
    System.out.println(left.value +  "left");
    System.out.println(right.value + "right");
    System.out.println(operations[operation] + "operations");
    System.out.println(value + "value");
    System.out.println();
}*/
    verify(value);

}
    node(int value){
        this.value = value;
        leaf = true;
        this.left = null;
        this.right = null;
    }
    void verify(int value){
        int currentDiff = Math.abs(value - solutionList.gettarget());
        //System.out.println(value + "value");
        //System.out.println(solutionList.getmin() + "getmin");
        if(currentDiff <= Math.abs(solutionList.getmin())){
            if(currentDiff < solutionList.getmin()){
                solutionList.clearsolutions();
                solutionList.setmin(currentDiff);

            }
            if(!solutionList.checksols(this)){
            solutionList.addsolution(this);}
        }
        
    }
   public int getvalue(){
        return value;
    }
    public int getOperation(){
        return operation;
    }

    public void printTree(node node){
        if (node.left == null || node.right == null){
            return;
        }
        if(!leaf){
            System.out.println(node.left.getvalue()+ " " + operations[node.operation]+ " " + node.right.getvalue() +  " = " + node.getvalue());
            printTree(node.left);
            printTree(node.right);
        }
    }

    public boolean compnodes(node node1, node node2){
        if (node1 == null && node2 == null) {
            return true; 
        }
        if (node1 == null || node2 == null) {
            return false; 
        }
        if(node1.getvalue() == node2.getvalue() && node2.getOperation() == node1.getOperation()){
            if(((node1.compnodes(node1.left, node2.left)== true && node1.compnodes(node1.right, node2.right)== true)||
            ((node1.compnodes(node1.right, node2.left)== true && node1.compnodes(node1.left, node2.right)== true)
            ))){return true;}
        }
        return false;
    }
}


class solutionList{
    static int target;
    static int min = 1000;
    static ArrayList<node> solutionList = new ArrayList<>();
     static void addsolution(node node){
        solutionList.add(node);
     }
     static void clearsolutions(){
        solutionList.clear();
     }
     static void settarget(int number){
        target = number;
     }
     static void setmin(int newmin){
        min = newmin;
     }
     static int getmin(){
        return min;
     }
     static int gettarget(){
        return target;
     }
     static void printsols(){
        for(int i = 0; i < solutionList.size(); i++){
            solutionList.get(i).printTree(solutionList.get(i));
            System.out.println("BREAK");
        }
     }
     static boolean checksols(node node){
        for(int i = 0; i < solutionList.size(); i++){
            if (node.compnodes(node, solutionList.get(i)) == true){return true;}
        }
        return false;
     }
 

     
}


public class numbersagain {
    public static void main(String args[]){
        long start = System.nanoTime();
        int[] numbers = {100,1,4,75,8,4};
        int target = 865;
        solutionList.settarget(target);
        node[] numtree = new node[numbers.length];
        numtree = initializeNodes(numbers);
        treeForm(numtree);
        solutionList.printsols();
        long end = System.nanoTime();
        System.out.println((end - start)/Math.pow(10,9));

    }


    public static void  numssolve(int num1, int num2, int num3, int num4, int num5, int num6, int target){
        int[] nums = new int[6];
        nums[0] = num1;
        nums[1] = num2;
        nums[2] = num3;
        nums[3] = num4;
        nums[4] = num5;
        nums[5] = num6;
        solutionList.settarget(target);
        node[] numtree = new node[nums.length];
        numtree = initializeNodes(nums);
        treeForm(numtree);
        solutionList.printsols();
    }

    static node[] initializeNodes(int[] nums){
        node[] numtree = new node[nums.length];
        for(int i = 0; i < nums.length; i++){
            numtree[i] = new node(nums[i]);
        }
        return numtree;
    }
    static void treeForm(node[] nums){
        if (nums.length == 1) {
            nums[0].verify(nums[0].getvalue());
            return;
        }
        for(int i = 0; i < nums.length-1; i++){
            for(int j = i+1; j < nums.length; j++){
                 for(int m = 0; m < nums.length; m ++){
                    //System.out.print(nums[m].getvalue() + " ");
                }
                //System.out.println("");

                for(int k = 1; k <= 4; k++){
                if ((k != 4 || 
                    (k == 4 && 
                    ((nums[j].getvalue() != 0 && nums[i].getvalue() % nums[j].getvalue() == 0 && nums[i].getvalue() != 0) || 
                    (nums[i].getvalue() != 0 && nums[j].getvalue() % nums[i].getvalue() == 0 && nums[j].getvalue() != 0)))) && 
                    (k != 3 || (nums[i].getvalue() != 1 && nums[j].getvalue() != 1)) && 
                    (k != 4 || (nums[i].getvalue() != 1 && nums[j].getvalue() != 1))) {

                
                    node node;
                        if ((k == 4 || k == 2) && nums[i].getvalue() < nums[j].getvalue()) {
                            node = new node(nums[j],nums[i],k);
                        }
                        else{
                            node = new node(nums[i],nums[j],k);
                        }
                        node[] newnums = new node[nums.length-1];
                        int counter = 0;
                        for(int l = 0; l < nums.length; l++){
                            //System.out.println(i + " i" );
                            //System.out.println(j + " j" );
                            //System.out.println(l + " l" );


                            if(l != i && l!= j){
                                //System.out.println(nums[l].getvalue());
                                //System.out.println("success" + counter);
                                newnums[counter++] = nums[l];
                            }
                    }
                    newnums[newnums.length - 1] = node;
                    for(int m = 0; m < newnums.length; m ++){
                        //System.out.print(newnums[m].getvalue() + " ");
                        }
                    //System.out.println("^newnums");
                    if(newnums.length > 0){
                        //System.out.println(newnums.length);
                        //System.out.println("");
                    treeForm(newnums);}
                }
                }

            }
        }
    }

}
