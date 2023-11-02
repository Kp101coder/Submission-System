import java.awt.*;
import javax.imageio.ImageIO;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.*;
import javax.swing.filechooser.*;
import javax.swing.filechooser.FileFilter;
import static javax.swing.GroupLayout.Alignment.*;
import java.awt.event.*;
import java.io.*;
import java.net.URL;
import java.util.*;

public class StudentScreen extends JFrame
{
    private boolean anyFile = false;
    private String filepath = "";
    private int counter = 15;
    private String username;
    private String password;
    public StudentScreen(String user, String p) throws IOException 
    {
        System.out.println("Initiating Student Screen");
        createScreen();
        username = user;
        password = p;
    }
    public void createScreen() throws IOException 
    {
        //PreItems
        System.out.println("Running Pre-operations");
        Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "16"});
        File opsText = new File("Temp\\ops.txt");
        opsText.deleteOnExit();
        probationNotification();
        JLabel selectLabel = new JLabel("Click the Select Form button to choose a jpeg of your form.");;
        JLabel submitLabel = new JLabel("Click the Submit button to upload your jpeg. NO UNDOs!");
        JLabel fileName = new JLabel("File Selected: ");
        JLabel instructions = new JLabel("");
        JButton submitButton = new JButton("Sumbit");
        JButton selectButton = new JButton("Select Form");
        JButton viewOps = new JButton("View Volunteer Oportunities");
        JButton requestHours = new JButton("View Hours Sheet");
        JTextArea notes = new JTextArea("Add Notes Here");
        notes.setLineWrap(true);
        notes.setWrapStyleWord(true);
        viewOps.setForeground(Color.WHITE);
        viewOps.setBackground(Color.BLACK);
        requestHours.setForeground(Color.WHITE);
        requestHours.setBackground(Color.BLACK);
        submitButton.setForeground(Color.WHITE);
        submitButton.setBackground(Color.BLACK);
        selectButton.setForeground(Color.WHITE);
        selectButton.setBackground(Color.BLACK);
        GroupLayout layout = new GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setAutoCreateGaps(true);
        layout.setAutoCreateContainerGaps(true);
        layout.setHorizontalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup(LEADING)
                .addComponent(selectLabel)
                .addComponent(submitLabel)
                .addComponent(fileName)
                .addGroup(layout.createSequentialGroup()
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(requestHours))
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(viewOps)))
                .addComponent(instructions)
                .addComponent(notes))
            .addGroup(layout.createParallelGroup(LEADING)
                .addComponent(selectButton)
                .addComponent(submitButton))
        );
        layout.linkSize(SwingConstants.HORIZONTAL, submitButton);
        layout.linkSize(SwingConstants.HORIZONTAL, selectButton);
        layout.setVerticalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(selectLabel)
                .addComponent(selectButton)
            )
            .addGroup(layout.createParallelGroup(LEADING)
                .addGroup(layout.createSequentialGroup()
                    .addGroup(layout.createParallelGroup(BASELINE)
                        .addComponent(submitLabel)
                        .addComponent(submitButton)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(fileName)
                    )
                    .addGroup(layout.createParallelGroup(BASELINE)
                        .addComponent(requestHours)
                        .addComponent(viewOps)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(instructions)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(notes)
                    )
                )
            )
        );
        setTitle("MAO FORM UPLOADER");
        pack();
        setSize(500,300);
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        setVisible(true);
        requestHours.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e)
            {
                System.out.println("Requesting Hours for User");
                try
                {
                    
                    Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "4"});
                    //api command download hours file for user
                    instructions.setText("File to download to Downloads folder in 20 sec if available");
                }
                catch(Exception l)
                {
                    MainAPI.ifError(l.toString());
                }
            }
        });
        viewOps.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Viewing Opportunities");
                try 
                {
                    while(!opsText.exists())
                    {
                        continue;
                    }
                    JFrame frame = new JFrame("Club Opps");
                    frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
                    frame.setSize(Toolkit.getDefaultToolkit().getScreenSize());
                    JEditorPane editorPane = new JEditorPane();
                    editorPane.setEditable(false);
                    editorPane.setContentType("text/html");
                    URL url = new File("Assets\\obg.jpg").toURI().toURL();
                    String header = "<style>table {table-layout: fixed;}, th, td {border:1px solid black;word-break: break-all;}h1 {text-align: center;}p {text-align: center;}</style><h1 style=\"color:red;font-size:30px;\">MAO Club Volunteer Opportunities Chart</h1><table style=\"width:100%;background-image: url(" + url.toString() + ");\"><thead><tr><th>Opportunity Name</th><th>Opportunity Date</th><th>Opportunity Location</th><th>Other Opportunity Information</th></tr></thead>";
                    StringBuilder opB = new StringBuilder();
                    Scanner opsReader = new Scanner(opsText);
                    while(opsReader.hasNextLine())
                    {
                        String nextOp = opsReader.nextLine();
                        if(!nextOp.equals(""))
                        {
                            nextOp = nextOp.replace(":", "</td><td>");
                            opB.append("<tr><td>");
                            opB.append(nextOp);
                            opB.append("</td></tr>");
                        }
                    }
                    opsReader.close();
                    String footer = "<tfoot><tr><th>End List</th><th>End List</th><th>End List</th><th>End List</th></tr></tfoot></table>";
                    editorPane.setText(header+opB.toString()+footer);
                    editorPane.setBackground(new Color(0, 0, 0, 0));
                    JScrollPane scrollPane = new JScrollPane(editorPane, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
                    frame.add(scrollPane);
                    frame.setVisible(true);
                }
                catch (IOException e1) 
                {
                    MainAPI.ifError(e.toString());
                }
            }
        });
        selectButton.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Opening Selection");
                try 
                {
                    UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
                } 
                catch (Exception m) 
                {
                    MainAPI.ifError(m.toString());
                }
                JFileChooser jfc = new JFileChooser(FileSystemView.getFileSystemView().getHomeDirectory());
                FileFilter imageFilter = new FileNameExtensionFilter("Image files", ImageIO.getReaderFileSuffixes());
                jfc.addChoosableFileFilter(imageFilter);
                jfc.setAcceptAllFileFilterUsed(false);
                int returnValue = jfc.showOpenDialog(null);
                if (returnValue == JFileChooser.APPROVE_OPTION) 
                {
                    File selectedFile = jfc.getSelectedFile();
                    filepath = selectedFile.getAbsolutePath();
                    fileName.setText("File Selected: " + filepath.substring(filepath.lastIndexOf("\\")+1));
                    if(filepath.substring(filepath.lastIndexOf(".")).equals(".jpg") || filepath.substring(filepath.lastIndexOf(".")).equals(".JPG") || filepath.substring(filepath.lastIndexOf(".")).equals(".jpeg") || filepath.substring(filepath.lastIndexOf(".")).equals(".JPEG"))
                    {
                        anyFile = true;
                    }
                    else
                    {
                        fileName.setText("Error. Invalid file type. Please convert file to .jpeg or .jpg");
                        instructions.setText("Use this: https://image.online-convert.com/convert-to-jpg");
                    } 
                }
            }
        });
        submitButton.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Submitting File");
                if(anyFile)
                {
                    String note = notes.getText();
                    anyFile = false;
                    try
                    {
                        //Api command 1
                        Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "2", username, password, filepath, note});
                        notes.setText("Enter notes here");
                    }
                    catch(Exception l)
                    {
                        MainAPI.ifError(l.toString());
                    }
                    java.util.Timer timer = new java.util.Timer();
                    try
                    {
                        //Haha i did the funni!!!!:)          
                        Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "69"});
                    }
                    catch(Exception F)
                    {
                        MainAPI.ifError(F.toString());
                    }
                    timer.schedule( new TimerTask()
                    {
                        public void run()
                        {
                            counter--;
                            instructions.setText("Completing upload in: " + counter + " seconds");
                            fileName.setText("Upload in Progress DO NOT CLOSE");
                            if(counter <= 0)
                            {
                                File checkerFile = new File("Temp\\was.txt");
                                if(checkerFile.exists())
                                {
                                    instructions.setText("Your file was successfully uploaded");
                                    fileName.setText("SELECT A NEW FILE TO UPLOAD");
                                    checkerFile.delete();
                                    counter=15;
                                    timer.cancel();
                                }
                                else if((checkerFile = new File("Temp\\not.txt")).exists())
                                {
                                    instructions.setText("FILE NOT UPLOADED");
                                    fileName.setText("VIEW YOUR EMAIL");
                                    checkerFile.delete();
                                    counter=15;
                                    timer.cancel();
                                }                                
                            }
                        }
                    }, 0, 1000);
                }
                else
                {
                    fileName.setText("No File Present!");
                    instructions.setText("Please select a file using the Select Button.");
                }
            }
        });
    }
    public void probationNotification()
    {
        Thread t = new Thread(new Runnable() 
        {
            public void run()
            {
                System.out.println("Checking Probation Status");
                try
                {
                    //api command download hours file for program
                    Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "10"});
                    File tempHours = new File("Temp\\studentHours.txt");
                    File checkerFile = new File("Temp\\condCheckH.txt");
                    System.out.println("Waiting For File");
                    while(!tempHours.exists() && !checkerFile.exists())
                    {
                        continue;
                    }
                    ArrayList<String> userHours = new ArrayList<>();
                    if(tempHours.exists())
                    {
                        System.out.println("Found Hours File");
                        Scanner input = new Scanner(tempHours);
                        String str = "";
                        System.out.println("Reading File");
                        while(input.hasNextLine())
                        {
                            String next = input.nextLine();
                            if(next != "" && input.hasNextLine())
                            {
                                str+=next+"\n";
                            }
                            else if(next != "")
                            {
                                str+=next;
                            }
                        }
                        input.close();
                        checkerFile.delete();
                        tempHours.delete();
                        Collections.addAll(userHours,str.split("\n"));
                        System.out.println("Completed Read Searching for Probation Status");
                        if(searchFor(username, userHours) != -1)
                        {
                            String data = userHours.get(searchFor(username, userHours));
                            if(data.contains("true"))
                            {
                                JFrame fP = new JFrame("YOU ARE ON PROBATION");
                                JLabel haha = new JLabel("YOU ARE ON PROBATION.");
                                JLabel haha2 = new JLabel("CONTACT AN OFFICER OR SUBMIT LATE HOURS");
                                haha.setFont(new Font("Times New Roman", Font.PLAIN, 20));
                                haha2.setFont(new Font("Times New Roman", Font.PLAIN, 20));
                                // Set the layout manager to FlowLayout with center alignment
                                fP.setLayout(new FlowLayout(FlowLayout.CENTER));
                                fP.add(haha);
                                fP.add(haha2);
                                fP.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                                fP.pack();
                                fP.setVisible(true);
                                playSound();
                                try
                                {
                                    
                                    Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "17"});
                                }
                                catch(Exception F)
                                {
                                    MainAPI.ifError(F.toString());
                                }
                            }
                            else
                            {
                                System.out.println("Not on Probation");
                            }
                        }
                    }
                    else
                    {
                        System.out.println("Found Fail File");
                        JFrame fP = new JFrame("No File Found");
                        JLabel haha = new JLabel("Unable to check probation status");
                        JLabel haha2 = new JLabel("Hours file may not exist temporarily");
                        haha.setFont(new Font("Times New Roman", Font.PLAIN, 20));
                        haha2.setFont(new Font("Times New Roman", Font.PLAIN, 20));
                        // Set the layout manager to FlowLayout with center alignment
                        fP.setLayout(new FlowLayout(FlowLayout.CENTER));
                        fP.add(haha);
                        fP.add(haha2);
                        fP.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                        fP.pack();
                        fP.setVisible(true);
                        checkerFile.delete();
                    }
                }
                catch(Exception f)
                {
                    System.out.println("Unable to notify probation status");
                }
            }
        });
        t.start();
    }
    public int searchFor(String str, ArrayList<String> arr)
    {
        for(int i = 0; i<arr.size(); i++)
        {
            if(arr.get(i).contains(str))
            {
                return i;
            }
        }
        return -1;
    }
    public static synchronized void playSound() throws UnsupportedAudioFileException,IOException, LineUnavailableException
    {
        AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("Assets/hellothere.wav"));
        Clip clip = AudioSystem.getClip();
        clip.open(audioInputStream);
        clip.start();
    }
}
