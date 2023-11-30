public class hola {
    public static void main(String[] args) {
        imprimirCohete();
    }

    public static void imprimirCohete() {
        int alturaCohete = 15;

        for (int i = 0; i < alturaCohete; i++) {
            System.out.print(" ".repeat(alturaCohete - i - 1));
            System.out.print("/");
            System.out.print(" ".repeat(2 * i));
            System.out.println("\\");
        }

        System.out.println("|" + " ".repeat(2 * alturaCohete - 2) + "|");
        System.out.println("|" + " ".repeat(2 * alturaCohete - 2) + "|");

        for (int i = 0; i <= alturaCohete; i++) {
            System.out.println("|" + "|".repeat(2 * alturaCohete - 2) + "|");
        }
    }
}
