/**
 * lab1
 */

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;
public class Associativity {

    public static void main(String[] args) throws IOException {
        int n = 100000000;
        int count = 0;
        Random rand = new Random();
        for (int i = 0; i < n; i++) {
            double x = rand.nextDouble();
            double y = rand.nextDouble();
            double z = rand.nextDouble();
            double a = x+(y+z);
            double b = (x+y)+z;

            if (a == b ){
                count++;
            }
        }
        double percentage = (double) count /n *100;
        try (PrintWriter file = new PrintWriter(new FileWriter("answer_associativity.txt"))) {
            file.println("Number of tests: " + n);
            file.println("Equal results: " + count);
            file.println("Percentage: " + percentage + "%");
        }
    }
        
}