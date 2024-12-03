import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class SolutionDay1 {

    private String input;

    SolutionDay1(String input){
        this.input = input;

    }

    public int solutionPart1(){
        ArrayList<Integer> leftColumn = new ArrayList<>();
        ArrayList<Integer> rightColumn = new ArrayList<>();

        String[] lines = input.split("\n");

        for(String line: lines){
            String[] lineArray = line.trim().split("\\s+");
            leftColumn.add(Integer.parseInt(lineArray[0]));
            rightColumn.add(Integer.parseInt(lineArray[1]));
        }

        Collections.sort(leftColumn, Collections.reverseOrder());
        Collections.sort(rightColumn, Collections.reverseOrder());

        int sum = 0;
        for(int i = 0; i < leftColumn.size(); i++){
            sum += Math.abs(leftColumn.get(i) - rightColumn.get(i));
        }

        return sum;
    }

    public int solutionPart2(){
        ArrayList<Integer> leftColumn = new ArrayList<>();
        ArrayList<Integer> rightColumn = new ArrayList<>();
        String[] lines = input.split("\n");

        for(String line: lines){
            String[] lineArray = line.trim().split("\\s+");
            leftColumn.add(Integer.parseInt(lineArray[0]));
            rightColumn.add(Integer.parseInt(lineArray[1]));
        }

        HashMap<Integer, Integer> map = new HashMap<>();

        for(int i = 0; i < leftColumn.size(); i++){
            for(int j = 0; j < rightColumn.size(); j++){
                if((int)rightColumn.get(j) == (int)leftColumn.get(i)){
                    int number = map.getOrDefault(rightColumn.get(j), 0);
                    map.put(rightColumn.get(j), number + 1);
                }
            }

        }

        int sum = 0;
        System.out.println(map);
        for(Integer key: map.keySet()){
            sum += key * map.get(key);
        }
        return sum;
    }


}
