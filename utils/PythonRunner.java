import java.io.*;

public class PythonRunner {
    public static void main(String[] args) {
        try {

            String scriptPath = "formatter.py";


            ProcessBuilder pb = new ProcessBuilder("python", scriptPath);


            pb.directory(new File("C:\\xampp\\htdocs\\midterm\\utils"));


            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            System.out.println("Formatted Report:");
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            boolean hasError = false;
            while ((line = errorReader.readLine()) != null) {
                hasError = true;
                System.err.println("Python error: " + line);
            }

            int exitCode = process.waitFor();
            if (!hasError) {
                System.out.println("Python script finished with exit code " + exitCode);
            } else {
                System.err.println("Python script finished with errors (code " + exitCode + ")");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
