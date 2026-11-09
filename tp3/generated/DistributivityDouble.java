import java.util.Random;

public class DistributivityDouble {

    public static void main(String[] args) {

        int tests = 1000000;
        int equal = 0;

        Random random = new Random(42);

        for (int i = 0; i < tests; i++) {

            double min = -1e16;
            double max = 1e16;

            double x = (double)
                (min + random.nextDouble() * (max - min));

            double y = (double)
                (min + random.nextDouble() * (max - min));

            double z = (double)
                (min + random.nextDouble() * (max - min));

            if (x * (y + z) == x * y + x * z) {
                equal++;
            }
        }

        double percentage = (double) equal / tests * 100;

        System.out.printf(
            "Property: distributivity | Type: double | Percentage: %.4f%%%n",
            percentage
        );
    }
}