import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;

public class AssociativityLLM {

    public static void main(String[] args) throws Exception {

        int tests = 1_000_000;
        int equal = 0;

        Random random = new Random(42);

        String outputDir = System.getenv().getOrDefault("OUTPUT_DIR", ".");
        new File(outputDir).mkdirs();

        for (int i = 0; i < tests; i++) {

            double x = -1e16 + random.nextDouble() * 2e16;
            double y = -1e16 + random.nextDouble() * 2e16;
            double z = -1e16 + random.nextDouble() * 2e16;

            if ((x + y) + z == x + (y + z)) {
                equal++;
            }
        }

        double percentage = (double) equal / tests * 100;

        try (PrintWriter file = new PrintWriter(
                new FileWriter(outputDir + "/answer_associativity_llm_java.txt"))) {

            file.println("Tests: " + tests);
            file.println("Equal results: " + equal);
            file.printf("Percentage: %.4f%%%n", percentage);
            file.println("Language: Java");
            file.println("Random seed: 42");
            file.println("Range: [-1e16, 1e16)");
            file.println("Comparison: exact floating-point equality");
        }

        System.out.printf("Associativity: %.4f%%%n", percentage);
    }
}