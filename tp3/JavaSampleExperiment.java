import java.util.Random;

public class JavaSampleExperiment {
    public static void main(String[] args) {
        int tests = Integer.parseInt(args[0]);
        long seed = Long.parseLong(args[1]);
        double minimum = Double.parseDouble(args[2]);
        double maximum = Double.parseDouble(args[3]);
        String numberType = args[4];
        String property = args[5];
        boolean inclusive = Boolean.parseBoolean(args[6]);

        Random random = new Random(seed);
        int equal = 0;
        long scale = 1L << 53;

        for (int i = 0; i < tests; i++) {
            double x = sample(random, minimum, maximum, scale, inclusive);
            double y = sample(random, minimum, maximum, scale, inclusive);
            double z = sample(random, minimum, maximum, scale, inclusive);

            if ("Float".equals(numberType)) {
                if (checkFloat(property, (float) x, (float) y, (float) z)) {
                    equal++;
                }
            } else if (checkDouble(property, x, y, z)) {
                equal++;
            }
        }

        double percentage = 100.0 * equal / tests;
        System.out.printf(
            java.util.Locale.ROOT,
            "{\"equal\":%d,\"percentage\":%.9f}%n",
            equal,
            percentage
        );
    }

    private static double sample(
        Random random, double minimum, double maximum, long scale, boolean inclusive
    ) {
        long numerator = inclusive
            ? random.nextLong(scale + 1)
            : random.nextLong(scale);
        double unit = (double) numerator / scale;
        return minimum + (maximum - minimum) * unit;
    }

    private static boolean checkDouble(String property, double x, double y, double z) {
        switch (property) {
            case "AdditionAssociativity":
                return (x + y) + z == x + (y + z);
            case "MultiplicationAssociativity":
                return (x * y) * z == x * (y * z);
            case "Distributivity":
                return x * (y + z) == (x * y) + (x * z);
            default:
                throw new IllegalArgumentException("Unknown property: " + property);
        }
    }

    private static boolean checkFloat(String property, float x, float y, float z) {
        switch (property) {
            case "AdditionAssociativity":
                return (x + y) + z == x + (y + z);
            case "MultiplicationAssociativity":
                return (x * y) * z == x * (y * z);
            case "Distributivity":
                return x * (y + z) == (x * y) + (x * z);
            default:
                throw new IllegalArgumentException("Unknown property: " + property);
        }
    }
}
