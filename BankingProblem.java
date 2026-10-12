import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class BankingProblem {
    public static void main(String[] args) throws IOException {
        double money = Math.E;
        int years = 50;
        String outputDir = System.getenv().getOrDefault("OUTPUT_DIR", ".");

        for (int n = 1; n <= years; n++) {
            money = (money - 1) * n;
        }
        money -= 1;
        File outputFile = new File(outputDir, "answer_banking.txt");
        
        try (PrintWriter file = new PrintWriter(new FileWriter(outputFile))) {
            file.println("Money after " + years + " years: "
                    + money + " euros");
        }

        System.out.println("Results saved to " + outputFile.getPath());
    }
}
