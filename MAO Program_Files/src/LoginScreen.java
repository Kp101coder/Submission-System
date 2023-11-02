import java.awt.*;
import javax.swing.*;
import static javax.swing.GroupLayout.Alignment.*;
import java.awt.event.*;
import java.io.File;
import java.io.IOException;
 
public class LoginScreen extends JFrame 
{
    public volatile boolean check = false;
    public static String user, password;
    public LoginScreen() 
    {
        System.out.println("Initiating Login Screen");
        java.awt.EventQueue.invokeLater(new Runnable() 
        {
            public void run() 
            {
                try 
                {
                    UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
                } catch (Exception ex) {}
                createScreen();
            }
        });
    } 
    public void createScreen() 
    {
        JLabel label = new JLabel("Enter ID");;
        JTextField userField = new JTextField();
        JLabel label2 = new JLabel("Enter Password");
        JTextField passwordField = new JTextField();
        JButton enterButton = new JButton("Enter");
        JButton deleteMessage = new JButton("Delete the startup video/message");
        enterButton.setPreferredSize(deleteMessage.getPreferredSize());
        deleteMessage.setForeground(Color.WHITE);
        deleteMessage.setBackground(Color.BLACK);
        enterButton.setForeground(Color.WHITE);
        enterButton.setBackground(Color.BLACK);
        JLabel madeBy = new JLabel("Made by: Krish Prabhu");
        JTextPane textPane = new JTextPane();
        textPane.setText("MAO form uploading tool:\n.JPEG FILES ONLY! If not .jpeg, search up file converter and convert your file to jpeg!\nIf you are a student, please enter your NAME. Your password will be given to you by MAO team at meeting. Make sure to provide them your name AND your grade.\nAdministrators must enter Admin ID and password to continue.");
        textPane.setBackground(Color.RED);
        textPane.setForeground(Color.WHITE);
        JScrollPane scrollPane = new JScrollPane(textPane);
        scrollPane.setVerticalScrollBarPolicy(javax.swing.ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED);
        GroupLayout layout = new GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setAutoCreateGaps(true);
        layout.setAutoCreateContainerGaps(true);
        layout.setHorizontalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup()
                .addGroup(layout.createSequentialGroup()
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(label)
                        .addComponent(label2)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(userField)
                        .addComponent(passwordField)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(enterButton)
                        .addComponent(deleteMessage)
                    )
                )
                .addComponent(scrollPane)
                .addComponent(madeBy)
            )
        );
        layout.linkSize(SwingConstants.HORIZONTAL, enterButton);
        layout.linkSize(SwingConstants.HORIZONTAL, deleteMessage);
        layout.setVerticalGroup(layout.createSequentialGroup()
            .addGroup(layout.createParallelGroup(BASELINE)
                .addComponent(label)
                .addComponent(userField)
                .addComponent(enterButton)
            )
            .addGroup(layout.createParallelGroup(LEADING)
                .addGroup(layout.createSequentialGroup()
                    .addGroup(layout.createParallelGroup(BASELINE)
                        .addComponent(label2)
                        .addComponent(passwordField)
                        .addComponent(deleteMessage)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(scrollPane)
                    )
                    .addGroup(layout.createParallelGroup(LEADING)
                        .addComponent(madeBy)
                    )
                )
            )
        );
        setTitle("MAO FORM UPLOADER LOGIN");
        pack();
        setSize(500,300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
        deleteMessage.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Deleting Message");
                try 
                {
                    
                    Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "11"});
                }
                catch (IOException e1) 
                {
                    MainAPI.ifError(e1.toString());
                }
            }
        });
        enterButton.addActionListener(new ActionListener() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Entering Data Button");
                try
                {
                    File validated = new File("Temp\\Validated.txt");
                    validated.deleteOnExit();
                    File unvalidated = new File("Temp\\Unvalidated.txt");
                    unvalidated.deleteOnExit();
                    textPane.setText("LOADING...");
                    user = userField.getText();
                    password = passwordField.getText();
                    SwingWorker<Void, Void> worker = new SwingWorker<Void, Void>() 
                    {
                        protected Void doInBackground() throws Exception 
                        {
                            
                            Process process = Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "1", user, password});
                            process.waitFor(); // Wait for the process to complete
                            return null;
                        }

                        @Override
                        protected void done() 
                        {
                            if (validated.exists()) 
                            {
                                textPane.setText("Username and Password match!");
                                validated.delete();
                                check = true;
                            } 
                            else 
                            {
                                textPane.setText("Username and Password do not match.");
                                unvalidated.delete();
                            }
                        }
                    };
                    worker.execute(); // Start the SwingWorker
                }
                catch(Exception e1)
                {
                    MainAPI.ifError(e1.toString());
                }
            }
        });
        getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), "enterPressed");
        getRootPane().getActionMap().put("enterPressed", new AbstractAction() 
        {
            public void actionPerformed(ActionEvent e) 
            {
                System.out.println("Entering Data");
                try
                {
                    File validated = new File("Temp\\Validated.txt");
                    validated.deleteOnExit();
                    File unvalidated = new File("Temp\\Unvalidated.txt");
                    unvalidated.deleteOnExit();
                    textPane.setText("LOADING...");
                    user = userField.getText();
                    password = passwordField.getText();
                    SwingWorker<Void, Void> worker = new SwingWorker<Void, Void>() 
                    {
                        protected Void doInBackground() throws Exception 
                        {
                            
                            Process process = Runtime.getRuntime().exec(new String[] {"Python\\python.exe", "Main.py", "1", user, password});
                            process.waitFor(); // Wait for the process to complete
                            return null;
                        }

                        @Override
                        protected void done() 
                        {
                            if (validated.exists()) 
                            {
                                textPane.setText("Username and Password match!");
                                validated.delete();
                                check = true;
                            } 
                            else 
                            {
                                textPane.setText("Username and Password do not match.");
                                unvalidated.delete();
                            }
                        }
                    };
                    worker.execute(); // Start the SwingWorker
                }
                catch(Exception e1)
                {
                    MainAPI.ifError(e1.toString());
                }
            }
        });
    }
    public boolean getUserAuth()
    {
        return check;
    }
}