/**
 * lab1
 */

import java.util.Random;
public class Main {

    public static void main(String[] args) {
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
        double percentaje = (double) count /n *100;
        System.out.println(n);
        System.out.println(count);
        System.out.println( percentaje);
        
    }
}