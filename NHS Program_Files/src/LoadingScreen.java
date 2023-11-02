import java.awt.*;
import java.io.IOException;
 
public class LoadingScreen 
{
    public LoadingScreen() throws NullPointerException, IllegalStateException, InterruptedException, IOException
    {
        System.out.println("New Messages");
        Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "0"});
        final SplashScreen splash = SplashScreen.getSplashScreen();
        Graphics2D g = splash.createGraphics();
        for(int i=0; i<150; i++) 
        {
            renderSplashFrame(g, i);
            splash.update();
            Thread.sleep(80);
        }
        splash.close();
    }
    private static void renderSplashFrame(Graphics2D g, int frame) 
    {
        final String[] comps = {"Getting bork.exe", "Training doggie", "Finding woof","I LV Vaayu", "Loading treats", "Locating poopbag", "Sniffing Cats","Locating DogPride", "Locating AHSPride", "Deleting Bite.virus ;]", "Smelling food", "Stealing food", "Walking outside", "Touch grass, you should"};
        g.setComposite(AlphaComposite.Clear);
        g.fillRect(100,135,200,40);
        g.setPaintMode();
        g.setColor(Color.WHITE);
        g.drawString(comps[(frame/8)%comps.length]+"...", 100, 145);
    }
    public static void main(String[] args) throws NullPointerException, IllegalStateException, InterruptedException, IOException
    {
        new LoadingScreen();
    }
}