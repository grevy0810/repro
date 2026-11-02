
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;

public class Distributivity {

    public static void main(String[] args) throws Exception {

        int n = 100000000;
        int count = 0;

        Random rand = new Random();

        String outputDir = System.getenv().getOrDefault("OUTPUT_DIR", ".");
        new File(outputDir).mkdirs();

        for (int i = 0; i < n; i++) {

            double x = rand.nextDouble();
            double y = rand.nextDouble();
            double z = rand.nextDouble();

            double a = x * (y + z);
            double b = x * y + x * z;

            if (a == b) {
                count++;
            }
        }

        double percentage = (double) count / n * 100;

        File outputFile = new File(
            outputDir, "answer_distributivity.txt"
        );

        try (PrintWriter file = new PrintWriter(
                new FileWriter(outputFile))) {

            file.println("Number of tests: " + n);
            file.println("Equal results: " + count);
            file.println("Percentage: " + percentage + "%");
            file.println("Property: Distributivity");
        }

        System.out.println("Distributivity: " + percentage + "%");
    }
}