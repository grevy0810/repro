import java.util.Random;

public class AssociativityRuntime {

    public static int checkProperty(int tests) {
        int equal = 0;
        Random random = new Random(42);

        for (int i = 0; i < tests; i++) {
            double x = -1e16 + random.nextDouble() * 2e16;
            double y = -1e16 + random.nextDouble() * 2e16;
            double z = -1e16 + random.nextDouble() * 2e16;

            if ((x + y) + z == x + (y + z)) {
                equal++;
            }
        }

        return equal;
    }

    public static void main(String[] args) {

        int[] repetitions = {
            100, 1000, 10000, 100000, 1000000
        };

        for (int tests : repetitions) {
            int equal = checkProperty(tests);
            double percentage = (double) equal / tests * 100;

            System.out.printf(
                "Tests: %d | Equal: %d | Percentage: %.4f%%%n",
                tests, equal, percentage
            );
        }
    }
}