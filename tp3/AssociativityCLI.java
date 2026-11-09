import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Random;
import java.util.Locale;

public class AssociativityCLI {

    public static void main(String[] args) throws Exception {

        int tests = 1_000_000;
        long seed = 42;
        double min = -1e16;
        double max = 1e16;

        // Read command-line arguments
        for (String arg : args) {

            String[] parts = arg.replaceFirst("^--", "").split("=", 2);

            if (parts.length != 2) {
                throw new IllegalArgumentException(
                    "Invalid argument: " + arg
                );
            }

            switch (parts[0]) {
                case "tests":
                    tests = Integer.parseInt(parts[1]);
                    break;

                case "seed":
                    seed = Long.parseLong(parts[1]);
                    break;

                case "min":
                    min = Double.parseDouble(parts[1]);
                    break;

                case "max":
                    max = Double.parseDouble(parts[1]);
                    break;

                default:
                    throw new IllegalArgumentException(
                        "Unknown argument: " + parts[0]
                    );
            }
        }

        if (tests <= 0 || !Double.isFinite(min)
                || !Double.isFinite(max) || min >= max) {
            throw new IllegalArgumentException("Invalid parameters");
        }

        int equal = 0;
        Random random = new Random(seed);

        for (int i = 0; i < tests; i++) {

            double x = min + random.nextDouble() * (max - min);
            double y = min + random.nextDouble() * (max - min);
            double z = min + random.nextDouble() * (max - min);

            if ((x + y) + z == x + (y + z)) {
                equal++;
            }
        }

        double percentage = (double) equal / tests * 100;

        String outputDir = System.getenv().getOrDefault(
            "OUTPUT_DIR", "."
        );

        new File(outputDir).mkdirs();

        try (PrintWriter file = new PrintWriter(
                new FileWriter(
                    outputDir + "/answer_associativity_llm_java.txt"
                ))) {

            file.println("Tests: " + tests);
            file.println("Equal results: " + equal);
            file.printf(
                Locale.US,
                "Percentage: %.4f%%%n",
                percentage
            );
            file.println("Language: Java");
            file.println("Random seed: " + seed);
            file.println("Range: [" + min + ", " + max + ")");
            file.println("Comparison: exact floating-point equality");
        }

        System.out.printf(
            Locale.US,
            "Tests: %d | Equal: %d | Percentage: %.4f%%%n",
            tests, equal, percentage
        );
    }
}