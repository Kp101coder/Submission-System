import java.io.*;
import java.time.LocalDate;
import java.util.Scanner;
import javax.swing.*;

public class MainAPI
{
  private static final String version = "1.0";
  public static void ifError(String e)
  {
    JFrame errorFound = new JFrame("Well Shit");
    errorFound.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    errorFound.setExtendedState(JFrame.MAXIMIZED_BOTH);
    errorFound.setSize(500, 300);
    JTextPane errorText = new JTextPane();
    errorText.setText("There was an error processing your request.\nPlease close this page and try again.\nError:\n" + e + "\n\nVersion: " + version);
    errorFound.setContentPane(errorText);
    errorFound.setLayout(null);
    errorFound.setVisible(true);
  }
  public static void main(String[] args) throws IOException, InterruptedException
  {
    System.out.println("Program Starting");
    new File("Temp\\pyout.txt").deleteOnExit();
    //get userlogin and admin
    System.out.println("Checking Date");
    String curDate = LocalDate.now().toString().substring(5);
    FileWriter writer;
    File lastDate = new File("Assets/lastDate.txt");
    try(Scanner input = new Scanner(lastDate))
    {
      String date = input.nextLine();
      String month = date.substring(0,2);
      String day = date.substring(3);
      if(Math.abs(Integer.parseInt(curDate.substring(3))-Integer.parseInt(day))>7 || Integer.parseInt(curDate.substring(0,2)) > Integer.parseInt(month))
      {
        System.out.println("Deleting User Token");
        try
        {
          new File("User/token.json").delete();
        }catch(Exception e){}
        lastDate.delete();
        lastDate = new File("Assets/lastDate.txt");
        writer = new FileWriter(lastDate);
        writer.write(curDate);
        writer.close();
      }
    }
    catch(Exception e)
    {
      lastDate = new File("Assets/lastDate.txt");
      writer = new FileWriter(lastDate);
      writer.write(curDate);
    }
    System.out.println("Starting Login Screen");
    LoginScreen lS = new LoginScreen();
    while(!lS.getUserAuth())
    {
      continue;
    }
    System.out.println("Authentication Recived");
    lS.dispose();
    try 
    {
      System.out.println("Starting Student Screen");
      new StudentScreen(LoginScreen.user, LoginScreen.password);
    } 
    catch (Exception e) 
    {
      ifError(e.toString());
    }
  }
}