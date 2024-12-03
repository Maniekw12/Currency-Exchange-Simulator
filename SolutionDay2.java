import java.util.ArrayList;

public class SolutionDay2 {

    private String input;

    SolutionDay2(String input){
        this.input = input;
    }


    public int solutionPart1(){
        String[] lines = input.split("\n");

        int safeLines = 0;
        for(String line : lines){
            ArrayList<Integer> numbers = new ArrayList<>();

            for(String number : line.split(" ")){
                numbers.add(Integer.parseInt(number));
            }

            if(isSafe(numbers)){
                safeLines++;
            }
            System.out.println(safeLines + " " + numbers);


        }
        return safeLines;

    }

    private boolean isSafe(ArrayList<Integer> numbers) {
        int firstDiff = numbers.get(1) - numbers.get(0);
        boolean increasing = firstDiff > 0;

        if (Math.abs(firstDiff) < 1 || Math.abs(firstDiff) > 3) {
            return false;
        }

        for (int i = 1; i < numbers.size(); i++) {
            int diff = numbers.get(i) - numbers.get(i - 1);

            if (Math.abs(diff) < 1 || Math.abs(diff) > 3) {
                return false;
            }

            boolean currentIncreasing = diff > 0;
            if (currentIncreasing != increasing) {
                return false;
            }
        }

        return true;
    }


    public int solutionPart2(){
        String[] lines = input.split("\n");
        int safeLines = 0;
        for(String line : lines){
            ArrayList<Integer> numbers = new ArrayList<>();

            for(String number : line.split(" ")){
                numbers.add(Integer.parseInt(number));
            }
            if(isSafe(numbers)){
                safeLines++;
                continue;
            }

            for(int i = 0; i < numbers.size(); i++){
                int removed = numbers.remove(i);
                if(isSafe(numbers)){
                    safeLines++;
                    numbers.add(i,removed);
                    break;
                }
                numbers.add(i,removed);
            }

            System.out.println(safeLines + " " + numbers);
        }
        return safeLines;


    }





}
