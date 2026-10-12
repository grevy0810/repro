
public class BankingProblem {
    public static void main(String[] args) {
        double money = Math.E;
        int years = 50;

        for (int n = 1; n <= years; n++) {
            money = (money - 1) * n;
        }
        money -= 1;

        System.out.println("Money after " + years + " years: " + money + " euros");
    }
}
